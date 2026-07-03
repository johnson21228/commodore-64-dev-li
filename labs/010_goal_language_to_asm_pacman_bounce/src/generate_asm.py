#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

SCREEN_BASE = 0x0400
COLOR_BASE = 0xD800
SCREEN_WIDTH = 40
SCREEN_HEIGHT = 25
CUSTOM_CHARSET_ADDR = 0x3000

COLOR = {
    "black": 0,
    "blue": 6,
    "yellow": 7,
}

ALLOWED = set("#.o PGX")


def byte(value: int) -> str:
    return f"${value & 0xFF:02x}"


def word(value: int) -> str:
    return f"${value & 0xFFFF:04x}"


def load_board(path: Path) -> list[str]:
    rows = path.read_text().splitlines()
    if not rows:
        raise ValueError("board.txt is empty")
    width = len(rows[0])
    for y, row in enumerate(rows):
        if len(row) != width:
            raise ValueError(f"board row {y} width mismatch")
        bad = sorted({ch for ch in row if ch not in ALLOWED})
        if bad:
            raise ValueError(f"board row {y} has unsupported chars {bad}")
    if width > SCREEN_WIDTH or len(rows) > SCREEN_HEIGHT:
        raise ValueError(f"board {width}x{len(rows)} does not fit {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    return rows


def color_for(cell: str) -> int:
    if cell == "#":
        return COLOR["blue"]
    if cell in {".", "o"}:
        return COLOR["yellow"]
    return COLOR["black"]


def glyph_rows_to_bytes(rows: list[str]) -> list[int]:
    if len(rows) != 8 or any(len(row) != 8 for row in rows):
        raise ValueError("glyph must be 8 rows of 8 pixels")
    values: list[int] = []
    for row in rows:
        value = 0
        for bit, pixel in enumerate(row):
            if pixel != ".":
                value |= 1 << (7 - bit)
        values.append(value)
    return values


def wall_glyph(mask: int) -> list[int]:
    pixels = [["." for _ in range(8)] for _ in range(8)]

    def fill(x0: int, y0: int, x1: int, y1: int) -> None:
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                pixels[yy][xx] = "#"

    # Center node.
    fill(3, 3, 4, 4)

    # N=1, E=2, S=4, W=8.
    if mask & 1:
        fill(3, 0, 4, 3)
    if mask & 2:
        fill(4, 3, 7, 4)
    if mask & 4:
        fill(3, 4, 4, 7)
    if mask & 8:
        fill(0, 3, 3, 4)

    return glyph_rows_to_bytes(["".join(row) for row in pixels])


def build_charset() -> list[list[int]]:
    glyphs: list[list[int]] = []

    # 0 = blank.
    glyphs.append([0x00] * 8)

    # 1..16 = neighbor-aware thin-wall glyphs for wall masks 0..15.
    for mask in range(16):
        glyphs.append(wall_glyph(mask))

    # 17 = centered small pellet.
    glyphs.append(glyph_rows_to_bytes([
        "........",
        "........",
        "........",
        "...##...",
        "...##...",
        "........",
        "........",
        "........",
    ]))

    # 18 = centered power pellet.
    glyphs.append(glyph_rows_to_bytes([
        "........",
        "........",
        "..####..",
        "..####..",
        "..####..",
        "..####..",
        "........",
        "........",
    ]))

    return glyphs


def wall_mask(rows: list[str], x: int, y: int) -> int:
    mask = 0
    if y > 0 and rows[y - 1][x] == "#":
        mask |= 1
    if x + 1 < len(rows[y]) and rows[y][x + 1] == "#":
        mask |= 2
    if y + 1 < len(rows) and rows[y + 1][x] == "#":
        mask |= 4
    if x > 0 and rows[y][x - 1] == "#":
        mask |= 8
    return mask


def char_for_cell(rows: list[str], x: int, y: int) -> int:
    cell = rows[y][x]
    if cell == "#":
        return 1 + wall_mask(rows, x, y)
    if cell == ".":
        return 17
    if cell == "o":
        return 18
    return 0


def board_data(rows: list[str]) -> str:
    out = []
    for y, row in enumerate(rows):
        out.append(f"board_row_{y:02d}:")
        out.append("    .byte " + ", ".join(byte(ord(ch)) for ch in row))
    return "\n".join(out)


def charset_asm(glyphs: list[list[int]]) -> str:
    out = []
    for index, glyph in enumerate(glyphs):
        out.append(f"custom_char_{index:02d}:")
        out.append("    .byte " + ", ".join(byte(value) for value in glyph))
    return "\n".join(out)


def render_code(rows: list[str], left: int, top: int) -> str:
    out = []
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            saddr = SCREEN_BASE + (top + y) * SCREEN_WIDTH + left + x
            caddr = COLOR_BASE + (top + y) * SCREEN_WIDTH + left + x
            out.append(f"    ; board[{x:02d},{y:02d}] = {cell!r}")
            out.append(f"    lda #{byte(char_for_cell(rows, x, y))}")
            out.append(f"    sta {word(saddr)}")
            out.append(f"    lda #{byte(color_for(cell))}")
            out.append(f"    sta {word(caddr)}")
    return "\n".join(out)


def generate(rows: list[str]) -> str:
    width = len(rows[0])
    height = len(rows)
    left = (SCREEN_WIDTH - width) // 2
    top = 1 if height < SCREEN_HEIGHT else 0
    dots = sum(ch == "." for row in rows for ch in row)
    power = sum(ch == "o" for row in rows for ch in row)
    walls = sum(ch == "#" for row in rows for ch in row)
    glyphs = build_charset()
    charset_bytes = len(glyphs) * 8

    return f"""; Generated by Lab 010 generate_asm.py.
; Milestone B.1: custom C64 character projection from verified board.txt.
; Generated assembly is an artifact, not the board authority.

.setcpu "6502"

.segment "EXEHDR"
    .word $0801

BOARD_COLS = {width}
BOARD_ROWS = {height}
BOARD_CHAR_LEFT = {left}
BOARD_CHAR_TOP = {top}
DOT_COUNT = {dots}
POWER_DOT_COUNT = {power}
WALL_COUNT = {walls}
CUSTOM_CHAR_COUNT = {len(glyphs)}
CUSTOM_CHARSET_BYTES = {charset_bytes}
CUSTOM_CHARSET_ADDR = {word(CUSTOM_CHARSET_ADDR)}

.segment "STARTUP"

basic_start:
    .word basic_next
    .word 10
    .byte $9e
    .byte "2061", 0
basic_next:
    .word 0

start:
    sei
    lda #$00
    sta $d020
    sta $d021
    jsr install_custom_charset
    lda #$1c
    sta $d018
    jsr clear_screen
    jsr render_board

forever:
    jmp forever

install_custom_charset:
    ldx #$00
copy_charset_loop:
    lda custom_charset,x
    sta CUSTOM_CHARSET_ADDR,x
    inx
    cpx #CUSTOM_CHARSET_BYTES
    bne copy_charset_loop
    rts

clear_screen:
    ldx #$00
clear_loop:
    lda #$00
    sta $0400,x
    sta $0500,x
    sta $0600,x
    sta $06e8,x
    lda #$00
    sta $d800,x
    sta $d900,x
    sta $da00,x
    sta $dae8,x
    inx
    bne clear_loop
    rts

render_board:
{render_code(rows, left, top)}
    rts

; Custom character projection.
; char 00 = blank
; char 01..16 = neighbor-aware thin wall glyphs
; char 17 = centered pellet
; char 18 = centered power pellet
custom_charset:
{charset_asm(glyphs)}

; Board data copied from src/board.txt for auditability.
{board_data(rows)}
"""


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print("usage: generate_asm.py goal.lang program.lang generated_intent.json generated.s")
        return 2

    goal_path = Path(argv[1])
    program_path = Path(argv[2])
    intent_path = Path(argv[3])
    asm_path = Path(argv[4])
    src = Path(__file__).resolve().parent
    board_path = src / "board.txt"
    meta_path = src / "projected_board.json"

    rows = load_board(board_path)
    meta = json.loads(meta_path.read_text())

    if meta.get("width") != len(rows[0]) or meta.get("height") != len(rows):
        raise ValueError("projected_board.json dimensions do not match board.txt")

    asm_path.write_text(generate(rows))

    intent = {
        "schemaVersion": 3,
        "milestone": "board_only_render_custom_character_projection",
        "authority": {
            "boardText": str(board_path),
            "projectedBoard": str(meta_path),
            "sourceImage": meta.get("sourceImage"),
            "generatedAssemblyIsArtifact": True
        },
        "inputs": {
            "goal": goal_path.read_text().splitlines(),
            "program": program_path.read_text().splitlines()
        },
        "board": {
            "width": len(rows[0]),
            "height": len(rows),
            "walls": sum(ch == "#" for row in rows for ch in row),
            "dots": sum(ch == "." for row in rows for ch in row),
            "powerDots": sum(ch == "o" for row in rows for ch in row),
            "pacmanStart": meta.get("pacmanStart"),
            "ghostStarts": meta.get("ghostStarts", []),
            "projectionStatus": meta.get("projectionStatus")
        },
        "characterProjection": {
            "customCharsetAddress": "$3000",
            "blankChar": 0,
            "wallGlyphRange": [1, 16],
            "centeredDotChar": 17,
            "centeredPowerDotChar": 18,
            "wallGlyphSelection": "neighbor_aware_thin_wall"
        },
        "scopeLimits": [
            "no Pac-Man movement",
            "no ghost movement",
            "no scoring",
            "no win/loss outcomes",
            "no computer vision"
        ]
    }
    intent_path.write_text(json.dumps(intent, indent=2) + "\n")
    print(f"Generated {asm_path} from {board_path}")
    print(f"Generated {intent_path} from {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
