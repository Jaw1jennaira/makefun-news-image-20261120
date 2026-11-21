#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

The graded image is built ahead of time by render.py and shipped in this
repository as entry.png (1024x1024). Running this program places an exact
copy at the output path the harness asks for. It touches no network, keeps
no state, and writes identical bytes on every run, so the two grading runs
agree byte for byte.
"""
import os
import shutil
import sys


def entry_image_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "entry.png")


def output_path():
    return os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                        "entry.png")


def run():
    destination = output_path()
    parent = os.path.dirname(destination)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(entry_image_path(), destination)
    return 0


if __name__ == "__main__":
    sys.exit(run())
