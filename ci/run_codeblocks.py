#!/usr/bin/env python
# Extract and run fenced codeblocks from a markdown file
# Blocks must be marked with sh:
# ```sh
# Optionally add a prefix to retry N times if the block fails
# ```sh {retry=N}

from argparse import ArgumentParser
from os import getenv
import re
from subprocess import run, CalledProcessError

CI = getenv("CI") == "true"

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


def get_retries(lineno, line):
    assert line.startswith("```")
    codeblock_marker = line[3:].rstrip().split(maxsplit=1)
    if codeblock_marker[0] != "sh":
        raise ValueError(f"Line {lineno}: Only `sh` code blocks are supported: {line}")
    if len(codeblock_marker) > 1:
        m = re.match(r"\{retry=([0-9]+)\}", codeblock_marker[1])
        if m:
            return int(m.group(1))
        else:
            raise ValueError(f"Line {lineno}: Unable to parse sh metadata: {line}")
    return 0


scripts = []
inside_code = False
script = []
n = 0
with open(args.input) as f:
    for line in f:
        n += 1
        if line.startswith("```"):
            if inside_code:
                if line.rstrip() != "```":
                    raise ValueError(f"Line {n}: Unexpected closing block:{line}")
                scripts.append(("".join(script), retries))
                script = []
            else:
                retries = get_retries(n, line)
            inside_code = not inside_code
        elif inside_code:
            for sub in args.sub:
                find, replace = sub.split("=", 1)
                line = line.replace(find, replace)
            script.append(line)

if script:
    raise ValueError(f"Line {n}: Incomplete script: Missing closing ```")

for s, retries in scripts:
    if CI:
        firstline = s.strip().splitlines()[0]
        print(f"::group::{firstline}")

    print(f"Running\n```\n{s}\n```", flush=True)
    if args.run:
        for n in range(retries + 1):
            try:
                run(["bash", "-o", "errexit", "-o", "xtrace", "-c", s], check=True)
                break
            except CalledProcessError as e:
                if n == retries:
                    raise
                print(f"Failed exitcode={e.returncode}, retrying")

    if CI:
        print("::endgroup::")
