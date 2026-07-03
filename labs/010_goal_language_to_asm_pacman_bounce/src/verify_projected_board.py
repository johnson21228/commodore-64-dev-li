#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
BOARD_PATH = SRC / "board.txt"
META_PATH = SRC / "projected_board.json"

ALLOWED = set("#.o PGX")
TRAVERSABLE = set(".o PG")

def load_board() -> list[str]:
    if not BOARD_PATH.exists():
        raise AssertionError(f"missing board file: {BOARD_PATH}")
    rows = BOARD_PATH.read_text().splitlines()
    if not rows:
        raise AssertionError("board.txt is empty")
    return rows

def load_meta() -> dict:
    if not META_PATH.exists():
        raise AssertionError(f"missing projected board metadata: {META_PATH}")
    return json.loads(META_PATH.read_text())

def neighbors(x: int, y: int, rows: list[str]):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(rows) and 0 <= nx < len(rows[ny]):
            yield nx, ny

def main() -> int:
    rows = load_board()
    meta = load_meta()

    width = len(rows[0])
    height = len(rows)

    errors: list[str] = []
    warnings: list[str] = []

    for index, row in enumerate(rows):
        if len(row) != width:
            errors.append(f"row {index} width {len(row)} does not match width {width}")

    if meta.get("width") != width:
        errors.append(f"metadata width {meta.get('width')} does not match board width {width}")

    if meta.get("height") != height:
        errors.append(f"metadata height {meta.get('height')} does not match board height {height}")

    bad_chars = sorted({char for row in rows for char in row if char not in ALLOWED})
    if bad_chars:
        errors.append(f"board contains unsupported characters: {bad_chars}")

    cells = [(x, y, char) for y, row in enumerate(rows) for x, char in enumerate(row)]

    pacman_cells = [(x, y) for x, y, char in cells if char == "P"]
    ghost_cells = [(x, y) for x, y, char in cells if char == "G"]
    dot_cells = [(x, y) for x, y, char in cells if char == "."]
    power_dot_cells = [(x, y) for x, y, char in cells if char == "o"]
    wall_cells = [(x, y) for x, y, char in cells if char == "#"]
    traversable_cells = [(x, y) for x, y, char in cells if char in TRAVERSABLE]

    if len(pacman_cells) != 1:
        errors.append(f"expected exactly one Pac-Man start, found {len(pacman_cells)}")

    if not ghost_cells:
        warnings.append("no ghost starts found")

    if not dot_cells:
        errors.append("expected at least one dot")

    if not wall_cells:
        errors.append("expected at least one wall")

    if not traversable_cells:
        errors.append("expected at least one traversable path cell")

    meta_p = meta.get("pacmanStart")
    if len(pacman_cells) == 1 and meta_p != {"x": pacman_cells[0][0], "y": pacman_cells[0][1]}:
        errors.append(f"metadata pacmanStart {meta_p} does not match board {pacman_cells[0]}")

    meta_ghosts = meta.get("ghostStarts", [])
    board_ghosts = [{"x": x, "y": y} for x, y in ghost_cells]
    if meta_ghosts != board_ghosts:
        errors.append(f"metadata ghostStarts {meta_ghosts} does not match board {board_ghosts}")

    if pacman_cells:
        px, py = pacman_cells[0]
        legal_moves = [
            (nx, ny)
            for nx, ny in neighbors(px, py, rows)
            if rows[ny][nx] in TRAVERSABLE
        ]
        if not legal_moves:
            errors.append("Pac-Man start has no legal orthogonal move")

    traversable_set = {(x, y) for x, y in traversable_cells}
    components = []
    remaining = set(traversable_set)

    while remaining:
        start = next(iter(remaining))
        seen = {start}
        queue = deque([start])
        remaining.remove(start)

        while queue:
            x, y = queue.popleft()
            for nx, ny in neighbors(x, y, rows):
                if (nx, ny) in remaining and rows[ny][nx] in TRAVERSABLE:
                    remaining.remove((nx, ny))
                    seen.add((nx, ny))
                    queue.append((nx, ny))

        components.append(seen)

    if len(components) > 1:
        component_sizes = sorted((len(c) for c in components), reverse=True)
        warnings.append(f"traversable board has {len(components)} regions: {component_sizes}")

    if errors:
        print("Board projection verification FAILED")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        return 1

    print("Board projection verification passed.")
    print(f"Board: {width}x{height}")
    print(f"Walls: {len(wall_cells)}")
    print(f"Dots: {len(dot_cells)}")
    print(f"Power dots: {len(power_dot_cells)}")
    print(f"Traversable cells: {len(traversable_cells)}")
    print(f"Pac-Man start: {pacman_cells[0] if pacman_cells else 'missing'}")
    print(f"Ghost starts: {ghost_cells}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
