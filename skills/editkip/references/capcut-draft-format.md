# CapCut draft format notes

Formats differ between CapCut versions. Treat this as a map and confirm against
the real file. Safest technique: **clone an existing segment/material from the
same project and modify the clone** instead of building entries from scratch.

## Location

Projects live in a `com.lveditor.draft` folder (path in `notes/capcut-path.txt`).
Each project subfolder typically has `draft_content.json` (or `draft_info.json`
in some versions), `draft_meta_info.json` and cache/resource folders;
`root_meta_info.json` in the parent lists projects.
Windows default: `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft`
Mac default: `~/Movies/CapCut/User Data/Projects/com.lveditor.draft`

If the main draft file doesn't parse as JSON it is probably encrypted. Stop
(SKILL.md rule 5).

## Units

- Time is in **microseconds** (1 s = 1,000,000). Ranges: `{"start": int, "duration": int}`.
- `target_timerange` = position on the timeline; `source_timerange` = slice of source media.
- Canvas size: `canvas_config.width` / `height`.

## Structure (typical)

```
duration, fps, canvas_config
materials: videos[], audios[], texts[], effects[], speeds[], canvases[],
           sound_channel_mappings[], material_animations[], ...
tracks[]: {id, type: "video"|"audio"|"text"|"effect"|..., segments[]}
segment: {id, material_id, target_timerange, source_timerange, speed, volume,
          clip{transform{x,y}, scale{x,y}, rotation, alpha},
          common_keyframes[], extra_material_refs[], render_index, ...}
```

Keep the file valid:
- Every `segment.material_id` and id in `extra_material_refs` must exist in
  `materials`. Clone the speed/canvas/channel-mapping helper materials the
  way existing segments reference them, with new ids.
- Ids are unique UUID strings, matching the file's casing.
- Segments in one track must not overlap and must be sorted by start.
- Update the draft's total `duration` to the end of the last segment.
- Images are `videos[]` materials with `type: "photo"`.
- Imported media: add a material with an absolute `path`, and fill
  `duration`, `width`, `height` like an existing one.
- Write UTF-8 without BOM.

## Keyframes (zoom)

Per segment, `common_keyframes` holds one entry per property, e.g.
`property_type: "KFTypeScaleX"` and `"KFTypeScaleY"`, each with a
`keyframe_list` of `{time_offset, values:[scale]}` (microseconds from segment
start). Zoom in = 1.0 -> ~1.06 across the segment; zoom out = 1.06 -> 1.0;
alternate per image. If the project already has keyframes, copy their exact
structure (curve/handle fields). Property names vary by version; match the file.

## Safe frame for text

`clip.transform.x/y` are normalized (-1..1, centre 0; check an existing text
segment for the y direction). Keep the text centre within |x| <= 0.9 and
|y| <= 0.9, and size/wrap text so its box (about chars * 0.55 * font size px
wide) fits within 90% of canvas width. For 9:16 video keep captions in the
middle-lower third, away from platform UI at the very top/bottom.

## Audio

Music track `volume` ~0.08-0.15 under voice (about -22 to -26 dB) plus
fades if the version has them. SFX on a separate track, volume 0.4-0.8.
