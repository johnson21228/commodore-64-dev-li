#!/usr/bin/env python3
"""Clean generated LI/workbench artifacts before packing.

This script is intentionally conservative: it removes common overlay application
cruft and stale generated history artifacts, while preserving source files,
tracked workbench content, and the newest repo-history artifact.
"""
from pathlib import Path
import shutil

ROOT = Path('.')

# Fixed overlay/cruft directory names used by older overlays/templates.
REMOVE_DIR_NAMES = {
    'overlay',
    'files',
    '__MACOSX',
}

# Directory glob patterns for repo-specific overlay unpack folders.
# Examples: josh_copilot_token_burn_overlay/, foo_overlay_v2/
REMOVE_DIR_GLOBS = [
    '*_overlay',
    '*_overlay_v*',
]

REMOVE_FILE_GLOBS = [
    'apply_*_overlay.py',
    'apply_*_overlay_*.py',
    '*_overlay.zip',
    '*_overlay_v*.zip',
    '.DS_Store',
    '**/.DS_Store',
]


def remove_dir(path: Path) -> None:
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
        print(f'Removed directory {path}')


def remove_file(path: Path) -> None:
    if path.exists() and path.is_file():
        path.unlink()
        print(f'Removed file {path}')


for name in sorted(REMOVE_DIR_NAMES):
    remove_dir(ROOT / name)

for pattern in REMOVE_DIR_GLOBS:
    for path in sorted(ROOT.glob(pattern)):
        if path.is_dir() and path.name not in {'.git', 'dist', 'outputs'}:
            remove_dir(path)

for pattern in REMOVE_FILE_GLOBS:
    for path in sorted(ROOT.glob(pattern)):
        remove_file(path)

history_dir = ROOT / 'outputs' / 'history'
if history_dir.exists():
    histories = sorted(
        history_dir.glob('repo_history_for_llm_*.md'),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for old in histories[1:]:
        old.unlink()
        print(f'Removed stale history {old}')

print('LI cleanup complete.')
