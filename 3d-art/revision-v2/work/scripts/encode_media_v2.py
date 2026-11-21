"""Encode travel films and the 27 s combined reel from numbered PNG frames.

    python encode_media_v2.py --run-root <run> --staging-root <bundle> --ffmpeg <path>
"""
import argparse
import json
import os
import shutil
import subprocess


def run(cmd, log_path, check=True):
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write("CMD " + " ".join(cmd) + "\n")
        p = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("command failed (%d): %s" % (p.returncode, " ".join(cmd)))
    return p.returncode


def frames_ok(directory, start, end):
    missing = []
    for i in range(start, end + 1):
        p = os.path.join(directory, "frame_%04d.png" % i)
        if not os.path.exists(p) or os.path.getsize(p) < 5000:
            missing.append(i)
    return missing


def encode_seq(ffmpeg, frames_dir, out, log, fps=24, start=1):
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
           "-framerate", str(fps), "-start_number", str(start),
           "-i", os.path.join(frames_dir, "frame_%04d.png"),
           "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(fps),
           "-movflags", "+faststart", out]
    run(cmd, log)


def ffprobe(ffprobe_bin, path):
    p = subprocess.run([ffprobe_bin, "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=codec_name,width,height,r_frame_rate,"
                        "avg_frame_rate,nb_frames,duration,pix_fmt",
                        "-show_entries", "format=duration,size",
                        "-of", "json", path], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return json.loads(p.stdout)


def full_decode(ffmpeg, path, log):
    return run([ffmpeg, "-v", "error", "-xerror", "-i", path, "-map", "0:v:0",
                "-f", "null", "-"], log, check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--staging-root", required=True)
    ap.add_argument("--ffmpeg", required=True)
    a = ap.parse_args()
    run_root, stage = a.run_root, a.staging_root
    ffmpeg = a.ffmpeg
    ffprobe_bin = os.path.join(os.path.dirname(ffmpeg), "ffprobe.exe")
    if not os.path.exists(ffprobe_bin):
        ffprobe_bin = shutil.which("ffprobe") or "ffprobe"
    log = os.path.join(run_root, "logs", "encode.log")
    report = {"travel": {}, "reel": {}, "frames_checked": {}}
    for site in ("kodingareng", "tunda", "amur"):
        frames_dir = os.path.join(run_root, "renders", "travel", site)
        missing = frames_ok(frames_dir, 1, 168)
        report["frames_checked"][site] = {"expected": 168, "missing": missing}
        if missing:
            raise RuntimeError("%s travel missing frames: %s" % (site, missing[:12]))
        out = os.path.join(stage, "media", "coasts", site, "travel.mp4")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        encode_seq(ffmpeg, frames_dir, out, log)
        report["travel"][site] = {"path": "media/coasts/%s/travel.mp4" % site,
                                  "bytes": os.path.getsize(out),
                                  "ffprobe": ffprobe(ffprobe_bin, out),
                                  "decode_exit": full_decode(ffmpeg, out, log)}
    # build the reel frame sequence with hardlinks
    reel_dir = os.path.join(run_root, "renders", "reel-frames")
    shutil.rmtree(reel_dir, ignore_errors=True)
    os.makedirs(reel_dir)
    seq = []
    globe_dir = os.path.join(run_root, "renders", "globe-reel")
    for i in range(1, 97):
        seq.append(os.path.join(globe_dir, "frame_%04d.png" % i))
    for site in ("kodingareng", "tunda", "amur"):
        d = os.path.join(run_root, "renders", "travel", site)
        for i in range(1, 169):
            seq.append(os.path.join(d, "frame_%04d.png" % i))
    for i in range(97, 145):
        seq.append(os.path.join(globe_dir, "frame_%04d.png" % i))
    missing = [p for p in seq if not os.path.exists(p)]
    if missing:
        raise RuntimeError("reel source frames missing: %s" % missing[:8])
    for idx, src in enumerate(seq, 1):
        dst = os.path.join(reel_dir, "frame_%04d.png" % idx)
        try:
            os.link(src, dst)
        except Exception:
            shutil.copy2(src, dst)
    for i in range(1, len(seq) + 1):
        if not os.path.exists(os.path.join(reel_dir, "frame_%04d.png" % i)):
            raise RuntimeError("reel frame gap at %d" % i)
    out = os.path.join(stage, "media", "coast-reel.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    encode_seq(ffmpeg, reel_dir, out, log)
    report["reel"] = {"path": "media/coast-reel.mp4", "frames": len(seq),
                      "seconds": round(len(seq) / 24.0, 2),
                      "bytes": os.path.getsize(out),
                      "ffprobe": ffprobe(ffprobe_bin, out),
                      "decode_exit": full_decode(ffmpeg, out, log)}
    with open(os.path.join(run_root, "logs", "encode-report.json"), "w",
              encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print("ENCODE " + json.dumps({"travel": list(report["travel"]),
                                  "reel_frames": len(seq),
                                  "reel_bytes": report["reel"]["bytes"]}))


if __name__ == "__main__":
    main()
