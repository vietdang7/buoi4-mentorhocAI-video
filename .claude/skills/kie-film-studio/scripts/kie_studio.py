#!/usr/bin/env python3
"""
KIE Film Studio — KIE.ai pipeline driver for GPT Image 2 (storyboard) + Seedance 2.0 mini (video).

Zero external deps (stdlib only). Talks to the unified KIE jobs API:
  create : POST https://api.kie.ai/api/v1/jobs/createTask   {model, input} -> {data.taskId}
  poll   : GET  https://api.kie.ai/api/v1/jobs/recordInfo?taskId=...
           data.state in {waiting,queuing,generating,success,fail}
           data.resultJson (JSON STRING) -> {"resultUrls":[...]}

Subcommands:
  image   --prompt ... [--aspect-ratio 16:9] [--resolution 1K|2K|4K] [--out FILE]
  video   --prompt ... (--first-frame-url URL | --first-frame-file FILE-not-supported)
                       [--last-frame-url URL] [--duration N] [--resolution 480p|720p]
                       [--aspect-ratio 16:9] [--no-audio] [--out FILE]
  run     MANIFEST.json [--from storyboard|animate|assemble] [--only storyboard|animate|assemble]
                       [--concurrency N] [--outdir DIR]
  poll    --task-id ID [--out FILE]

Models (override via --model or manifest):
  image: gpt-image-2-text-to-image
  video: bytedance/seedance-2-fast   (this is the KIE slug for "Seedance 2.0 mini")
"""
import argparse, json, os, sys, time, urllib.request, urllib.error, urllib.parse, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

API_BASE = "https://api.kie.ai/api/v1/jobs"
IMAGE_MODEL = "gpt-image-2-text-to-image"
VIDEO_MODEL = "bytedance/seedance-2-fast"  # Seedance 2.0 mini on KIE
POLL_INTERVAL = 6        # seconds between polls
POLL_TIMEOUT = 900       # max seconds to wait per task
_SSL = ssl.create_default_context()


# ---------- auth ----------
def load_api_key():
    key = os.environ.get("KIE_AI_API_KEY")
    if key:
        return key.strip()
    # search upward for a .env
    here = os.path.abspath(os.getcwd())
    for d in [here] + list(_parents(here)):
        envp = os.path.join(d, ".env")
        if os.path.isfile(envp):
            for line in open(envp, encoding="utf-8"):
                line = line.strip()
                if line.startswith("KIE_AI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    die("KIE_AI_API_KEY not found in env or any parent .env")


def _parents(path):
    while True:
        nxt = os.path.dirname(path)
        if nxt == path:
            return
        path = nxt
        yield path


# ---------- http ----------
def _req(method, url, key, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    last = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, context=_SSL, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            payload = e.read().decode(errors="replace")
            if e.code == 429 or 500 <= e.code < 600:
                wait = 2 ** attempt
                eprint(f"  HTTP {e.code}, retry in {wait}s ({payload[:160]})")
                time.sleep(wait)
                last = f"HTTP {e.code}: {payload[:300]}"
                continue
            die(f"HTTP {e.code} on {url}: {payload[:500]}")
        except urllib.error.URLError as e:
            wait = 2 ** attempt
            eprint(f"  network error, retry in {wait}s ({e})")
            time.sleep(wait)
            last = str(e)
    die(f"request failed after retries: {last}")


def create_task(key, model, inp):
    resp = _req("POST", f"{API_BASE}/createTask", key, {"model": model, "input": inp})
    if resp.get("code") != 200:
        die(f"createTask failed: code={resp.get('code')} msg={resp.get('msg')}")
    tid = (resp.get("data") or {}).get("taskId")
    if not tid:
        die(f"createTask returned no taskId: {resp}")
    return tid


def poll_task(key, task_id, label=""):
    url = f"{API_BASE}/recordInfo?" + urllib.parse.urlencode({"taskId": task_id})
    start = time.time()
    last_state = None
    while True:
        resp = _req("GET", url, key)
        data = resp.get("data") or {}
        state = data.get("state")
        if state != last_state:
            eprint(f"  [{label or task_id}] state={state}")
            last_state = state
        if state == "success":
            rj = data.get("resultJson") or "{}"
            try:
                parsed = json.loads(rj)
            except json.JSONDecodeError:
                die(f"resultJson not parseable: {rj[:300]}")
            urls = parsed.get("resultUrls") or []
            if not urls:
                die(f"success but no resultUrls: {parsed}")
            return urls, parsed
        if state == "fail":
            die(f"task {task_id} failed: {data.get('failCode')} {data.get('failMsg')}")
        if time.time() - start > POLL_TIMEOUT:
            die(f"task {task_id} timed out after {POLL_TIMEOUT}s (last state={state})")
        time.sleep(POLL_INTERVAL)


def download(url, out_path):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept": "*/*",
    })
    with urllib.request.urlopen(req, context=_SSL, timeout=300) as r, open(out_path, "wb") as f:
        while True:
            chunk = r.read(1 << 16)
            if not chunk:
                break
            f.write(chunk)
    return out_path


# ---------- high-level ops ----------
def gen_image(key, prompt, aspect_ratio="16:9", resolution="2K", model=IMAGE_MODEL,
              out=None, label="image"):
    inp = {"prompt": prompt, "aspect_ratio": aspect_ratio, "resolution": resolution}
    tid = create_task(key, model, inp)
    eprint(f"  [{label}] taskId={tid}")
    urls, _ = poll_task(key, tid, label)
    url = urls[0]
    local = None
    if out:
        local = download(url, out)
        eprint(f"  [{label}] saved {local}")
    return {"task_id": tid, "url": url, "file": local}


def gen_video(key, prompt, first_frame_url=None, last_frame_url=None, duration=5,
              resolution="720p", aspect_ratio="16:9", generate_audio=True,
              reference_image_urls=None, model=VIDEO_MODEL, out=None, label="video"):
    inp = {"prompt": prompt, "duration": int(duration), "resolution": resolution,
           "aspect_ratio": aspect_ratio, "generate_audio": bool(generate_audio)}
    if first_frame_url:
        inp["first_frame_url"] = first_frame_url
    if last_frame_url:
        inp["last_frame_url"] = last_frame_url
    if reference_image_urls:
        inp["reference_image_urls"] = reference_image_urls
    tid = create_task(key, model, inp)
    eprint(f"  [{label}] taskId={tid}")
    urls, _ = poll_task(key, tid, label)
    url = urls[0]
    local = None
    if out:
        local = download(url, out)
        eprint(f"  [{label}] saved {local}")
    return {"task_id": tid, "url": url, "file": local}


# ---------- manifest runner (deep-research-style phases) ----------
def _save_manifest(path, m):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def run_manifest(key, path, do_storyboard, do_animate, do_assemble, concurrency, outdir):
    m = json.load(open(path, encoding="utf-8"))
    d = m.get("defaults", {})
    shots = m["shots"]
    title = m.get("title", "film")
    outdir = outdir or os.path.join(os.path.dirname(os.path.abspath(path)), "output")
    img_dir = os.path.join(outdir, "frames")
    vid_dir = os.path.join(outdir, "clips")

    # Phase: storyboard (images) — parallel
    if do_storyboard:
        eprint(f"\n=== STORYBOARD PHASE ({sum(1 for s in shots if not s.get('image_url'))} frames to generate) ===")
        todo = [s for s in shots if not s.get("image_url") and s.get("image_prompt")]
        def _img(s):
            r = gen_image(key, s["image_prompt"],
                          s.get("aspect_ratio", d.get("aspect_ratio", "16:9")),
                          s.get("image_resolution", d.get("image_resolution", "2K")),
                          s.get("image_model", d.get("image_model", IMAGE_MODEL)),
                          out=os.path.join(img_dir, f"{s['id']}.png"), label=f"img:{s['id']}")
            s["image_url"], s["image_file"] = r["url"], r["file"]
            return s["id"]
        _parallel(_img, todo, concurrency, lambda: _save_manifest(path, m))
        _save_manifest(path, m)
        eprint("  storyboard manifest updated.")

    # Phase: animate (videos) — parallel, depends on image_url
    if do_animate:
        ready = [s for s in shots if s.get("image_url") and not s.get("video_file")]
        eprint(f"\n=== ANIMATE PHASE ({len(ready)} clips) ===")
        def _vid(s):
            r = gen_video(key, s.get("motion_prompt") or s.get("image_prompt"),
                          first_frame_url=s["image_url"],
                          last_frame_url=s.get("last_frame_url"),
                          duration=s.get("duration", d.get("duration", 5)),
                          resolution=s.get("video_resolution", d.get("video_resolution", "720p")),
                          aspect_ratio=s.get("aspect_ratio", d.get("aspect_ratio", "16:9")),
                          generate_audio=s.get("generate_audio", d.get("generate_audio", True)),
                          model=s.get("video_model", d.get("video_model", VIDEO_MODEL)),
                          out=os.path.join(vid_dir, f"{s['id']}.mp4"), label=f"vid:{s['id']}")
            s["video_url"], s["video_file"] = r["url"], r["file"]
            return s["id"]
        _parallel(_vid, ready, concurrency, lambda: _save_manifest(path, m))
        _save_manifest(path, m)
        eprint("  animate manifest updated.")

    # Phase: assemble — ffmpeg concat in shot order
    if do_assemble:
        clips = [s["video_file"] for s in shots if s.get("video_file")]
        if not clips:
            die("assemble: no clips found. Run animate first.")
        final = os.path.join(outdir, f"{_safe(title)}.mp4")
        _ffmpeg_concat(clips, final)
        m["final_video"] = final
        _save_manifest(path, m)
        eprint(f"\n=== FINAL FILM: {final} ===")
    return m


def _parallel(fn, items, concurrency, checkpoint):
    if not items:
        return
    errors = []
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as ex:
        futs = {ex.submit(fn, it): it for it in items}
        for fut in as_completed(futs):
            try:
                sid = fut.result()
                eprint(f"  ✓ done {sid}")
                checkpoint()
            except SystemExit as e:
                errors.append(str(e))
            except Exception as e:
                errors.append(repr(e))
    if errors:
        die("some tasks failed:\n  - " + "\n  - ".join(errors))


def _ffmpeg_concat(clips, out):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    listfile = out + ".concat.txt"
    with open(listfile, "w") as f:
        for c in clips:
            f.write(f"file '{os.path.abspath(c)}'\n")
    # try stream copy first; fall back to re-encode if inputs differ
    import subprocess
    cmd_copy = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", out]
    if subprocess.run(cmd_copy, capture_output=True).returncode == 0:
        eprint(f"  concat (copy) -> {out}")
    else:
        eprint("  stream copy failed, re-encoding...")
        cmd_enc = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                   "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", out]
        r = subprocess.run(cmd_enc, capture_output=True)
        if r.returncode != 0:
            die("ffmpeg concat failed:\n" + r.stderr.decode(errors="replace")[-800:])
    os.remove(listfile)


# ---------- utils ----------
def _safe(s):
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in s)[:60] or "film"


def eprint(*a):
    print(*a, file=sys.stderr, flush=True)


def die(msg):
    eprint("ERROR:", msg)
    sys.exit(1)


# ---------- cli ----------
def main():
    p = argparse.ArgumentParser(description="KIE Film Studio pipeline driver")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("image")
    pi.add_argument("--prompt", required=True)
    pi.add_argument("--aspect-ratio", default="16:9")
    pi.add_argument("--resolution", default="2K")
    pi.add_argument("--model", default=IMAGE_MODEL)
    pi.add_argument("--out")

    pv = sub.add_parser("video")
    pv.add_argument("--prompt", required=True)
    pv.add_argument("--first-frame-url")
    pv.add_argument("--last-frame-url")
    pv.add_argument("--duration", type=int, default=5)
    pv.add_argument("--resolution", default="720p")
    pv.add_argument("--aspect-ratio", default="16:9")
    pv.add_argument("--no-audio", action="store_true")
    pv.add_argument("--model", default=VIDEO_MODEL)
    pv.add_argument("--out")

    pp = sub.add_parser("poll")
    pp.add_argument("--task-id", required=True)
    pp.add_argument("--out")

    pr = sub.add_parser("run")
    pr.add_argument("manifest")
    pr.add_argument("--from", dest="from_phase", choices=["storyboard", "animate", "assemble"])
    pr.add_argument("--only", choices=["storyboard", "animate", "assemble"])
    pr.add_argument("--concurrency", type=int, default=3)
    pr.add_argument("--outdir")

    a = p.parse_args()
    key = load_api_key()

    if a.cmd == "image":
        r = gen_image(key, a.prompt, a.aspect_ratio, a.resolution, a.model, a.out)
        print(json.dumps(r))
    elif a.cmd == "video":
        r = gen_video(key, a.prompt, a.first_frame_url, a.last_frame_url, a.duration,
                      a.resolution, a.aspect_ratio, not a.no_audio, model=a.model, out=a.out)
        print(json.dumps(r))
    elif a.cmd == "poll":
        urls, parsed = poll_task(key, a.task_id, "poll")
        if a.out:
            download(urls[0], a.out)
        print(json.dumps({"urls": urls, "result": parsed}))
    elif a.cmd == "run":
        if a.only and a.from_phase:
            die("pass either --only or --from, not both")
        phases = ["storyboard", "animate", "assemble"]
        if a.only:
            sel = {a.only}
        elif a.from_phase:
            sel = set(phases[phases.index(a.from_phase):])
        else:
            sel = set(phases)
        run_manifest(key, a.manifest, "storyboard" in sel, "animate" in sel,
                     "assemble" in sel, a.concurrency, a.outdir)


if __name__ == "__main__":
    main()
