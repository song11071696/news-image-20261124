#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261124.

Copies the pre-rendered front-page image ``entry.png`` (1024x1024,
built in-session from 37 verified 24 November 2026 news stories) to
the output directory as ``entry.png``.

Standard library only, no network, deterministic: the same bytes are
written on every run.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard against a partial copy: the output must be byte-identical
    # to the bundled image, so the two grader runs always agree.
    if _sha256(src) != _sha256(dst):
        raise SystemExit("entry.png copy failed verification")
    print("wrote %s" % dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
