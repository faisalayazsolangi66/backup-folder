#!/usr/bin/env python3
"""Back up a folder into a timestamped zip archive.

Zips a folder (recursively) into <name>_YYYY-MM-DD_HH-MM-SS.zip.
Hidden files can be skipped, and the archive itself is never
included in its own backup.
"""
import argparse
import os
import sys
import zipfile
from datetime import datetime


def make_name(source, output_dir, name):
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = name or os.path.basename(os.path.abspath(source.rstrip(os.sep)))
    if not base:
        base = "backup"
    return os.path.join(output_dir, f"{base}_{stamp}.zip")


def should_skip(rel_path, include_hidden):
    if include_hidden:
        return False
    parts = rel_path.split(os.sep)
    return any(part.startswith(".") for part in parts)


def backup(source, archive_path, include_hidden):
    count = 0
    total_bytes = 0
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for root, dirs, files in os.walk(source):
            # Keep hidden directories out of the walk unless requested.
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(".")]
            for name in sorted(files):
                full = os.path.join(root, name)
                rel = os.path.relpath(full, source)
                if should_skip(rel, include_hidden):
                    continue
                if os.path.abspath(full) == os.path.abspath(archive_path):
                    continue
                archive.write(full, rel)
                total_bytes += os.path.getsize(full)
                count += 1
    return count, total_bytes


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Back up a folder into a timestamped zip archive."
    )
    parser.add_argument("source", help="folder to back up")
    parser.add_argument("--output-dir", default=".",
                        help="folder to write the zip into (default: current folder)")
    parser.add_argument("--name", default=None,
                        help="base name for the zip (default: source folder name)")
    parser.add_argument("--include-hidden", action="store_true",
                        help="include hidden files and folders (default: skip them)")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.source):
        print(f"Not a folder: {args.source}", file=sys.stderr)
        return 1

    os.makedirs(args.output_dir, exist_ok=True)
    archive_path = make_name(args.source, args.output_dir, args.name)
    if os.path.exists(archive_path):
        print(f"Archive already exists: {archive_path}", file=sys.stderr)
        return 1

    try:
        count, total_bytes = backup(args.source, archive_path,
                                    args.include_hidden)
    except Exception as exc:
        print(f"Backup failed: {exc}", file=sys.stderr)
        return 1

    size_mb = os.path.getsize(archive_path) / (1024 * 1024)
    print(f"Backed up {count} file(s) ({total_bytes / 1024:.1f} KB) "
          f"from {args.source}")
    print(f"Archive: {archive_path} ({size_mb:.2f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
