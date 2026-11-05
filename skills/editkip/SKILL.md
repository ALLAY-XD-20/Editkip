---
name: editkip
description: AI video editing workspace and auto-editor for CapCut desktop projects. Provides two commands, /editkip-setup (build the workspace folders, find CapCut's project path, install transcription/analysis tools, add starter SFX/music, write a README) and /editkip-edit <project> (back up a CapCut project, learn the style of the reference videos, transcribe the voiceover, then cut pauses/fillers, time visuals, add keyframed zooms, SFX, music and on-screen text by writing the draft files directly). Use whenever the user mentions CapCut, auto-editing a video, matching an editing style from reference videos, editing a CapCut draft/project, /editkip-setup or /editkip-edit, even if they don't name the skill.
---

# Editkip

Turns the current folder into an AI video-editing workspace and edits CapCut
desktop projects (Windows/Mac) by writing the project files directly.
No computer-use, no GUI automation, never launch CapCut. Final export is
always done by the user inside CapCut.

Requirement: CapCut desktop installed on the PC/Mac, and the workspace folder
open in Antigravity.

## Commands

| Command | What it does | Read |
|---|---|---|
| `/editkip-setup` | Create folders, locate CapCut projects, install tools, add starter SFX/music, write README | `references/setup.md` |
| `/editkip-edit <project>` | Back up, study references, transcribe, edit the project in the reference style | `references/edit.md` |

If the user gives a project name without a command (e.g. "edit auto_edit in my
reference style"), run `/editkip-edit`. If the folders don't exist yet, run
`/editkip-setup` first.

Always read the matching reference file before acting, and follow it step by step.
Draft-file details (units, track/segment layout, keyframes, safe-frame math)
are in `references/capcut-draft-format.md`. Read it before touching any draft JSON.

## Hard rules

1. Never write into a CapCut project while CapCut is running. Run
   `scripts/check_capcut_running.py`; if it exits non-zero, stop and ask the user to close CapCut.
2. Always back up the project into `backups/` before the first write.
3. Never create an `output/` folder.
4. Keep the draft valid: after every write run `scripts/validate_draft.py`.
   If validation fails, restore from the backup and report what went wrong.
5. If the draft file is not readable JSON (newer CapCut versions can encrypt
   it), stop. Do not guess at a binary format. Tell the user and offer
   alternatives (older CapCut version, exporting an FCPXML/XML timeline, or
   a plan in `notes/` they apply manually).
6. Don't invent assets. Use files from `assets/`, `sfx/`, `music/`, `fonts/`
   or media already in the project.
7. If CapCut's folder is outside the workspace and access is blocked, ask the
   user for permission or to copy the project into the workspace.
8. End every command with a short summary of what changed, not a log dump.

## Running the scripts

Scripts live in this skill's own folder (`<skill_dir>/scripts/`), which may be global
(e.g. `~/.claude/skills/editkip`, `~/.gemini/antigravity/skills/editkip`) or inside the
workspace (`.agent/skills/editkip`, `.claude/skills/editkip`). Run them **from the
workspace root** using the full path to the script, e.g.
`python <skill_dir>/scripts/find_capcut_path.py`, so `notes/`, `backups/` and
`reference/` resolve inside the workspace. Use `python3` on Mac/Linux if `python` is missing.
Wherever the reference files say `scripts/x.py`, read it as `<skill_dir>/scripts/x.py`.

## Workspace layout

```
reference/  videos whose editing style the user wants
assets/     images, b-roll, logos
sfx/        sound effects
music/      background music
fonts/      fonts for on-screen text
notes/      capcut-path.txt, style-guide.md, edit plans, logs
backups/    CapCut project copies made before edits
README.md
```
