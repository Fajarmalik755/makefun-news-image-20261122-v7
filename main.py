#!/usr/bin/env python3
"""main.py - news-image-20261122 v7 entry point (standard library only).

Copies the pre-rendered entry.png into MAKEFUN_OUTPUT_DIR and verifies
the copy by SHA-256 and size, so a truncated or stale image fails loudly
instead of being submitted.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "90ef0cec9c9475bc6bccbc2fd4e25945e251a9512dd4f19de642cb8d0445a325"
EXPECTED_SIZE = 115998


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is not set")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) != EXPECTED_SIZE:
        fail("entry.png size %d, expected %d" % (len(data), EXPECTED_SIZE))
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        fail("entry.png sha256 %s, expected %s" % (digest, EXPECTED_SHA256))
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    with open(dest, "rb") as fh:
        copied = fh.read()
    copied_digest = hashlib.sha256(copied).hexdigest()
    if len(copied) != EXPECTED_SIZE or copied_digest != EXPECTED_SHA256:
        fail("copied entry.png failed verification (%s, %d bytes)"
             % (copied_digest, len(copied)))
    print("wrote %s (%d bytes, sha256 %s)" % (dest, len(copied), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
