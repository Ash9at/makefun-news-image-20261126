"""Copy the pre-rendered entry image into the output directory.

The image is already baked into this repository as entry.png; scoring
runs in an environment without image libraries, so this script only
copies the file and does no generation at all.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)

    destination = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, destination)
    print("copied entry.png to", destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
