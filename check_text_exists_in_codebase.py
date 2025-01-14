#!/usr/bin/env python

"""Checks each file in sys.argv for all strings submitted as arguments.  Ignores files and directories excluded by .gitignore."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description='strings required in the codebase to pass')
parser.add_argument('required_text', nargs='+', help='required strings')
args = parser.parse_args()

if len(args.required_text) == 0:
    print('Error: No required strings provided', file=sys.stderr)
    sys.exit(1)

def err(s: str) -> None:
    print(s, file=sys.stderr)

for string in args.required_text:
  command = ["git", "grep", "-Hn", "--no-index", "--exclude-standard", f"{string}", *sys.argv[1:]]
  print(f"Running command: {' '.join(command)}")

  res = subprocess.run(command, capture_output=True)

  if res.returncode == 1:
      err('Error: The string f"{string}" was NOT found!')
      err(res.stdout.decode("utf-8"))
      sys.exit(1)
  elif res.returncode == 2:
      err(f"Error invoking grep on {', '.join(sys.argv[1:])}:")
      err(res.stderr.decode("utf-8"))
      sys.exit(2)
  elif res.returncode != 0:
      err(f"Error: error finding '{string}'.  Exit code: {res.returncode}")
      sys.exit(res.returncode)
  
  print("found string: ", string)

err("\nfound all the strings\n")
sys.exit(0)

