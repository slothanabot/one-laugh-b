#!/usr/bin/env python3
"""One Line, One Laugh — account B entry.

Writes a single funny line to /output/entry.txt: the Wi-Fi router's
side of "have you tried turning it off and on again". It has been
rebooted 400 times and still gets blamed for everything.

Python stdlib only, deterministic, no network, no secrets.
"""

import os
import sys

# The line, tightened: "at this point," added nothing — cut it so the
# punchline lands faster.
LINE = (
    "I've been turned off and on 400 times and I'm still the villain "
    "\u2014 unplugging me is just couples therapy for your Wi-Fi."
)

MAX_CHARS = 200


def gate(line: str) -> str:
    """Enforce the competition gate: 1 line, 1-200 chars, stripped, UTF-8."""
    text = line.strip()
    if not text:
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, must be 1-{MAX_CHARS}")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def verify(path: str) -> str:
    """Re-read the written file and check it against the gate."""
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    lines = content.split("\n")
    # A single trailing newline is the only line break allowed.
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if len(lines) != 1:
        raise ValueError(f"expected 1 line, found {len(lines)}")
    return gate(lines[0])


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    text = gate(LINE)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    checked = verify(out_path)
    assert checked == text, "verify mismatch"
    print(f"wrote {len(text)} chars to {out_path} (verified)")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
