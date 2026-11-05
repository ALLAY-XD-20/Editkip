# /editkip-setup

Set up the current folder as the user's AI video editing workspace.

## Steps

1. **Folders.** Create (skip any that exist):
   `reference`, `assets`, `sfx`, `music`, `fonts`, `notes`, `backups`.
   Do NOT create `output`. The final export happens in CapCut.

2. **CapCut path.** Run `python scripts/find_capcut_path.py`. It writes the
   projects folder to `notes/capcut-path.txt`. If nothing is found or the
   location isn't accessible, ask the user for the path or for access.

3. **Tools.** Run `python scripts/install_tools.py`. It installs/checks the
   Python packages `faster-whisper`, `scenedetect[opencv]`, `psutil` and the
   `ffmpeg`/`ffprobe` binaries. If ffmpeg is missing, tell the user how to
   install it (Windows: `winget install Gyan.FFmpeg`; Mac: `brew install ffmpeg`)
   rather than failing silently.

4. **Starter packs (only if you can do it legitimately).** Try to add a few
   royalty-free SFX (whoosh, pop, click, ding) to `sfx/` and 2-3 royalty-free
   tracks to `music/`. Use only sources with clear free licenses (CC0 or
   Pixabay/Freesound CC0 items) and record source + license in
   `notes/licenses.md`. If there is no network access or no verifiable
   license, skip this and say so. Never fabricate audio files. As a fallback,
   offer to synthesize simple placeholder SFX with ffmpeg and label them
   as placeholders.

5. **README.md.** Explain what goes in each folder (layout in SKILL.md),
   how to run `/editkip-setup` and `/editkip-edit <project>`, and that CapCut
   must be closed while editing.

6. **Finish.** Tell the user in one or two lines what was created and to add
   their reference videos to `reference/`.
