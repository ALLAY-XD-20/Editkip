#!/usr/bin/env python3
"""Analyze reference/ videos -> notes/reference-analysis.json + notes/frames/<video>/ stills."""
import json, subprocess
from pathlib import Path

EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}

def probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate:format=duration",
        "-of", "json", str(p)], capture_output=True, text=True).stdout
    d = json.loads(out)
    st, dur = d["streams"][0], float(d["format"]["duration"])
    n, m = st["r_frame_rate"].split("/")
    return {"width": st["width"], "height": st["height"], "fps": round(int(n) / int(m), 2), "duration": round(dur, 2)}

def cuts(p):
    from scenedetect import detect, ContentDetector
    return [round(s[0].get_seconds(), 2) for s in detect(str(p), ContentDetector())][1:]

res = {}
for v in sorted(Path("reference").iterdir()):
    if v.suffix.lower() not in EXT:
        continue
    info = probe(v)
    c = cuts(v)
    info["cut_times"] = c
    info["cuts_per_min"] = round(len(c) / info["duration"] * 60, 1)
    info["avg_shot_len"] = round(info["duration"] / (len(c) + 1), 2)
    fd = Path("notes/frames") / v.stem
    fd.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vf", "fps=1,scale=480:-1",
                    "-frames:v", "40", str(fd / "f_%03d.jpg")])
    res[v.name] = info
    print(v.name, info["cuts_per_min"], "cuts/min")
Path("notes").mkdir(exist_ok=True)
Path("notes/reference-analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
