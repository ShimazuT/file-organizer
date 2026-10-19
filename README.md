# File Organizer

A small Python script that cleans up a messy folder (like `~/Downloads`) by moving
files into subfolders by type: Images, Documents, Videos, Archives, and more.

## Features
- Sorts files by extension into category folders
- `--dry-run` mode to preview changes safely
- Never overwrites: duplicates become `name (1).ext`
- Skips folders, hidden files, and unfinished downloads (`.part`, `.crdownload`)
- No dependencies, only the Python standard library

## Usage
```bash
python3 organizer.py --dry-run        # preview
python3 organizer.py                  # organize ~/Downloads
python3 organizer.py ~/Desktop        # organize another folder
```

## Customize
Edit the `CATEGORIES` dictionary at the top of `organizer.py` to add your own
extensions or categories.

## Requirements
Python 3.8+ (tested on Linux).

## License
MIT
