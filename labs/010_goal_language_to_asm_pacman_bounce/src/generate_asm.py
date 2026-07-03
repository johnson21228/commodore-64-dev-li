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
    "red": 2,
    "blue": 6,
    "yellow": 7,
}

ALLOWED = set("#.o PGX")
TRAVERSABLE = set(".o PG")

DIRS = [
    ("N", 0, -1),
    ("E", 1, 0),
    ("S", 0, 1),
    ("W", -1, 0),
]

REVERSE = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}


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


def find_one(rows: list[str], target: str) -> tuple[int, int]:
    found = [(x, y) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch == target]
    if len(found) != 1:
        raise ValueError(f"expected exactly one {target!r}, found {len(found)}")
    return found[0]


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

    fill(3, 3, 4, 4)

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

    glyphs.append([0x00] * 8)

    for mask in range(16):
        glyphs.append(wall_glyph(mask))

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

    # 19 = Pac-Man facing east.
    # Nearly full 8x8 cell with a small inset and a clear right-facing mouth.
    glyphs.append(glyph_rows_to_bytes([
        ".######.",
        "########",
        "#######.",
        "#####...",
        "#####...",
        "#######.",
        "########",
        ".######.",
    ]))

    # 20 = Pac-Man facing west.
    # Mirrored east glyph with a clear left-facing mouth.
    glyphs.append(glyph_rows_to_bytes([
        ".######.",
        "########",
        ".#######",
        "...#####",
        "...#####",
        ".#######",
        "########",
        ".######.",
    ]))

    # 21 = Pac-Man facing north.
    # Round-ish full-cell body with a top-facing mouth notch.
    glyphs.append(glyph_rows_to_bytes([
        ".##..##.",
        "###..###",
        "########",
        "########",
        "########",
        "########",
        "########",
        ".######.",
    ]))

    # 22 = Pac-Man facing south.
    # Round-ish full-cell body with a bottom-facing mouth notch.
    glyphs.append(glyph_rows_to_bytes([
        ".######.",
        "########",
        "########",
        "########",
        "########",
        "########",
        "###..###",
        ".##..##.",
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


def is_traversable(rows: list[str], x: int, y: int) -> bool:
    return 0 <= y < len(rows) and 0 <= x < len(rows[y]) and rows[y][x] in TRAVERSABLE


def lfsr_next(value: int) -> int:
    carry = value & 0x80
    value = (value << 1) & 0xFF
    if carry:
        value ^= 0x1D
    return value


def legal_moves(rows: list[str], x: int, y: int) -> list[tuple[str, int, int]]:
    moves: list[tuple[str, int, int]] = []
    for name, dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if is_traversable(rows, nx, ny):
            moves.append((name, nx, ny))
    return moves


def generate_path(rows: list[str], steps: int = 220) -> list[tuple[int, int]]:
    x, y = find_one(rows, "P")
    direction: str | None = None
    rng = 0x5A
    path = [(x, y)]

    for step in range(steps - 1):
        moves = legal_moves(rows, x, y)
        if not moves:
            raise ValueError(f"Pac-Man dead-ended with no legal move at {(x, y)}")

        reverse_name = REVERSE.get(direction or "")
        non_reverse = [move for move in moves if move[0] != reverse_name]
        reverse_moves = [move for move in moves if move[0] == reverse_name]

        rng = lfsr_next(rng)

        if non_reverse:
            options = non_reverse[:]
            if reverse_moves and (rng & 0x07) == 0:
                options += reverse_moves
        else:
            options = reverse_moves or moves

        choice = options[rng % len(options)]
        direction, x, y = choice
        if not is_traversable(rows, x, y):
            raise ValueError(f"generated path entered blocked cell {(x, y)}")
        path.append((x, y))

    return path


def board_data(rows: list[str]) -> str:
    out = []
    for y, row in enumerate(rows):
        out.append(f"board_row_{y:02d}:")
        out.append("    .byte " + ", ".join(byte(ord(ch)) for ch in row))
    return "\n".join(out)


def byte_table(label: str, values: list[int]) -> str:
    lines = [f"{label}:"]
    for index in range(0, len(values), 16):
        lines.append("    .byte " + ", ".join(byte(value) for value in values[index:index + 16]))
    return "\n".join(lines)


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


def cell_screen_addr(x: int, y: int, left: int, top: int) -> int:
    return SCREEN_BASE + (top + y) * SCREEN_WIDTH + left + x


def cell_color_addr(x: int, y: int, left: int, top: int) -> int:
    return COLOR_BASE + (top + y) * SCREEN_WIDTH + left + x


def generate(rows: list[str], path: list[tuple[int, int]]) -> str:
    width = len(rows[0])
    height = len(rows)
    left = (SCREEN_WIDTH - width) // 2
    top = 1 if height < SCREEN_HEIGHT else 0
    dots = sum(ch == "." for row in rows for ch in row)
    power = sum(ch == "o" for row in rows for ch in row)
    walls = sum(ch == "#" for row in rows for ch in row)
    glyphs = build_charset()
    charset_bytes = len(glyphs) * 8

    path_screen = [cell_screen_addr(x, y, left, top) for x, y in path]
    path_color = [cell_color_addr(x, y, left, top) for x, y in path]
    path_x = [x for x, _ in path]
    path_y = [y for _, y in path]

    # Character codes: 19=E, 20=W, 21=N, 22=S.
    path_char: list[int] = []
    for index, (x, y) in enumerate(path):
        if index + 1 < len(path):
            nx, ny = path[index + 1]
            dx, dy = nx - x, ny - y
        elif index > 0:
            px, py = path[index - 1]
            dx, dy = x - px, y - py
        else:
            dx, dy = 1, 0

        if dx > 0:
            path_char.append(19)
        elif dx < 0:
            path_char.append(20)
        elif dy < 0:
            path_char.append(21)
        else:
            path_char.append(22)

    return f"""; Generated by Lab 010 generate_asm.py.
; Milestone C: Pac-Man random path walker from verified board.txt.
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
PACMAN_E_CHAR = $13
PACMAN_W_CHAR = $14
PACMAN_N_CHAR = $15
PACMAN_S_CHAR = $16
PATH_LEN = {len(path)}
SCREEN_PTR = $fb
COLOR_PTR = $fd

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
    lda #$00
    sta path_index
    jsr draw_pacman

walk_loop:
    jsr delay_frame
    jsr erase_pacman_cell
    inc path_index
    lda path_index
    cmp #PATH_LEN
    bcc continue_walk
    lda #$02
    sta $d020
stop_game:
    jmp stop_game

continue_walk:
    jsr draw_pacman
    jmp walk_loop

delay_frame:
    ldx #$90
delay_outer:
    ldy #$ff
delay_inner:
    dey
    bne delay_inner
    dex
    bne delay_outer
    rts

set_screen_ptr_for_index:
    ldx path_index
    lda path_screen_lo,x
    sta SCREEN_PTR
    lda path_screen_hi,x
    sta SCREEN_PTR+1
    rts

set_color_ptr_for_index:
    ldx path_index
    lda path_color_lo,x
    sta COLOR_PTR
    lda path_color_hi,x
    sta COLOR_PTR+1
    rts

erase_pacman_cell:
    jsr set_screen_ptr_for_index
    ldy #$00
    lda #$00
    sta (SCREEN_PTR),y
    jsr set_color_ptr_for_index
    lda #$00
    sta (COLOR_PTR),y
    rts

draw_pacman:
    jsr set_screen_ptr_for_index
    ldy #$00
    ldx path_index
    lda path_char,x
    sta (SCREEN_PTR),y
    jsr set_color_ptr_for_index
    lda #$07
    sta (COLOR_PTR),y
    rts

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

path_index:
    .byte $00

; Custom character projection.
; char 00 = blank
; char 01..16 = neighbor-aware thin wall glyphs
; char 17 = centered pellet
; char 18 = centered power pellet
; char 19 = Pac-Man facing east
; char 20 = Pac-Man facing west
; char 21 = Pac-Man facing north
; char 22 = Pac-Man facing south
custom_charset:
{charset_asm(glyphs)}

; Random legal path generated from board.txt.
{byte_table("path_x", path_x)}
{byte_table("path_y", path_y)}
{byte_table("path_char", path_char)}
{byte_table("path_screen_lo", [addr & 0xFF for addr in path_screen])}
{byte_table("path_screen_hi", [addr >> 8 for addr in path_screen])}
{byte_table("path_color_lo", [addr & 0xFF for addr in path_color])}
{byte_table("path_color_hi", [addr >> 8 for addr in path_color])}

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

    path = generate_path(rows)

    asm_path.write_text(generate(rows, path))

    intent = {
        "schemaVersion": 4,
        "milestone": "pacman_random_path_walker",
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
            "pacmanChars": {"E": 19, "W": 20, "N": 21, "S": 22},
            "wallGlyphSelection": "neighbor_aware_thin_wall"
        },
        "pacmanPathWalker": {
            "pathLength": len(path),
            "start": {"x": path[0][0], "y": path[0][1]},
            "movementAuthority": "board.txt traversable cells",
            "traversableCells": [".", "o", " ", "P", "G"],
            "blockedCells": ["#", "X"],
            "turnPolicy": "deterministic LFSR random legal path from board model",
            "visualMotion": "slowed cell-to-cell movement",
            "mouthDirection": "Pac-Man character faces next path direction",
            "cellFit": "nearly full 8x8 hallway cell with small inset",
            "verticalGlyphReview": "north and south glyphs use round body with explicit top/bottom mouth notch",
            "deadEndPolicy": "reverse if it is the only legal move",
            "failurePolicy": "runtime stops visibly if path completes; verifier fails if path enters blocked cells"
        },
        "scopeLimits": [
            "no ghost movement",
            "no scoring",
            "no win/loss outcomes beyond visible stop",
            "no computer vision"
        ]
    }
    intent_path.write_text(json.dumps(intent, indent=2) + "\n")
    print(f"Generated {asm_path} from {board_path}")
    print(f"Generated {intent_path} from {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
