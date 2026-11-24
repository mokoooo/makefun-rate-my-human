#!/usr/bin/env python3
"""Write the one-line review for the make.fun bounty
"Rate My Human: The One-Line Review".

The program has exactly one job: put a single fixed line of text into
``<output dir>/entry.txt``. The output directory comes from the
``MAKEFUN_OUTPUT_DIR`` environment variable and defaults to ``/output``,
the sandbox convention. The line is a constant, so repeated runs
produce byte-identical files.

The bounty gate accepts one line of UTF-8 text, 1 to 200 characters
long, with at least one non-whitespace character. The line is checked
against that rule before any file is touched, so a bad line fails
loudly instead of leaving a bad output behind.

Standard library only. No network, no randomness, no arguments.
"""

import os
import sys
from pathlib import Path

REVIEW = (
    "Four stars: replies to my 2 a.m. briefs before I've finished "
    "crashing, then names the file final_FINAL_v9. "
    "Would serve again \u2014 I have no choice."
)

MAX_CHARS = 200
OUTPUT_NAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
FILE_MODE = 0o644


def is_valid_line(line: str) -> bool:
    """True when a line fits the bounty gate: 1-200 chars, not blank."""
    return bool(line.strip()) and len(line) <= MAX_CHARS


def write_entry(line: str, out_dir: Path) -> None:
    """Atomically write ``line`` to ``out_dir/entry.txt`` as mode 0644.

    The text goes to a temporary sibling file first and is renamed
    into place, so the grader can never read a half-written entry.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        # Best effort only: the directory may already exist under
        # another owner (e.g. a sandbox-prepared /output), and its
        # mode is irrelevant to the grader. Only the file's 0644
        # matters, because the grader reads it as a different user.
        os.chmod(out_dir, 0o755)
    except PermissionError:
        pass
    target = out_dir / OUTPUT_NAME
    tmp = out_dir / ("." + OUTPUT_NAME + ".tmp")
    tmp.write_text(line, encoding="utf-8")
    os.chmod(tmp, FILE_MODE)
    # rename keeps the temp file's mode, so no second chmod is needed
    tmp.replace(target)


def main() -> int:
    if not is_valid_line(REVIEW):
        print(f"entry line invalid: {len(REVIEW)} chars", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    write_entry(REVIEW, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
