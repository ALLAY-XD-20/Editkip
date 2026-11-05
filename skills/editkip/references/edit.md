# /editkip-edit <project>

Default project name: `auto_edit`.

## 0. Preconditions

- Workspace exists (folders + `notes/capcut-path.txt`). If not, run setup first.
- Run `python scripts/check_capcut_running.py`. If it reports CapCut running,
  STOP and ask the user to close it. Do not continue until they confirm.
- Read `references/capcut-draft-format.md`.

## 1. Back up

`python scripts/backup_project.py <project>` copies the whole project folder to
`backups/<project>_<timestamp>/`. Confirm the copy exists before going on.

## 2. Study the reference videos

- `python scripts/analyze_reference.py` -> `notes/reference-analysis.json`
  and extracted frames in `notes/frames/<video>/`.
- View the frames and stats, then write `notes/style-guide.md` covering:
  pacing (average shot length, cuts/min), zoom behaviour (amount, direction,
  easing), text style (font, size, position, animation, frequency), SFX
  (type, and where: cuts, text pops, transitions), music (genre, level
  under voice), transitions, colour/look. Mark anything inferred from frames
  as an estimate.
- If `reference/` is empty, stop and ask the user to add videos.

## 3. Transcribe

`python scripts/transcribe.py <voiceover file>` -> `notes/transcript.json`
with word-level timestamps, detected filler words and pauses.
Find the voiceover among the project's audio materials (see the draft format
reference) or ask the user which file it is.

## 4. Plan

Write a brief `notes/edit-plan.md`: cut list (pauses > ~0.35 s trimmed,
fillers removed), which image/b-roll goes where with word-anchored times,
SFX placements, music choice, text overlays. Then execute.

## 5. Edit (write the draft files directly)

- **Cuts:** remove long pauses and filler words (um, uh, like, you know...)
  by splitting/trimming voiceover segments and ripple-shifting everything
  downstream so audio and visuals stay in sync. Keep ~80-120 ms of padding
  at cut points so words aren't clipped.
- **Visual timing:** each image/b-roll starts on the word it illustrates
  (word timestamps). Use `assets/` or media already in the project.
- **Zoom:** every image gets a very gentle keyframed scale, alternating
  in (100% -> ~106%) and out (~106% -> 100%) across consecutive images.
- **Audio:** SFX from `sfx/` on cuts, text pops and transitions, never
  constant or stacked. Music from `music/` on its own track, low under the
  voice (about -22 to -26 dB relative to voice), with fade in/out.
- **Text:** add on-screen text where it helps (key terms, numbers, hooks).
  Every text element must sit fully inside the frame with margin
  (safe-frame math in the draft format reference). Use a font already in the
  project unless you can register a font from `fonts/` the way the draft expects.
- **Validity:** run `python scripts/validate_draft.py <project>` after writing.
  Fix errors; if you can't, restore the backup and tell the user.

Do not launch CapCut and do not use computer use.

## 6. Finish

Log changes to `notes/edit-log.md` and reply with a short summary: what was
cut (counts/time saved), how many visuals/SFX/text items were added, music
used, limitations, and where the backup is. Remind the user to open the
project in CapCut, review, and export there.
