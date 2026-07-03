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
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        return fail("missing required files: " + ", ".join(missing))

    projected = subprocess.run([sys.executable, str(PROJECTED_VERIFIER)], cwd=ROOT, text=True, capture_output=True)
    if projected.returncode != 0:
        print(projected.stdout)
        print(projected.stderr)
        return fail("projected board verifier failed")

    board_rows = read_board()
    meta = json.loads(META.read_text())
    intent = json.loads(INTENT.read_text())
    asm_text = ASM.read_text()
    generator_text = GENERATOR.read_text()

    if meta.get("width") != len(board_rows[0]) or meta.get("height") != len(board_rows):
        return fail("projected_board.json dimensions do not match board.txt")

    if intent.get("milestone") != "board_only_render":
        return fail("generated_intent.json does not declare board_only_render")

    if not intent.get("authority", {}).get("generatedAssemblyIsArtifact"):
        return fail("generated_intent.json must declare generated assembly as artifact")

    if parse_asm_board_rows(asm_text) != board_rows:
        return fail("generated.s board_row data does not match board.txt")

    for snippet in [
        "Milestone B: board-only C64 render",
        "BOARD_COLS = 28",
        "BOARD_ROWS = 22",
        "DOT_COUNT = 205",
        "POWER_DOT_COUNT = 4",
        "WALL_COUNT = 332",
        "render_board:",
        "forever:",
        "board_row_00:",
        "board_row_21:",
    ]:
        if snippet not in asm_text:
            return fail(f"generated.s missing expected snippet: {snippet}")

    for forbidden in ["move_pacman", "ghost_move", "collision_loss", "dot_eating_loop"]:
        if forbidden in asm_text:
            return fail(f"board-only milestone should not include runtime feature: {forbidden}")

    if "board.txt" not in generator_text or "projected_board.json" not in generator_text:
        return fail("generate_asm.py must read board.txt and projected_board.json")

    print("OK: C64 Lab 010 board-only render is generated from verified board.txt/projected_board.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
