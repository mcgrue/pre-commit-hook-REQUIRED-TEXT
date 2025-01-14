#!/usr/bin/env python

"""Checks each file in sys.argv for all strings submitted as arguments.  Ignores files and directories excluded by .gitignore."""

from __future__ import annotations

import os
import subprocess
import sys

debug_mode = False
# parse an optional command-line argument of --debug-mode
if len(sys.argv) > 1 and sys.argv[1] == "--debug-mode":
    print("Debug mode enabled")
    debug_mode = True
    sys.argv.pop(1)


# error if .pre-commit-hook-REQUIRED-TEXT is absent
if not os.path.exists(".pre-commit-hook-REQUIRED-TEXT"):
    print("Error: .pre-commit-hook-REQUIRED-TEXT file is absent", file=sys.stderr)
    print("====================================================", file=sys.stderr)
    print("1. create it", file=sys.stderr)
    print("2. add it to your .gitignore", file=sys.stderr)
    print("3. fill it with strings (newline delimited) that the commit hook will look for", file=sys.stderr)
    sys.exit(1)

# error if .pre-commit-hook-REQUIRED-TEXT is not in your .gitignore file
if not any(".pre-commit-hook-REQUIRED-TEXT" in line for line in open(".gitignore")):
    print("Error: .pre-commit-hook-REQUIRED-TEXT is not in your .gitignore file", file=sys.stderr)
    print("====================================================", file=sys.stderr)
    print("1. add it to your .gitignore", file=sys.stderr)
    sys.exit(1)

# error if .pre-commit-hook-REQUIRED-TEXT is empty
if os.stat(".pre-commit-hook-REQUIRED-TEXT").st_size == 0:
    print("Error: .pre-commit-hook-REQUIRED-TEXT file is empty", file=sys.stderr)
    print("====================================================", file=sys.stderr)
    print("1. add strings (newline delimited) that the commit hook will look for", file=sys.stderr)
    sys.exit(1)

needles = []

# read .pre-commit-hook-REQUIRED-TEXT file and put all strings in a list
with open(".pre-commit-hook-REQUIRED-TEXT") as f:
    needles = f.read().splitlines()

def err(s: str) -> None:
    print(s, file=sys.stderr)

for string in needles:
  command = ["git", "grep", "-Hn", "--no-index", "--exclude-standard", f"{string}"]
  if debug_mode:
    print(f"Running command: {' '.join(command)}")

  res = subprocess.run(command, capture_output=True)

  if res.returncode == 1:
      err(f"Error: The string '{string}' was NOT found!")
      err(res.stdout.decode("utf-8"))
      sys.exit(1)
  elif res.returncode == 2:
      err(f"Error invoking grep on {', '.join(sys.argv[1:])}:")
      err(res.stderr.decode("utf-8"))
      sys.exit(2)
  elif res.returncode != 0:
      err(f"Error: error finding '{string}'.  Exit code: {res.returncode}")
      sys.exit(res.returncode)
  
  if debug_mode:
    print("found string: ", string)

if debug_mode:
  err("\nfound all the strings\n")
  
sys.exit(0)

