#!/usr/bin/env -S uv run --script --
# /// script
# requires-python = "==3.12.*"
# ///

"""
    script to recursively convert all word docs (.docx) in a given
    input directory to markdown (.md) using pandoc.

    requires:
        - UV
        - docker

    example:
        ./to_md.py input_dir output_dir

    input_dir and output_dir must be provided relative to to_md.py
"""

import argparse
import pathlib
import os
import re
import subprocess


def process_directory(in_dir: str, out_dir: str, pattern: re.Pattern):
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    for entry in os.listdir(in_dir):
        in_rel_path = os.path.join(in_dir, entry)
        out_rel_path = os.path.join(out_dir, entry)
        if os.path.isdir(in_rel_path):
            process_directory(in_rel_path, out_rel_path, pattern)
        elif bool(re.search(pattern, entry)):
            print(f"{in_rel_path} -> {out_rel_path}.md")
            subprocess.run(f'docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/core {in_rel_path} -t gfm -o {out_rel_path}.md', shell=True)



parser = argparse.ArgumentParser()
parser.add_argument("input_directory")
parser.add_argument("output_directory")
parser.add_argument("input_extension")
args = parser.parse_args()

process_directory(
    args.input_directory,
    args.output_directory,
    re.compile(rf"\.{args.input_extension}$")
)
