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
SPRITE_DATA_ADDR = 0x3400
SPRITE_PTR_E_OPEN = SPRITE_DATA_ADDR // 64
SPRITE_PTR_W_OPEN = SPRITE_PTR_E_OPEN + 1
SPRITE_PTR_N_OPEN = SPRITE_PTR_E_OPEN + 2
SPRITE_PTR_S_OPEN = SPRITE_PTR_E_OPEN + 3
SPRITE_PTR_E_CLOSED = SPRITE_PTR_E_OPEN + 4
SPRITE_PTR_W_CLOSED = SPRITE_PTR_E_OPEN + 5
SPRITE_PTR_N_CLOSED = SPRITE_PTR_E_OPEN + 6
SPRITE_PTR_S_CLOSED = SPRITE_PTR_E_OPEN + 7

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

    return glyphs


def sprite_rows_to_bytes(rows: list[str]) -> list[int]:
    if len(rows) != 21 or any(len(row) != 24 for row in rows):
        raise ValueError("sprite must be 21 rows of 24 pixels")
    out: list[int] = []
    for row in rows:
        for chunk_start in (0, 8, 16):
            value = 0
            for bit, pixel in enumerate(row[chunk_start:chunk_start + 8]):
                if pixel != ".":
                    value |= 1 << (7 - bit)
            out.append(value)
    out.append(0)
    return out


def radial_pacman_sprite(direction: str, open_mouth: bool) -> list[str]:
    # C64 hardware sprite canvas is 24x21.
    #
    # Pac-Man is drawn from one shared radial geometry for every direction:
    # center = (11.5, 9.5)
    # radius ~= 6 pixels
    #
    # Open-mouth frames cut a wedge out of the same circular body.
    # This makes north/south use the same pixel width and visual weight
    # as east/west, instead of relying on hand-drawn vertical art.
    cx = 11.5
    cy = 9.5
    radius_sq = 6.15 * 6.15
    mouth_slope = 0.72

    rows: list[str] = []
    for y in range(21):
        row: list[str] = []
        for x in range(24):
            px = x + 0.5
            py = y + 0.5
            dx = px - cx
            dy = py - cy

            inside = (dx * dx + dy * dy) <= radius_sq

            if inside and open_mouth:
                if direction == "E" and dx > 0 and abs(dy) <= dx * mouth_slope:
                    inside = False
                elif direction == "W" and dx < 0 and abs(dy) <= (-dx) * mouth_slope:
                    inside = False
                elif direction == "N" and dy < 0 and abs(dx) <= (-dy) * mouth_slope:
                    inside = False
                elif direction == "S" and dy > 0 and abs(dx) <= dy * mouth_slope:
                    inside = False

            row.append("#" if inside else ".")
        rows.append("".join(row))
    return rows


def build_sprites() -> list[list[int]]:
    # Eight frames:
    # D0-D3 open mouth E/W/N/S
    # D4-D7 closed mouth E/W/N/S
    #
    # All directions are generated from the same radial body and same
    # mouth-wedge rule so vertical and horizontal sprites use the same
    # pixel dimensions and visual weight.
    east_open = radial_pacman_sprite("E", True)
    west_open = radial_pacman_sprite("W", True)
    north_open = radial_pacman_sprite("N", True)
    south_open = radial_pacman_sprite("S", True)

    east_closed = radial_pacman_sprite("E", False)
    west_closed = radial_pacman_sprite("W", False)
    north_closed = radial_pacman_sprite("N", False)
    south_closed = radial_pacman_sprite("S", False)

    return [
        sprite_rows_to_bytes(east_open),
        sprite_rows_to_bytes(west_open),
        sprite_rows_to_bytes(north_open),
        sprite_rows_to_bytes(south_open),
        sprite_rows_to_bytes(east_closed),
        sprite_rows_to_bytes(west_closed),
        sprite_rows_to_bytes(north_closed),
        sprite_rows_to_bytes(south_closed),
    ]


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

    for _ in range(steps - 1):
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

        direction, x, y = options[rng % len(options)]
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


def sprite_asm(sprites: list[list[int]]) -> str:
    labels = [
        "sprite_pacman_east_open",
        "sprite_pacman_west_open",
        "sprite_pacman_north_open",
        "sprite_pacman_south_open",
        "sprite_pacman_east_closed",
        "sprite_pacman_west_closed",
        "sprite_pacman_north_closed",
        "sprite_pacman_south_closed",
    ]
    out: list[str] = []
    for label, sprite in zip(labels, sprites):
        out.append(f"{label}:")
        for index in range(0, len(sprite), 8):
            out.append("    .byte " + ", ".join(byte(value) for value in sprite[index:index + 8]))
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


def cell_sprite_x(x: int, left: int) -> int:
    # C64 sprite coordinates are offset from the text cell origin.
    # Tuned so Pac-Man is visually centered between hallway walls.
    # C.13/C.12 appeared one pixel too far right.
    return 17 + (left + x) * 8


def cell_sprite_y(y: int, top: int) -> int:
    # Tuned so Pac-Man is visually centered between hallway walls.
    # C.12 appeared one pixel too high.
    return 44 + (top + y) * 8


def direction_ptr(path: list[tuple[int, int]], index: int) -> int:
    if index + 1 < len(path):
        x, y = path[index]
        nx, ny = path[index + 1]
        dx, dy = nx - x, ny - y
    elif index > 0:
        px, py = path[index - 1]
        x, y = path[index]
        dx, dy = x - px, y - py
    else:
        dx, dy = 1, 0

    if dx > 0:
        return SPRITE_PTR_E_OPEN
    if dx < 0:
        return SPRITE_PTR_W_OPEN
    if dy < 0:
        return SPRITE_PTR_N_OPEN
    return SPRITE_PTR_S_OPEN


def generate(rows: list[str], path: list[tuple[int, int]]) -> str:
    width = len(rows[0])
    height = len(rows)
    left = (SCREEN_WIDTH - width) // 2
    top = 1 if height < SCREEN_HEIGHT else 0
    dots = sum(ch == "." for row in rows for ch in row)
    power = sum(ch == "o" for row in rows for ch in row)
    walls = sum(ch == "#" for row in rows for ch in row)
    glyphs = build_charset()
    sprites = build_sprites()
    charset_bytes = len(glyphs) * 8
    sprite_bytes = len(sprites) * 64

    path_screen = [cell_screen_addr(x, y, left, top) for x, y in path]
    path_x = [x for x, _ in path]
    path_y = [y for _, y in path]
    sprite_x = [cell_sprite_x(x, left) for x, _ in path]
    sprite_y = [cell_sprite_y(y, top) for _, y in path]
    sprite_ptr = [direction_ptr(path, index) for index in range(len(path))]

    return f"""; Generated by Lab 010 generate_asm.py.
; Milestone C.15: radial Pac-Man sprite geometry with retuned x/y sprite origin from verified board.txt.
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
SPRITE_DATA_BYTES = {sprite_bytes}
SPRITE_DATA_ADDR = {word(SPRITE_DATA_ADDR)}
SPRITE_PTR_E_OPEN = {byte(SPRITE_PTR_E_OPEN)}
SPRITE_PTR_W_OPEN = {byte(SPRITE_PTR_W_OPEN)}
SPRITE_PTR_N_OPEN = {byte(SPRITE_PTR_N_OPEN)}
SPRITE_PTR_S_OPEN = {byte(SPRITE_PTR_S_OPEN)}
SPRITE_PTR_E_CLOSED = {byte(SPRITE_PTR_E_CLOSED)}
SPRITE_PTR_W_CLOSED = {byte(SPRITE_PTR_W_CLOSED)}
SPRITE_PTR_N_CLOSED = {byte(SPRITE_PTR_N_CLOSED)}
SPRITE_PTR_S_CLOSED = {byte(SPRITE_PTR_S_CLOSED)}
PATH_LEN = {len(path)}
PATH_LAST = {len(path) - 1}
SCREEN_PTR = $fb

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
    jsr install_sprite_data
    lda #$1c
    sta $d018
    jsr clear_screen
    jsr render_board
    jsr init_sprite
    lda #$00
    sta path_index
    jsr set_sprite_position_from_index
    jsr set_target_for_index
    lda #$00
    sta mouth_counter
    sta mouth_phase
    jsr set_sprite_pointer_for_index
    jsr update_sprite_registers

walk_loop:
    jsr delay_frame
    jsr update_mouth_animation
    jsr set_sprite_pointer_for_index
    jsr at_target
    beq move_sprite
    jsr erase_cell_for_index
    lda path_index
    cmp #PATH_LAST
    bcc advance_path
    lda #$02
    sta $d020
stop_game:
    jmp stop_game

advance_path:
    inc path_index
    jsr set_target_for_index
    jsr set_sprite_pointer_for_index

move_sprite:
    jsr move_sprite_toward_target
    jsr update_sprite_registers
    jmp walk_loop

delay_frame:
    ldx #$02
wait_frame:
    lda $d012
wait_raster_low:
    cmp $d012
    beq wait_raster_low
wait_next_frame:
    lda $d012
    bne wait_next_frame
    dex
    bne wait_frame
    rts

init_sprite:
    lda #$01
    sta $d015
    lda #$00
    sta $d017
    sta $d01d
    sta $d01c
    sta $d01b
    lda #$07
    sta $d027
    rts

set_sprite_position_from_index:
    ldx path_index
    lda path_sprite_x_lo,x
    sta sprite_x_lo
    lda path_sprite_x_hi,x
    sta sprite_x_hi
    lda path_sprite_y,x
    sta sprite_y
    rts

set_target_for_index:
    ldx path_index
    lda path_sprite_x_lo,x
    sta target_x_lo
    lda path_sprite_x_hi,x
    sta target_x_hi
    lda path_sprite_y,x
    sta target_y
    rts

set_sprite_pointer_for_index:
    ldx path_index
    lda path_sprite_ptr,x
    ldy mouth_phase
    beq sprite_pointer_ready
    clc
    adc #$04
sprite_pointer_ready:
    sta $07f8
    rts

update_mouth_animation:
    inc mouth_counter
    lda mouth_counter
    and #$07
    bne mouth_done
    lda mouth_phase
    eor #$01
    sta mouth_phase
mouth_done:
    rts

update_sprite_registers:
    lda sprite_x_lo
    sta $d000
    lda sprite_y
    sta $d001
    lda $d010
    and #$fe
    ora sprite_x_hi
    sta $d010
    rts

at_target:
    lda sprite_x_lo
    cmp target_x_lo
    bne not_at_target
    lda sprite_x_hi
    cmp target_x_hi
    bne not_at_target
    lda sprite_y
    cmp target_y
    bne not_at_target
    lda #$01
    rts
not_at_target:
    lda #$00
    rts

move_sprite_toward_target:
    lda sprite_x_hi
    cmp target_x_hi
    bcc move_x_inc
    bne move_x_dec
    lda sprite_x_lo
    cmp target_x_lo
    bcc move_x_inc
    bne move_x_dec
    jmp move_y_check

move_x_inc:
    inc sprite_x_lo
    bne move_done
    inc sprite_x_hi
    jmp move_done

move_x_dec:
    lda sprite_x_lo
    bne move_x_dec_lo
    dec sprite_x_hi
move_x_dec_lo:
    dec sprite_x_lo
    jmp move_done

move_y_check:
    lda sprite_y
    cmp target_y
    bcc move_y_inc
    bne move_y_dec
    jmp move_done

move_y_inc:
    inc sprite_y
    jmp move_done

move_y_dec:
    dec sprite_y

move_done:
    rts

erase_cell_for_index:
    ldx path_index
    lda path_screen_lo,x
    sta SCREEN_PTR
    lda path_screen_hi,x
    sta SCREEN_PTR+1
    ldy #$00
    lda #$00
    sta (SCREEN_PTR),y
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

install_sprite_data:
    ldx #$00
copy_sprite_page0:
    lda custom_sprites,x
    sta SPRITE_DATA_ADDR,x
    inx
    bne copy_sprite_page0

    ldx #$00
copy_sprite_page1:
    lda custom_sprites+$0100,x
    sta SPRITE_DATA_ADDR+$0100,x
    inx
    bne copy_sprite_page1
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
sprite_x_lo:
    .byte $00
sprite_x_hi:
    .byte $00
sprite_y:
    .byte $00
target_x_lo:
    .byte $00
target_x_hi:
    .byte $00
target_y:
    .byte $00
mouth_counter:
    .byte $00
mouth_phase:
    .byte $00

; Custom character projection for board.
custom_charset:
{charset_asm(glyphs)}

; Hardware sprite data for Pac-Man directions.
custom_sprites:
{sprite_asm(sprites)}

; Random legal path generated from board.txt.
{byte_table("path_x", path_x)}
{byte_table("path_y", path_y)}
{byte_table("path_sprite_x_lo", [value & 0xFF for value in sprite_x])}
{byte_table("path_sprite_x_hi", [(value >> 8) & 0x01 for value in sprite_x])}
{byte_table("path_sprite_y", sprite_y)}
{byte_table("path_sprite_ptr", sprite_ptr)}
{byte_table("path_screen_lo", [addr & 0xFF for addr in path_screen])}
{byte_table("path_screen_hi", [addr >> 8 for addr in path_screen])}

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
        "schemaVersion": 5,
        "milestone": "pacman_hardware_sprite_interpolation_retuned_xy_origin",
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
        "spriteProjection": {
            "enabledSprite": 0,
            "spriteDataAddress": "$3400",
            "spritePointers": {
                "E_OPEN": SPRITE_PTR_E_OPEN,
                "W_OPEN": SPRITE_PTR_W_OPEN,
                "N_OPEN": SPRITE_PTR_N_OPEN,
                "S_OPEN": SPRITE_PTR_S_OPEN,
                "E_CLOSED": SPRITE_PTR_E_CLOSED,
                "W_CLOSED": SPRITE_PTR_W_CLOSED,
                "N_CLOSED": SPRITE_PTR_N_CLOSED,
                "S_CLOSED": SPRITE_PTR_S_CLOSED
            },
            "movement": "pixel interpolation between board-cell centers",
            "sizeTuning": "smaller 10-12 pixel centered sprite body within 24x21 hardware sprite cell",
            "mouthDirection": "hardware sprite pointer selected from path direction",
            "mouthAnimation": "open and closed sprite frames alternate at a visible crunch pace while moving",
            "mouthSpeedTuning": "toggle every 8 frame-pixel updates",
            "verticalSpriteArt": "north/south mouth uses same radial sprite geometry as east/west",
            "spriteFootprint": "all directions use shared center, shared radius, and shared mouth-wedge rule",
            "spriteGeometry": "radial Pac-Man generated from one circle-like pixel model",
            "spriteOriginTuning": "sprite y origin lowered by one pixel and x origin shifted left by three pixels for hallway centering",
            "spriteCopyFix": "copies all 512 bytes for eight sprite frames",
            "speedTuning": "two raster frames per interpolated pixel"
        },
        "pacmanPathWalker": {
            "pathLength": len(path),
            "start": {"x": path[0][0], "y": path[0][1]},
            "movementAuthority": "board.txt traversable cells",
            "traversableCells": [".", "o", " ", "P", "G"],
            "blockedCells": ["#", "X"],
            "turnPolicy": "deterministic LFSR random legal path from board model",
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
