"""Entry point: write the 26 November 2026 news image to /output/entry.png."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen import build


def main():
    out = os.environ.get("OUTPUT_PATH", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = build()
    img.save(out, format="PNG")


if __name__ == "__main__":
    main()
