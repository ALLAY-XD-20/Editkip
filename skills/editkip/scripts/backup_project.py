#!/usr/bin/env python3
"""Usage: backup_project.py <project> -> copies it to backups/<project>_<timestamp>/"""
import shutil, sys, time
from pathlib import Path

name = sys.argv[1] if len(sys.argv) > 1 else "auto_edit"
root = Path(Path("notes/capcut-path.txt").read_text(encoding="utf-8").strip())
src = root / name
if not src.is_dir():
    sys.exit(f"Project not found: {src}")
dst = Path("backups") / f"{name}_{time.strftime('%Y%m%d_%H%M%S')}"
shutil.copytree(src, dst)
print(f"Backed up to {dst}")
