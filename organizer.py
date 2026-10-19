#!/usr/bin/env python3
"""File Organizer: sorts files in a folder (default: ~/Downloads) into
subfolders by file type (Images, Documents, Videos, ...).

Usage:
    python3 organizer.py --dry-run      # preview only, nothing is moved
    python3 organizer.py                # organize ~/Downloads
    python3 organizer.py /path/to/dir   # organize another folder
"""

import argparse
import shutil
import sys
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".odt", ".txt", ".rtf", ".md", ".epub"},
    "Spreadsheets": {".xls", ".xlsx", ".ods", ".csv"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv"},
    "Audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"},
    "Archives": {".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar", ".tgz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".c", ".cpp", ".h", ".java", ".ino", ".sh", ".json", ".yml", ".yaml"},
    "Installers": {".deb", ".rpm", ".appimage", ".iso", ".flatpakref", ".snap"},
}
OTHER = "Other"

# Files still being downloaded: never touch these.
PARTIAL_SUFFIXES = {".part", ".crdownload", ".download", ".tmp"}


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    for name, extensions in CATEGORIES.items():
        if ext in extensions:
            return name
    return OTHER


def unique_destination(dest: Path) -> Path:
    """If dest exists, return 'name (1).ext', 'name (2).ext', ... instead."""
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({counter}){dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, dry_run: bool = False) -> int:
    moved = 0
    for item in sorted(folder.iterdir()):
        # Skip folders, hidden files and partial downloads.
        if not item.is_file() or item.name.startswith("."):
            continue
        if item.suffix.lower() in PARTIAL_SUFFIXES:
            continue

        category = category_for(item)
        target_dir = folder / category
        destination = unique_destination(target_dir / item.name)

        print(f"{'[dry-run] ' if dry_run else ''}{item.name}  ->  {category}/{destination.name}")
        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
        moved += 1
    return moved


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize a folder by file type.")
    parser.add_argument("folder", nargs="?", default=str(Path.home() / "Downloads"),
                        help="folder to organize (default: ~/Downloads)")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="show what would happen without moving anything")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        sys.exit(f"Error: '{folder}' is not a folder.")

    count = organize(folder, args.dry_run)
    verb = "would be moved" if args.dry_run else "moved"
    print(f"\nDone: {count} file(s) {verb} in {folder}")


if __name__ == "__main__":
    main()
