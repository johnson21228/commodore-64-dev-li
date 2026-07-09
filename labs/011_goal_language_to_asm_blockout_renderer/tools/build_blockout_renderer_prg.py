#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PRG = DIST / "blockout_renderer.prg"
CELLS = DIST / "blockout_renderer_screen_cells.json"

LOAD_ADDR = 0x0801
CODE_START = 0x080D
SCREEN_BASE = 0x0400
COLOR_BASE = 0xD800

def ensure_generated() -> None:
    if not (DIST / "pit_line_segments.json").exists():
        subprocess.run(["python3", "tools/generate_blockout_renderer.py"], cwd=ROOT, check=True)

def map_to_cell(x: int, y: int) -> tuple[int, int]:
    col = max(0, min(39, round(x / 8)))
    row = max(0, min(24, round(y / 8)))
    return col, row

def bresenham_cells(x1: int, y1: int, x2: int, y2: int) -> list[tuple[int, int]]:
    c1, r1 = map_to_cell(x1, y1)
    c2, r2 = map_to_cell(x2, y2)

    points: list[tuple[int, int]] = []
    dx = abs(c2 - c1)
    dy = -abs(r2 - r1)
    sx = 1 if c1 < c2 else -1
    sy = 1 if r1 < r2 else -1
    err = dx + dy

    c, r = c1, r1
    while True:
        points.append((c, r))
        if c == c2 and r == r2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            c += sx
        if e2 <= dx:
            err += dx
            r += sy
    return points

def emit_byte(code: list[int], value: int) -> None:
    code.append(value & 0xFF)

def emit_word(code: list[int], value: int) -> None:
    code.append(value & 0xFF)
    code.append((value >> 8) & 0xFF)

def emit_lda_imm(code: list[int], value: int) -> None:
    code.extend([0xA9, value & 0xFF])

def emit_ldx_imm(code: list[int], value: int) -> None:
    code.extend([0xA2, value & 0xFF])

def emit_sta_abs(code: list[int], addr: int) -> None:
    code.append(0x8D)
    emit_word(code, addr)

def emit_sta_abs_x(code: list[int], addr: int) -> None:
    code.append(0x9D)
    emit_word(code, addr)

def emit_inx(code: list[int]) -> None:
    code.append(0xE8)

def emit_bne_to(code: list[int], current_addr: int, target_addr: int) -> None:
    # BNE rel8. Offset is relative to address after operand.
    after = current_addr + 2
    offset = target_addr - after
    if not -128 <= offset <= 127:
        raise ValueError(f"Branch out of range: {offset}")
    code.extend([0xD0, offset & 0xFF])

def emit_jmp_abs(code: list[int], addr: int) -> None:
    code.append(0x4C)
    emit_word(code, addr)

def basic_stub() -> bytes:
    # C64 BASIC:
    # 10 SYS2061
    #
    # Code starts at $080D == 2061.
    return bytes([
        0x01, 0x08,             # PRG load address $0801
        0x0B, 0x08,             # next BASIC line pointer
        0x0A, 0x00,             # line 10
        0x9E,                   # SYS token
        0x32, 0x30, 0x36, 0x31, # "2061"
        0x00,                   # end of line
        0x00, 0x00,             # end of BASIC program
    ])

def build_machine_code(cells: list[tuple[int, int]]) -> bytes:
    code: list[int] = []
    addr = CODE_START

    def add(values: list[int]) -> None:
        nonlocal addr
        code.extend(values)
        addr += len(values)

    # Black border/background.
    add([0xA9, 0x00, 0x8D, 0x20, 0xD0, 0x8D, 0x21, 0xD0])

    # Clear screen memory.
    add([0xA9, 0x20, 0xA2, 0x00])  # LDA #space, LDX #0
    loop = addr
    add([0x9D, 0x00, 0x04])
    add([0x9D, 0x00, 0x05])
    add([0x9D, 0x00, 0x06])
    add([0x9D, 0x00, 0x07])
    add([0xE8])
    branch_addr = addr
    temp: list[int] = []
    emit_bne_to(temp, branch_addr, loop)
    add(temp)

    # Set color RAM.
    add([0xA9, 0x0E, 0xA2, 0x00])  # light blue-ish
    loop = addr
    add([0x9D, 0x00, 0xD8])
    add([0x9D, 0x00, 0xD9])
    add([0x9D, 0x00, 0xDA])
    add([0x9D, 0x00, 0xDB])
    add([0xE8])
    branch_addr = addr
    temp = []
    emit_bne_to(temp, branch_addr, loop)
    add(temp)

    # Draw governed board cells.
    for col, row in cells:
        offset = row * 40 + col
        if not 0 <= offset < 1000:
            continue

        # Use '*' screen code as the first crude line/pixel mark.
        add([0xA9, 0x2A])
        temp = []
        emit_sta_abs(temp, SCREEN_BASE + offset)
        add(temp)

        # Use yellow/white-ish color for drawn cells.
        add([0xA9, 0x07])
        temp = []
        emit_sta_abs(temp, COLOR_BASE + offset)
        add(temp)

    # Infinite loop so the display remains visible.
    halt = addr
    temp = []
    emit_jmp_abs(temp, halt)
    add(temp)

    return bytes(code)

def main() -> None:
    ensure_generated()
    DIST.mkdir(parents=True, exist_ok=True)

    segments = json.loads((DIST / "pit_line_segments.json").read_text(encoding="utf-8"))

    ordered_cells: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()

    for segment in segments:
        for cell in bresenham_cells(segment["x1"], segment["y1"], segment["x2"], segment["y2"]):
            if cell not in seen:
                seen.add(cell)
                ordered_cells.append(cell)

    # Add a tiny label at the top-left. This is not board geometry; it is run evidence.
    label = "LAB011"
    for i, _ in enumerate(label):
        ordered_cells.append((i, 0))

    program = basic_stub() + build_machine_code(ordered_cells)
    PRG.write_bytes(program)

    CELLS.write_text(json.dumps({
        "source": "dist/pit_line_segments.json",
        "rendering": "character_screen_approximation",
        "screen": {"columns": 40, "rows": 25},
        "cell_count": len(ordered_cells),
        "cells": [{"col": c, "row": r} for c, r in ordered_cells],
    }, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {PRG}")
    print(f"Wrote {CELLS}")
    print(f"Rendered {len(ordered_cells)} screen cells from governed pit_line_segments.")

if __name__ == "__main__":
    main()
