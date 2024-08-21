#!/usr/bin/env python
# Extract and run fenced codeblocks from a markdown file

from argparse import ArgumentParser
from subprocess import run

parser = ArgumentParser(description="Extract fenced codeblocks from a markdown file")
parser.add_argument("input", help="Input markdown file")
parser.add_argument(
    "--sub",
    action="append",
    default=[],
    help="Substitute a string in the input file (string=replacement)",
)
parser.add_argument("--run", action="store_true", help="Run the code")

args = parser.parse_args()

code = []
inside_code = False
with open(args.input) as f:
    for line in f:
        if line.startswith("```"):
            inside_code = not inside_code
        elif inside_code:
            line = line.strip()
            for sub in args.sub:
                find, replace = sub.split("=", 1)
                line = line.replace(find, replace)
            code.append(line)

for c in code:
    print(f"Running {c}", flush=True)
    if args.run:
        run(c, shell=True, check=True)
