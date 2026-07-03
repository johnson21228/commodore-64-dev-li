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



def find_char(rows: list[str], wanted: str) -> tuple[int, int]:
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == wanted:
                return x, y
    raise ValueError(f"character {wanted!r} not found in board")

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


def render_char_rows(rows: list[str]) -> list[list[int]]:
    return [
        [char_for_cell(rows, x, y) for x in range(len(row))]
        for y, row in enumerate(rows)
    ]


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


def legal_move_masks(rows: list[str]) -> list[list[int]]:
    masks: list[list[int]] = []
    height = len(rows)
    width = len(rows[0])

    for y in range(height):
        mask_row: list[int] = []
        for x in range(width):
            mask = 0
            if is_traversable(rows, x, y):
                if y > 0 and is_traversable(rows, x, y - 1):
                    mask |= 0x01
                if y + 1 < height and is_traversable(rows, x, y + 1):
                    mask |= 0x02
                if x > 0 and is_traversable(rows, x - 1, y):
                    mask |= 0x04
                if x + 1 < width and is_traversable(rows, x + 1, y):
                    mask |= 0x08
            mask_row.append(mask)
        masks.append(mask_row)
    return masks


def labelled_byte_rows(prefix: str, rows: list[list[int]]) -> str:
    out: list[str] = []
    for index, values in enumerate(rows):
        out.append(f"{prefix}_{index:02d}:")
        out.append("    .byte " + ", ".join(byte(value) for value in values))
    return "\n".join(out)


def row_address_tables(prefix: str, labels: list[str]) -> str:
    lo_values = [f"<{label}" for label in labels]
    hi_values = [f">{label}" for label in labels]
    return "\n".join([
        f"{prefix}_lo:",
        "    .byte " + ", ".join(lo_values),
        f"{prefix}_hi:",
        "    .byte " + ", ".join(hi_values),
    ])


def generate(rows: list[str]) -> str:
    left = (SCREEN_WIDTH - len(rows[0])) // 2
    top = 1
    width = len(rows[0])
    height = len(rows)
    dots = sum(ch == "." for row in rows for ch in row)
    power = sum(ch == "o" for row in rows for ch in row)
    walls = sum(ch == "#" for row in rows for ch in row)
    start_x, start_y = find_char(rows, "P")

    glyphs = build_charset()
    sprites = build_sprites()
    charset_bytes = len(glyphs) * 8
    sprite_bytes = len(sprites) * 64

    start_sprite_x = cell_sprite_x(start_x, left)
    start_sprite_y = cell_sprite_y(start_y, top)

    sprite_x_by_cell = [cell_sprite_x(x, left) for x in range(width)]
    sprite_y_by_cell = [cell_sprite_y(y, top) for y in range(height)]

    screen_rows = [cell_screen_addr(0, y, left, top) for y in range(height)]
    color_rows = [COLOR_BASE + (top + y) * SCREEN_WIDTH + left for y in range(height)]
    render_rows = render_char_rows(rows)
    legal_rows = legal_move_masks(rows)

    start_mask = legal_rows[start_y][start_x]
    if start_mask & 0x02:
        start_dir_ptr = SPRITE_PTR_S_OPEN
        start_target_x, start_target_y = start_x, start_y + 1
    elif start_mask & 0x08:
        start_dir_ptr = SPRITE_PTR_E_OPEN
        start_target_x, start_target_y = start_x + 1, start_y
    elif start_mask & 0x04:
        start_dir_ptr = SPRITE_PTR_W_OPEN
        start_target_x, start_target_y = start_x - 1, start_y
    elif start_mask & 0x01:
        start_dir_ptr = SPRITE_PTR_N_OPEN
        start_target_x, start_target_y = start_x, start_y - 1
    else:
        start_dir_ptr = SPRITE_PTR_E_OPEN
        start_target_x, start_target_y = start_x, start_y

    start_target_sprite_x = cell_sprite_x(start_target_x, left)
    start_target_sprite_y = cell_sprite_y(start_target_y, top)

    screen_row_labels = [f"screen_row_{y:02d}" for y in range(height)]
    legal_row_labels = [f"legal_row_{y:02d}" for y in range(height)]
    board_render_row_labels = [f"board_render_row_{y:02d}" for y in range(height)]

    screen_row_data = labelled_byte_rows("screen_row", [[addr & 0xFF for addr in screen_rows]])
    # Replace compact single row with actual labels for address pointer tables.
    screen_label_lines: list[str] = []
    for y, addr in enumerate(screen_rows):
        screen_label_lines.append(f"screen_row_{y:02d}:")
        screen_label_lines.append("    .byte " + ", ".join(byte(0) for _ in range(width)) + f" ; screen base {word(addr)}")

    return f"""; Generated by Lab 010 generate_asm.py.
; Milestone F.2: buffered-turn Pac-Man with visible dot and energizer scoring from verified board.txt.
; Generated assembly is an artifact, not the board authority.

.setcpu "6502"

SCREEN_BASE = {word(SCREEN_BASE)}
COLOR_BASE = {word(COLOR_BASE)}
BOARD_WIDTH = {width}
BOARD_HEIGHT = {height}
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
START_CELL_X = {byte(start_x)}
START_CELL_Y = {byte(start_y)}
START_TARGET_CELL_X = {byte(start_target_x)}
START_TARGET_CELL_Y = {byte(start_target_y)}
START_SPRITE_X_LO = {byte(start_sprite_x & 0xFF)}
START_SPRITE_X_HI = {byte((start_sprite_x >> 8) & 0x01)}
START_SPRITE_Y = {byte(start_sprite_y)}
START_TARGET_SPRITE_X_LO = {byte(start_target_sprite_x & 0xFF)}
START_TARGET_SPRITE_X_HI = {byte((start_target_sprite_x >> 8) & 0x01)}
START_TARGET_SPRITE_Y = {byte(start_target_sprite_y)}
START_DIR_PTR = {byte(start_dir_ptr)}
JOY_PORT_2 = $dc00
JOY_UP = $01
JOY_DOWN = $02
JOY_LEFT = $04
JOY_RIGHT = $08
KEYBOARD_ROW_PORT = $dc00
KEYBOARD_COL_PORT = $dc01
KEY_ROW_ALL = $ff
KEY_ROW_1 = $fd
KEY_ROW_2 = $fb
KEY_W = $02
KEY_A = $04
KEY_S = $20
KEY_D = $04
MASK_UP = $01
MASK_DOWN = $02
MASK_LEFT = $04
MASK_RIGHT = $08
BOARD_PTR = $f7
COLOR_PTR = $f9
SCREEN_PTR = $fb
LEGAL_PTR = $fd

.segment "LOADADDR"

; PRG file load address. C64 PRG files must begin with the little-endian
; address where the following bytes should be loaded.
.word $0801

.segment "EXEHDR"

; BASIC autostart line:
; 10 SYS 2061
;
; With the standard C64 load address at $0801, this header ends at $080d.
; Decimal 2061 is $080d, the first byte of the CODE segment below.
.word basic_line_end
.word 10
.byte $9e, $32, $30, $36, $31, $00
basic_line_end:
.word $0000

.segment "CODE"

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
    jsr init_score
    jsr init_sprite
    jsr init_pacman_state

main_loop:
    jsr delay_frame
    jsr read_input_buffer
    jsr read_keyboard_fallback
    jsr at_target
    beq moving
    jsr commit_target_cell
    jsr choose_next_target_from_buffer
    jsr update_sprite_registers
    jmp main_loop

moving:
    jsr update_mouth_animation
    jsr set_sprite_pointer_current
    jsr move_sprite_toward_target
    jsr update_sprite_registers
    jmp main_loop

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

init_pacman_state:
    lda #START_CELL_X
    sta pac_cell_x
    lda #START_TARGET_CELL_X
    sta target_cell_x
    lda #START_CELL_Y
    sta pac_cell_y
    lda #START_TARGET_CELL_Y
    sta target_cell_y
    lda #START_SPRITE_X_LO
    sta sprite_x_lo
    lda #START_TARGET_SPRITE_X_LO
    sta target_x_lo
    lda #START_SPRITE_X_HI
    sta sprite_x_hi
    lda #START_TARGET_SPRITE_X_HI
    sta target_x_hi
    lda #START_SPRITE_Y
    sta sprite_y
    lda #START_TARGET_SPRITE_Y
    sta target_y
    lda #START_DIR_PTR
    sta target_dir_ptr
    sta requested_dir_ptr
    lda #$00
    sta mouth_counter
    sta mouth_phase
    jsr set_sprite_pointer_current
    jsr update_sprite_registers
    rts

commit_target_cell:
    lda target_cell_x
    sta pac_cell_x
    lda target_cell_y
    sta pac_cell_y
    jsr erase_current_cell
    rts

init_score:
    lda #$30
    ldx #$00
init_score_loop:
    sta score_digits,x
    inx
    cpx #$06
    bne init_score_loop
    jsr render_score
    rts

render_score:
    lda #$13
    sta $0401
    lda #$03
    sta $0402
    lda #$0f
    sta $0403
    lda #$12
    sta $0404
    lda #$05
    sta $0405
    lda #$20
    sta $0406
    ldx #$00
render_score_digit_loop:
    lda score_digits,x
    sta $0407,x
    inx
    cpx #$06
    bne render_score_digit_loop
    rts

add_score_10:
    jsr score_increment_tens
    jsr render_score
    rts

add_score_50:
    jsr score_increment_tens
    jsr score_increment_tens
    jsr score_increment_tens
    jsr score_increment_tens
    jsr score_increment_tens
    jsr render_score
    rts

score_increment_tens:
    ldx #$04
score_increment_digit:
    inc score_digits,x
    lda score_digits,x
    cmp #$3a
    bne score_increment_done
    lda #$30
    sta score_digits,x
    dex
    bpl score_increment_digit
score_increment_done:
    rts

read_input_buffer:
    lda JOY_PORT_2
    sta joystick_state

    lda joystick_state
    and #JOY_LEFT
    beq buffer_left

    lda joystick_state
    and #JOY_RIGHT
    beq buffer_right

    lda joystick_state
    and #JOY_UP
    beq buffer_up

    lda joystick_state
    and #JOY_DOWN
    beq buffer_down

    rts

buffer_left:
    lda #SPRITE_PTR_W_OPEN
    sta requested_dir_ptr
    rts

buffer_right:
    lda #SPRITE_PTR_E_OPEN
    sta requested_dir_ptr
    rts

buffer_up:
    lda #SPRITE_PTR_N_OPEN
    sta requested_dir_ptr
    rts

buffer_down:
    lda #SPRITE_PTR_S_OPEN
    sta requested_dir_ptr
    rts

read_keyboard_fallback:
    lda #KEY_ROW_1
    sta KEYBOARD_ROW_PORT
    lda KEYBOARD_COL_PORT
    sta keyboard_row_state

    lda keyboard_row_state
    and #KEY_W
    beq keyboard_buffer_up

    lda keyboard_row_state
    and #KEY_A
    beq keyboard_buffer_left

    lda keyboard_row_state
    and #KEY_S
    beq keyboard_buffer_down

    lda #KEY_ROW_2
    sta KEYBOARD_ROW_PORT
    lda KEYBOARD_COL_PORT
    sta keyboard_row_state

    lda keyboard_row_state
    and #KEY_D
    beq keyboard_buffer_right

    lda #KEY_ROW_ALL
    sta KEYBOARD_ROW_PORT
    rts

keyboard_buffer_up:
    lda #SPRITE_PTR_N_OPEN
    sta requested_dir_ptr
    lda #KEY_ROW_ALL
    sta KEYBOARD_ROW_PORT
    rts

keyboard_buffer_left:
    lda #SPRITE_PTR_W_OPEN
    sta requested_dir_ptr
    lda #KEY_ROW_ALL
    sta KEYBOARD_ROW_PORT
    rts

keyboard_buffer_down:
    lda #SPRITE_PTR_S_OPEN
    sta requested_dir_ptr
    lda #KEY_ROW_ALL
    sta KEYBOARD_ROW_PORT
    rts

keyboard_buffer_right:
    lda #SPRITE_PTR_E_OPEN
    sta requested_dir_ptr
    lda #KEY_ROW_ALL
    sta KEYBOARD_ROW_PORT
    rts

choose_next_target_from_buffer:
    lda requested_dir_ptr
    cmp #SPRITE_PTR_W_OPEN
    beq try_requested_left
    cmp #SPRITE_PTR_E_OPEN
    beq try_requested_right
    cmp #SPRITE_PTR_N_OPEN
    beq try_requested_up
    cmp #SPRITE_PTR_S_OPEN
    beq try_requested_down
    jmp continue_current_direction

try_requested_left:
    jsr load_legal_mask
    and #MASK_LEFT
    beq continue_current_direction
    lda pac_cell_x
    sec
    sbc #$01
    sta target_cell_x
    lda pac_cell_y
    sta target_cell_y
    lda #SPRITE_PTR_W_OPEN
    sta target_dir_ptr
    jsr set_target_sprite_from_cell
    rts

try_requested_right:
    jsr load_legal_mask
    and #MASK_RIGHT
    beq continue_current_direction
    lda pac_cell_x
    clc
    adc #$01
    sta target_cell_x
    lda pac_cell_y
    sta target_cell_y
    lda #SPRITE_PTR_E_OPEN
    sta target_dir_ptr
    jsr set_target_sprite_from_cell
    rts

try_requested_up:
    jsr load_legal_mask
    and #MASK_UP
    beq continue_current_direction
    lda pac_cell_x
    sta target_cell_x
    lda pac_cell_y
    sec
    sbc #$01
    sta target_cell_y
    lda #SPRITE_PTR_N_OPEN
    sta target_dir_ptr
    jsr set_target_sprite_from_cell
    rts

try_requested_down:
    jsr load_legal_mask
    and #MASK_DOWN
    beq continue_current_direction
    lda pac_cell_x
    sta target_cell_x
    lda pac_cell_y
    clc
    adc #$01
    sta target_cell_y
    lda #SPRITE_PTR_S_OPEN
    sta target_dir_ptr
    jsr set_target_sprite_from_cell
    rts

continue_current_direction:
    lda target_dir_ptr
    cmp #SPRITE_PTR_W_OPEN
    beq try_current_left
    cmp #SPRITE_PTR_E_OPEN
    beq try_current_right
    cmp #SPRITE_PTR_N_OPEN
    beq try_current_up
    cmp #SPRITE_PTR_S_OPEN
    beq try_current_down
    rts

try_current_left:
    jsr load_legal_mask
    and #MASK_LEFT
    beq stop_at_cell_center
    lda pac_cell_x
    sec
    sbc #$01
    sta target_cell_x
    lda pac_cell_y
    sta target_cell_y
    lda #SPRITE_PTR_W_OPEN
    sta target_dir_ptr
    jsr set_target_sprite_from_cell
    rts

try_current_right:
    jsr load_legal_mask
    and #MASK_RIGHT
    beq stop_at_cell_center
    lda pac_cell_x
    clc
    adc #$01
    sta target_cell_x
    lda pac_cell_y
    sta target_cell_y
    lda #SPRITE_PTR_E_OPEN
    sta target_dir_ptr
    jsr set_target_sprite_from_cell
    rts

try_current_up:
    jsr load_legal_mask
    and #MASK_UP
    beq stop_at_cell_center
    lda pac_cell_x
    sta target_cell_x
    lda pac_cell_y
    sec
    sbc #$01
    sta target_cell_y
    lda #SPRITE_PTR_N_OPEN
    sta target_dir_ptr
    jsr set_target_sprite_from_cell
    rts

try_current_down:
    jsr load_legal_mask
    and #MASK_DOWN
    beq stop_at_cell_center
    lda pac_cell_x
    sta target_cell_x
    lda pac_cell_y
    clc
    adc #$01
    sta target_cell_y
    lda #SPRITE_PTR_S_OPEN
    sta target_dir_ptr
    jsr set_target_sprite_from_cell
    rts

stop_at_cell_center:
    rts

load_legal_mask:
    ldx pac_cell_y
    lda legal_row_lo,x
    sta LEGAL_PTR
    lda legal_row_hi,x
    sta LEGAL_PTR+1
    ldy pac_cell_x
    lda (LEGAL_PTR),y
    rts

set_target_sprite_from_cell:
    ldx target_cell_x
    lda sprite_x_lo_by_cell,x
    sta target_x_lo
    lda sprite_x_hi_by_cell,x
    sta target_x_hi
    ldx target_cell_y
    lda sprite_y_by_cell,x
    sta target_y
    rts

set_sprite_pointer_current:
    lda target_dir_ptr
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

erase_current_cell:
    ldx pac_cell_y
    lda screen_addr_row_lo,x
    sta SCREEN_PTR
    lda screen_addr_row_hi,x
    sta SCREEN_PTR+1
    ldy pac_cell_x
    lda (SCREEN_PTR),y
    cmp #$11
    beq score_small_dot
    cmp #$12
    beq score_power_dot
    rts
score_small_dot:
    lda #$00
    sta (SCREEN_PTR),y
    jsr add_score_10
    rts
score_power_dot:
    lda #$00
    sta (SCREEN_PTR),y
    jsr add_score_50
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
    sta SCREEN_BASE,x
    sta SCREEN_BASE+$0100,x
    sta SCREEN_BASE+$0200,x
    sta SCREEN_BASE+$0300,x
    sta COLOR_BASE,x
    sta COLOR_BASE+$0100,x
    sta COLOR_BASE+$0200,x
    sta COLOR_BASE+$0300,x
    inx
    bne clear_loop
    rts

render_board:
    ldx #$00
render_board_row_loop:
    stx render_row_index
    lda board_render_row_lo,x
    sta BOARD_PTR
    lda board_render_row_hi,x
    sta BOARD_PTR+1
    lda screen_addr_row_lo,x
    sta SCREEN_PTR
    lda screen_addr_row_hi,x
    sta SCREEN_PTR+1
    lda color_addr_row_lo,x
    sta COLOR_PTR
    lda color_addr_row_hi,x
    sta COLOR_PTR+1
    ldy #$00
render_board_col_loop:
    lda (BOARD_PTR),y
    beq render_board_skip_cell
    sta (SCREEN_PTR),y
    cmp #$11
    bcs render_board_yellow
    lda #$06
    jmp render_board_store_color
render_board_yellow:
    lda #$07
render_board_store_color:
    sta (COLOR_PTR),y
render_board_skip_cell:
    iny
    cpy #BOARD_WIDTH
    bne render_board_col_loop
    ldx render_row_index
    inx
    cpx #BOARD_HEIGHT
    bne render_board_row_loop
    rts

pac_cell_x:
    .byte $00
pac_cell_y:
    .byte $00
target_cell_x:
    .byte $00
target_cell_y:
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
target_dir_ptr:
    .byte $00
requested_dir_ptr:
    .byte $00
joystick_state:
    .byte $ff
keyboard_row_state:
    .byte $ff
render_row_index:
    .byte $00
score_digits:
    .byte $30, $30, $30, $30, $30, $30
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

; Compact board-render character rows generated from board.txt.
; Zero entries are skipped because clear_screen already initialized blank black cells.
board_render_rows:
{labelled_byte_rows("board_render_row", render_rows)}

{row_address_tables("board_render_row", board_render_row_labels)}

; Joystick legality masks generated from board.txt.
; bit 0 = up, bit 1 = down, bit 2 = left, bit 3 = right
legal_move_rows:
{labelled_byte_rows("legal_row", legal_rows)}

{row_address_tables("legal_row", legal_row_labels)}

; Screen and color row base addresses for compact rendering and dot clearing.
screen_addr_row_lo:
    .byte {", ".join(byte(addr & 0xFF) for addr in screen_rows)}
screen_addr_row_hi:
    .byte {", ".join(byte(addr >> 8) for addr in screen_rows)}
color_addr_row_lo:
    .byte {", ".join(byte(addr & 0xFF) for addr in color_rows)}
color_addr_row_hi:
    .byte {", ".join(byte(addr >> 8) for addr in color_rows)}

; Sprite coordinate projection tables.
sprite_x_lo_by_cell:
    .byte {", ".join(byte(value & 0xFF) for value in sprite_x_by_cell)}
sprite_x_hi_by_cell:
    .byte {", ".join(byte((value >> 8) & 0x01) for value in sprite_x_by_cell)}
sprite_y_by_cell:
    .byte {", ".join(byte(value) for value in sprite_y_by_cell)}

; Board text audit authority remains in src/board.txt and src/projected_board.json.
; Runtime board rendering uses compact board_render_row_* tables above.
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

    start_x, start_y = find_char(rows, "P")

    intent = {
        "schemaVersion": 6,
        "milestone": "pacman_buffered_turn_keyboard_fallback_control",
        "authority": {
            "boardText": str(board_path),
            "projectedBoard": str(meta_path),
            "generatedAssemblyIsArtifact": True,
            "movementAuthority": "board.txt traversable cells"
        },
        "inputs": {
            "goal": goal_path.read_text().strip().splitlines(),
            "program": program_path.read_text().strip().splitlines()
        },
        "board": {
            "width": len(rows[0]),
            "height": len(rows),
            "walls": sum(ch == "#" for row in rows for ch in row),
            "dots": sum(ch == "." for row in rows for ch in row),
            "powerDots": sum(ch == "o" for row in rows for ch in row),
            "pacmanStart": {"x": start_x, "y": start_y},
            "ghostStarts": [
                {"x": x, "y": y}
                for y, row in enumerate(rows)
                for x, ch in enumerate(row)
                if ch == "G"
            ]
        },
        "characterProjection": {
            "blankChar": 0,
            "wallGlyphRange": [1, 16],
            "centeredDotChar": 17,
            "centeredPowerDotChar": 18,
            "wallGlyphSelection": "neighbor_aware_thin_wall"
        },
        "scoring": {
            "enabled": True,
            "scoreStartsAt": 0,
            "smallDot": 10,
            "energizer": 50,
            "scoreOncePerConsumedCell": True,
            "visibleScore": True,
            "scoreStorage": "six screen-code decimal digits",
            "scoreTrigger": "Pac-Man reaches a board-cell center containing an unconsumed dot or energizer",
            "mutableItemMap": "rendered character board because Pac-Man is a hardware sprite"
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
            "mouthDirection": "hardware sprite pointer selected from current buffered-turn movement direction",
            "mouthAnimation": "open and closed sprite frames alternate at a visible crunch pace while moving",
            "mouthSpeedTuning": "toggle every 8 frame-pixel updates",
            "verticalSpriteArt": "north/south mouth uses same radial sprite geometry as east/west",
            "spriteFootprint": "all directions use shared center, shared radius, and shared mouth-wedge rule",
            "spriteGeometry": "radial Pac-Man generated from one circle-like pixel model",
            "spriteOriginTuning": "sprite y origin lowered by one pixel and x origin shifted left by three pixels for hallway centering",
            "spriteCopyFix": "copies all 512 bytes for eight sprite frames",
            "speedTuning": "two raster frames per interpolated pixel"
        },
        "joystickControl": {
            "enabled": True,
            "port": "$dc00",
            "portName": "joystick port 2",
            "activeLow": True,
            "directionBits": {
                "up": 1,
                "down": 2,
                "left": 4,
                "right": 8
            },
            "movementPolicy": "Pac-Man starts moving immediately, continues in the current legal direction, and applies buffered joystick or keyboard requested turns when legal at cell centers",
            "wallPolicy": "blocked requested turns are ignored; if current momentum is blocked and no buffered legal turn exists, Pac-Man stops",
            "legalitySource": "legal move masks generated from board.txt traversable cells",
            "keyboardFallback": "W/A/S/D keys update the same requested direction buffer as joystick input"
        },
        "pacmanPathWalker": {
            "movementAuthority": "board.txt traversable cells",
            "traversableCells": [".", "o", " ", "P", "G"],
            "blockedCells": ["#", "X"],
            "turnPolicy": "buffered joystick or keyboard requested legal turn, otherwise continue current legal direction",
            "deadEndPolicy": "start with a legal first target; continue current direction; stop at a cell center when current direction is blocked and no buffered legal turn exists",
            "failurePolicy": "runtime ignores blocked requested turns"
        },
        "assemblyEfficiency": {
            "renderer": "table-driven board renderer",
            "unrolledBoardWrites": False,
            "auditBoardTextInAssembly": False,
            "dataSource": "compact board_render_row tables generated from board.txt",
            "colorPolicy": "derive blue/yellow color from compact render character value"
        },
    }

    intent_path.write_text(json.dumps(intent, indent=2) + "\n")
    print(f"Generated {asm_path} from {board_path}")
    print(f"Generated {intent_path} from {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
