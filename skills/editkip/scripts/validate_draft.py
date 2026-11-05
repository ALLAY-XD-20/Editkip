#!/usr/bin/env python3
"""Usage: validate_draft.py <project> -> checks the draft JSON is sane. Exit 1 on errors."""
import json, sys
from pathlib import Path

name = sys.argv[1] if len(sys.argv) > 1 else "auto_edit"
proj = Path(Path("notes/capcut-path.txt").read_text(encoding="utf-8").strip()) / name
f = next((proj / n for n in ("draft_content.json", "draft_info.json") if (proj / n).exists()), None)
if not f:
    sys.exit("No draft_content.json / draft_info.json found")
try:
    d = json.loads(f.read_text(encoding="utf-8"))
except Exception as e:
    sys.exit(f"Not readable JSON (probably encrypted): {e}")

errs = []
mats = d.get("materials", {})
ids = {m.get("id") for lst in mats.values() if isinstance(lst, list) for m in lst if isinstance(m, dict)}
seen, end_max = set(), 0
W = d.get("canvas_config", {}).get("width")

for t in d.get("tracks", []):
    last_end = 0
    segs = t.get("segments", [])
    for s in segs:
        sid = s.get("id")
        if sid in seen:
            errs.append(f"duplicate segment id {sid}")
        seen.add(sid)
        tr = s.get("target_timerange", {})
        st, du = tr.get("start", 0), tr.get("duration", 0)
        if du <= 0:
            errs.append(f"{sid}: non-positive duration")
        if st < last_end:
            errs.append(f"{t.get('type')} track overlap/unsorted at {st}")
        last_end = max(last_end, st + du)
        for ref in [s.get("material_id")] + list(s.get("extra_material_refs", [])):
            if ref and ref not in ids:
                errs.append(f"{sid}: missing material {ref}")
        if t.get("type") == "text":
            tf = s.get("clip", {}).get("transform", {})
            if abs(tf.get("x", 0)) > 0.9 or abs(tf.get("y", 0)) > 0.9:
                errs.append(f"{sid}: text outside safe frame (x={tf.get('x')}, y={tf.get('y')})")
    end_max = max(end_max, last_end)

if end_max > d.get("duration", 0):
    errs.append(f"draft duration {d.get('duration')} < last segment end {end_max}")
if errs:
    print("\n".join(errs[:50]))
    sys.exit(1)
print(f"OK: {len(d.get('tracks', []))} tracks, duration {end_max / 1e6:.1f}s")
