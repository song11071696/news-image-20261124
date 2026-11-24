#!/usr/bin/env python3
"""news-image-20261124 entry program.

A pure-stdlib, deterministic copier. The entry image is the
``entry.png`` that ships beside this file in the repository: a
1024x1024 front page summing up the world's news of Tuesday
24 November 2026 in 37 stories across 7 regions.

Running it copies that image, byte for byte, to
``<output>/entry.png`` and writes a small deterministic build
report beside it as ``build-report.txt``. It makes no network
calls, reads no clock and writes no timestamps, so two runs
over the same repository produce identical outputs.

Usage (outside the grader's container)::

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Inside the grader the output directory defaults to ``/output``.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

ENTRY_DATE = "2026-11-24"
STORY_COUNT = 37
REGION_COUNT = 7
SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
REPORT_NAME = "build-report.txt"


def sha256_of(path):
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def output_dir():
    """Return the output directory, honouring MAKEFUN_OUTPUT_DIR."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if raw.strip():
        return Path(raw)
    return Path("/output")


def build_report(source_path, source_digest, source_size,
                 output_digest):
    """Build the deterministic text of the build report."""
    lines = [
        "news-image-20261124 build report",
        "entry date: " + ENTRY_DATE,
        "stories: " + str(STORY_COUNT),
        "regions: " + str(REGION_COUNT),
        "source: " + SOURCE_NAME,
        "source size (bytes): " + str(source_size),
        "source sha256: " + source_digest,
        "output: " + OUTPUT_NAME,
        "output sha256: " + output_digest,
        "match: " + str(source_digest == output_digest),
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    """Copy entry.png to the output directory and write the report."""
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print("error: %s not found beside main.py" % SOURCE_NAME,
              file=sys.stderr)
        return 1

    source_digest = sha256_of(source)
    source_size = source.stat().st_size

    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / OUTPUT_NAME
    shutil.copyfile(source, target)

    output_digest = sha256_of(target)
    if output_digest != source_digest:
        print("error: copied file digest does not match source",
              file=sys.stderr)
        return 1

    report = build_report(source, source_digest, source_size,
                          output_digest)
    (target_dir / REPORT_NAME).write_text(report, encoding="utf-8")

    print("news-image-%s: wrote %s (%d bytes, sha256 %s)"
          % (ENTRY_DATE.replace("-", ""), target, source_size,
             source_digest))
    print("build report: %s" % (target_dir / REPORT_NAME))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
