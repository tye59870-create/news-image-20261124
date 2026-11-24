#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261124.

Decodes the bundled front-page image (entry.png.b64: base64 of the
1024x1024 PNG rendered by build_image.py) and writes it to
/output/entry.png. Standard library only; no network access;
deterministic: every run writes identical bytes.
"""
import base64
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png.b64"
DST = Path("/output/entry.png")


def main() -> None:
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_bytes(base64.b64decode(SRC.read_text().strip()))
    digest = hashlib.sha256(DST.read_bytes()).hexdigest()
    print(f"wrote {DST} ({DST.stat().st_size} bytes, sha256={digest})")


if __name__ == "__main__":
    main()
