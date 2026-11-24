"""One Letter for Your Day -- entrypoint.

The brief: send exactly one character, a letter from A to Z, and
nothing else. The program writes that letter to entry.txt in the
output directory the harness provides (MAKEFUN_OUTPUT_DIR).

The letter is W. Behind it sits the word "wrecked": a day that
wrecked you. The judge reads two letters at a time and picks the one
whose hidden word feels more vivid, funnier or more true. Wrecked is
a sharp picture (a person flattened by their day), it lands at once
as a joke a reader repeats to a friend, and it is an honest report
of a grinding day -- and W is not one of the obvious, saturated
picks (Z for zero sleep, X for exhausted, U for unhinged), so the
letter stands on its own word instead of sharing a rate with
hundreds of identical entries.

The write is atomic (temporary file + rename) and verified by a
read-back, so the gate can never see a half-written entry.txt: the
file at the submitted path is either absent or exactly one byte.
"""

import os
import sys

LETTER = "W"
OUTPUT_NAME = "entry.txt"


def write_entry(letter: str, out_dir: str) -> str:
    """Atomically write exactly one A-Z character to entry.txt.

    Returns the path written. Raises ValueError unless the letter is
    a single character A-Z, and raises AssertionError unless the
    file read back is byte-for-byte that letter.
    """
    if len(letter) != 1 or not ("A" <= letter <= "Z"):
        raise ValueError("entry must be exactly one letter A-Z, got %r" % letter)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(letter)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)
    with open(path, "r", encoding="utf-8", newline="") as f:
        if f.read() != letter:
            raise AssertionError("entry.txt read-back mismatch")
    return path


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    write_entry(LETTER, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
