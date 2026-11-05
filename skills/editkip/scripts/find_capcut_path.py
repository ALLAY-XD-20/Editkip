#!/usr/bin/env python3
"""Locate CapCut's projects folder and save it to notes/capcut-path.txt (run from workspace root)."""
import os, platform, sys
from pathlib import Path

def candidates():
    h, s = Path.home(), platform.system()
    if s == "Windows":
        local = Path(os.environ.get("LOCALAPPDATA", h / "AppData" / "Local"))
        yield local / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
        yield local / "CapCut" / "Apps"  # fallback search root
    elif s == "Darwin":
        yield h / "Movies" / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
        yield h / "Movies" / "CapCut"
    else:
        yield h / ".config" / "CapCut"

def find():
    for c in candidates():
        if c.name == "com.lveditor.draft" and c.exists():
            return c
    for c in candidates():
        if c.exists():
            for p in c.rglob("com.lveditor.draft"):
                return p
    return None

if __name__ == "__main__":
    p = find()
    if not p:
        print("NOT FOUND: ask the user for the CapCut projects folder path.")
        sys.exit(1)
    Path("notes").mkdir(exist_ok=True)
    Path("notes/capcut-path.txt").write_text(str(p), encoding="utf-8")
    print(f"CapCut projects: {p}")
    print("Projects:", [d.name for d in p.iterdir() if d.is_dir()][:50])
