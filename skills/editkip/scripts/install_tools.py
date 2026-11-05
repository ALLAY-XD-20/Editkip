#!/usr/bin/env python3
"""Install/check tools for transcription and video analysis."""
import shutil, subprocess, sys

PKGS = ["faster-whisper", "scenedetect[opencv]", "psutil"]
for p in PKGS:
    print(f"pip install {p}")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", p])

missing = [b for b in ("ffmpeg", "ffprobe") if not shutil.which(b)]
if missing:
    print(f"MISSING: {missing}. Windows: winget install Gyan.FFmpeg | Mac: brew install ffmpeg")
    sys.exit(1)
print("All tools ready.")
