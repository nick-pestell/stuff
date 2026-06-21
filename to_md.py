#!/usr/bin/env -S uv run --script --
# /// script
# requires-python = "==3.12.*"
# ///

"""
    script to recursively search an input directory for documents of a given
    extension and convert to markdown (.md) using pandoc.

    requires:
        - UV
        - docker

    example:
        ./to_md.py <dir_to_process> docx
"""


import argparse
import pathlib
import os
import re
import subprocess


def process_directory(indir: str, data_parent_dir: str, pattern: re.Pattern, outdir_rel: str):
    for entry in os.listdir(indir):
        in_abs = os.path.join(indir, entry)
        out_rel = os.path.join(outdir_rel, entry)
        if os.path.isdir(in_abs):
            process_directory(in_abs, data_parent_dir, pattern, out_rel)
        elif bool(re.search(pattern, entry)):
            print(f"{entry} -> {entry}.md")
            cmd = f'docker run --rm --volume "{data_parent_dir}:/data" --user `id -u`:`id -g` pandoc/core {os.path.relpath(in_abs, data_parent_dir)} -t gfm -o {out_rel}.md'
            subprocess.run(cmd, shell=True)
            print()



parser = argparse.ArgumentParser()
parser.add_argument("indir")
parser.add_argument("input_extension")
parser.add_argument("--outdir_rel", default="output")
args = parser.parse_args()

pathlib.Path(
        os.path.join(
            os.path.dirname(args.indir),
            args.outdir_rel
        )
).mkdir(parents=True, exist_ok=True)

process_directory(
    args.indir,
    args.indir,
    re.compile(rf"\.{args.input_extension}$"),
    args.outdir_rel
)
