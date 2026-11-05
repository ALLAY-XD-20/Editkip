# Editkip

AI video-editing workspace and auto-editor for **CapCut desktop** (Windows/Mac), built as an
[Antigravity](https://antigravity.google) skill with slash commands.

Editkip sets up a workspace, learns the editing style of your reference videos, then edits a
CapCut project by writing its draft files directly. No computer-use and CapCut is never launched.
You export the final video from CapCut yourself.

## Commands

| Command | What it does |
|---|---|
| `/editkip-setup` | Creates `reference/ assets/ sfx/ music/ fonts/ notes/ backups/`, finds CapCut's project folder, installs transcription/analysis tools, adds starter SFX/music, writes a README |
| `/editkip-edit <project>` | Backs up the project, writes `notes/style-guide.md` from your references, transcribes the voiceover (word-level), cuts pauses/fillers, times visuals, adds gentle zooms, SFX, low music and in-frame text |

## Requirements

- CapCut desktop installed, and **closed** while Editkip edits
- Python 3.9+ and ffmpeg (`winget install Gyan.FFmpeg` / `brew install ffmpeg`)

## Install (one command)

```bash
npx github:ALLAY-XD-20/Editkip
```

Once published to npm, it's just:

```bash
npx editkip
```

That installs Editkip **globally** into every agent it finds: Antigravity (`~/.gemini/antigravity`)
and Claude Code (`~/.claude`). Then open any workspace folder and run `/editkip-setup`.

| Option | Effect |
|---|---|
| `--agent antigravity\|claude\|all` | Pick the agent(s) instead of auto-detecting |
| `--workspace [dir]` | Install into one workspace (`.agent/` and `.claude/`) instead of globally |
| `--uninstall` | Remove Editkip |

Requires Node 16.7+.

## Notes

- Newer CapCut versions may encrypt the draft file. If it isn't readable JSON, Editkip stops and tells you.
- Every edit is preceded by a backup in `backups/` and followed by a validation pass.
- Starter SFX/music are only downloaded from sources with a verifiable free license.

## Publishing to npm (maintainer)

```bash
npm view editkip          # check the name is free; if taken, rename in package.json (e.g. @allay-xd-20/editkip)
npm login
npm publish               # add --access public if scoped
```
