#!/usr/bin/env python3
"""Exit 0 if CapCut is NOT running, 1 if it is."""
import platform, subprocess, sys

def running():
    s = platform.system()
    if s == "Windows":
        out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
        return any(n in out for n in ("capcut.exe", "capcutbrowser.exe", "jianyingpro.exe"))
    out = subprocess.run(["ps", "-A", "-o", "comm"], capture_output=True, text=True).stdout.lower()
    return "capcut" in out

if running():
    print("CapCut is running. Ask the user to close it, then retry.")
    sys.exit(1)
print("CapCut is not running.")
