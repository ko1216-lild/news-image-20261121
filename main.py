#!/usr/bin/env python3
"""Entry program for the news-image-20261121 make.fun bounty.

The repository ships a pre-composed poster, entry.png, that sums up the
world news of Saturday 21 November 2026. This program delivers it to the
grader by copying it into the output directory as entry.png.
"""

import hashlib
import os
import shutil
from pathlib import Path

IMAGE_NAME = "entry.png"


def output_dir() -> Path:
    # Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output.
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    source = Path(__file__).resolve().parent / IMAGE_NAME
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME
    shutil.copyfile(source, target)
    # The grader runs this program twice and both runs must write the same
    # bytes, so verify the copy landed intact before reporting success.
    if digest(target) != digest(source):
        raise SystemExit(f"integrity check failed: {target} differs from {source}")


if __name__ == "__main__":
    main()
