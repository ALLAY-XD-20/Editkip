#!/usr/bin/env python3
"""Usage: transcribe.py <audio_or_video> [model=small] -> notes/transcript.json
Word-level timestamps (seconds), plus detected fillers and pauses."""
import json, sys
from pathlib import Path
from faster_whisper import WhisperModel

FILLERS = {"um", "uh", "umm", "uhh", "erm", "er", "ah", "hmm", "like", "basically", "actually", "literally"}
PAUSE = 0.35

src = sys.argv[1]
model = WhisperModel(sys.argv[2] if len(sys.argv) > 2 else "small", compute_type="int8")
segs, info = model.transcribe(src, word_timestamps=True, vad_filter=True)
words = [{"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
         for s in segs for w in s.words]
fillers = [w for w in words if w["w"].lower().strip(".,!?") in FILLERS]
pauses = [{"start": a["end"], "end": b["start"], "len": round(b["start"] - a["end"], 3)}
          for a, b in zip(words, words[1:]) if b["start"] - a["end"] > PAUSE]
Path("notes").mkdir(exist_ok=True)
Path("notes/transcript.json").write_text(json.dumps(
    {"language": info.language, "words": words, "fillers": fillers, "pauses": pauses},
    indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(words)} words, {len(fillers)} filler candidates, {len(pauses)} pauses > {PAUSE}s")
print("Review filler candidates: 'like'/'actually' may be real words in context.")
