#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labs" / "010_goal_language_to_asm_pacman_bounce"
SRC = LAB / "src"

BOARD = SRC / "board.txt"
META = SRC / "projected_board.json"
ASM = SRC / "generated.s"
INTENT = SRC / "generated_intent.json"
GENERATOR = SRC / "generate_asm.py"
PROJECTED_VERIFIER = SRC / "verify_projected_board.py"

ALLOWED = set("#.o PGX")
TRAVERSABLE = set(".o PG")


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def read_board() -> list[str]:
    rows = BOARD.read_text().splitlines()
    if not rows:
        raise AssertionError("board.txt is empty")
    width = len(rows[0])
    for y, row in enumerate(rows):
        if len(row) != width:
            raise AssertionError(f"board row {y} width mismatch")
        bad = sorted({ch for ch in row if ch not in ALLOWED})
        if bad:
            raise AssertionError(f"board row {y} has unsupported chars {bad}")
    return rows


def parse_asm_board_rows(text: str) -> list[str]:
    rows = []
    for _, payload in re.findall(r"board_row_(\d{2}):\n    \.byte ([^\n]+)", text):
        chars = []
        for raw in payload.split(","):
            raw = raw.strip()
            chars.append(chr(int(raw[1:], 16) if raw.startswith("$") else int(raw)))
        rows.append("".join(chars))
    return rows


def parse_byte_table(text: str, label: str) -> list[int]:
    pattern = rf"{re.escape(label)}:\n((?:    \.byte [^\n]+\n?)+)"
    match = re.search(pattern, text)
    if not match:
        raise AssertionError(f"missing byte table {label}")
    values = []
    for line in match.group(1).splitlines():
        payload = line.split(".byte", 1)[1]
        for raw in payload.split(","):
            raw = raw.strip()
            values.append(int(raw[1:], 16) if raw.startswith("$") else int(raw))
    return values


def pacman_start(rows: list[str]) -> tuple[int, int]:
    found = [(x, y) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch == "P"]
    if len(found) != 1:
        raise AssertionError(f"expected exactly one Pac-Man start, found {len(found)}")
    return found[0]


def legal_neighbors(rows: list[str], x: int, y: int) -> list[tuple[int, int]]:
    out = []
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(rows) and 0 <= nx < len(rows[ny]) and rows[ny][nx] in TRAVERSABLE:
            out.append((nx, ny))
    return out


def main() -> int:
    required = [
        BOARD,
        META,
        ASM,
        INTENT,
        GENERATOR,
        PROJECTED_VERIFIER,
        LAB / "BOARD_PROJECTION_LI.md",
        LAB / "assets" / "source_board.png",
        LAB / "c64_asm.cfg",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        return fail("missing required files: " + ", ".join(missing))

    projected = subprocess.run([sys.executable, str(PROJECTED_VERIFIER)], cwd=ROOT, text=True, capture_output=True)
    if projected.returncode != 0:
        print(projected.stdout)
        print(projected.stderr)
        return fail("projected board verifier failed")

    rows = read_board()
    meta = json.loads(META.read_text())
    intent = json.loads(INTENT.read_text())
    asm_text = ASM.read_text()
    generator_text = GENERATOR.read_text()

    if meta.get("width") != len(rows[0]) or meta.get("height") != len(rows):
        return fail("projected_board.json dimensions do not match board.txt")

    if intent.get("milestone") != "pacman_random_path_walker":
        return fail("generated_intent.json does not declare pacman_random_path_walker")

    if not intent.get("authority", {}).get("generatedAssemblyIsArtifact"):
        return fail("generated_intent.json must declare generated assembly as artifact")

    if parse_asm_board_rows(asm_text) != rows:
        return fail("generated.s board_row data does not match board.txt")

    path_x = parse_byte_table(asm_text, "path_x")
    path_y = parse_byte_table(asm_text, "path_y")
    path_char = parse_byte_table(asm_text, "path_char")

    if len(path_x) != len(path_y):
        return fail("path_x and path_y lengths differ")
    if len(path_char) != len(path_x):
        return fail("path_char length does not match path length")
    if not set(path_char).issubset({19, 20, 21, 22}):
        return fail("path_char must use only directional Pac-Man chars 19..22")

    declared_len = intent.get("pacmanPathWalker", {}).get("pathLength")
    if declared_len != len(path_x):
        return fail(f"intent pathLength {declared_len} does not match generated path length {len(path_x)}")

    start = pacman_start(rows)
    if (path_x[0], path_y[0]) != start:
        return fail(f"path starts at {(path_x[0], path_y[0])}, expected Pac-Man start {start}")

    if not legal_neighbors(rows, *start):
        return fail("Pac-Man start has no legal move")

    visited = set()
    reversals = 0
    previous_delta = None

    for index, (x, y) in enumerate(zip(path_x, path_y)):
        if not (0 <= y < len(rows) and 0 <= x < len(rows[y])):
            return fail(f"path step {index} exits board at {(x, y)}")
        if rows[y][x] not in TRAVERSABLE:
            return fail(f"path step {index} enters blocked cell {(x, y)} = {rows[y][x]!r}")
        visited.add((x, y))

        if index > 0:
            px, py = path_x[index - 1], path_y[index - 1]
            dx, dy = x - px, y - py
            if abs(dx) + abs(dy) != 1:
                return fail(f"path step {index} is not orthogonal adjacent: {(px, py)} -> {(x, y)}")
            if previous_delta and (dx, dy) == (-previous_delta[0], -previous_delta[1]):
                reversals += 1
            previous_delta = (dx, dy)

    if len(visited) < 40:
        return fail(f"path visits only {len(visited)} unique cells")

    if reversals < 1:
        return fail("path should include at least one reverse direction")

    for snippet in [
        "Milestone C: Pac-Man random path walker",
        "PACMAN_E_CHAR = $13",
        "PACMAN_W_CHAR = $14",
        "PACMAN_N_CHAR = $15",
        "PACMAN_S_CHAR = $16",
        "PATH_LEN = 220",
        "path_char:",
        "draw_pacman:",
        "erase_pacman_cell:",
        "walk_loop:",
        "stop_game:",
        "path_x:",
        "path_y:",
        "board_row_00:",
        "board_row_21:",
    ]:
        if snippet not in asm_text:
            return fail(f"generated.s missing expected snippet: {snippet}")

    projection = intent.get("characterProjection", {})
    expected_chars = {"E": 19, "W": 20, "N": 21, "S": 22}
    if projection.get("pacmanChars") != expected_chars:
        return fail("generated_intent.json must declare directional Pac-Man chars 19..22")

    walker = intent.get("pacmanPathWalker", {})
    if walker.get("verticalGlyphReview") != "north and south glyphs use round body with explicit top/bottom mouth notch":
        return fail("intent must declare round-body vertical glyph review")

    if walker.get("movementAuthority") != "board.txt traversable cells":
        return fail("intent must declare board.txt traversable cells as movement authority")

    if "generate_path" not in generator_text or "legal_moves" not in generator_text:
        return fail("generate_asm.py must include legal path generation from board model")

    print("OK: C64 Lab 010 Pac-Man random path walker stays on verified board paths with slowed larger directional Pac-Man glyphs and round-body vertical mouth review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
