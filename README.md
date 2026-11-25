# Backup Folder

Back up a folder into a timestamped zip archive, for example `photos_2026-11-25_10-30-00.zip`. Hidden files and folders are skipped by default.

## Requirements

- Python 3 (standard library only — no `requirements.txt`)

## How to run

```bash
python3 main.py --help
python3 main.py ~/Documents/photos --output-dir ~/backups
```

Options:

- `--output-dir` — folder to write the zip into (default: current folder)
- `--name` — base name for the zip (default: source folder name)
- `--include-hidden` — include hidden files and folders

## Example

```bash
$ python3 main.py photos --output-dir backups/
Backed up 12 file(s) (2048.0 KB) from photos
Archive: backups/photos_2026-11-25_10-30-00.zip (1.85 MB)
```
