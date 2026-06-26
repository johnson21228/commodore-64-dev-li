#!/usr/bin/env python3
"""Generate an arcade-optimized ca65 C64 Pac-Man bounce app from language.

Lab 010 proves a two-language front end:

    goal.lang      -> declares the app goal and constraints
    program.lang   -> implements the goal in a controlled language
    generated.s    -> assembly app source; no main.c is produced or consumed

The runtime mouth direction is vector-owned and speed-oriented:

* dx_vel/dy_vel are the movement truth.
* A compact direction_index caches E/NE/N/NW/W/SW/S/SE.
* direction_index is recomputed only when a bounce changes dx_vel or dy_vel.
* mouth_dirty marks when the VIC sprite pointer could need updating.
* apply_mouth_pointer_if_dirty_01 uses mouth_pointer_table_01,x and avoids
  writing $07f8 every frame.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

COLOR = {
    "black": 0, "white": 1, "red": 2, "cyan": 3, "purple": 4, "green": 5,
    "blue": 6, "yellow": 7, "orange": 8, "brown": 9, "light red": 10,
    "dark gray": 11, "gray": 12, "light green": 13, "light blue": 14,
    "light gray": 15,
}

DIRECTIONS = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
DIRECTION_INDEX = {name: idx for idx, name in enumerate(DIRECTIONS)}
DIRECTION_ANGLE = {
    "E": 0.0,
    "NE": -math.pi / 4.0,
    "N": -math.pi / 2.0,
    "NW": -3.0 * math.pi / 4.0,
    "W": math.pi,
    "SW": 3.0 * math.pi / 4.0,
    "S": math.pi / 2.0,
    "SE": math.pi / 4.0,
}

GOAL_RE = re.compile(r'^goal "([A-Z0-9 ,.:!.?\\-]+)"$')
IMPLEMENTS_RE = re.compile(r'^implements goal "([A-Z0-9 ,.:!.?\\-]+)"$')
SPRITE_RE = re.compile(r'^use yellow pacman sprite at x ([0-9]{1,3}) y ([0-9]{1,3})$')
VELOCITY_RE = re.compile(r'^move sprite velocity dx (-?[0-9]{1,2}) dy (-?[0-9]{1,2})$')
BOUNDS_RE = re.compile(r'^bounds x ([0-9]{1,3}) ([0-9]{1,3}) y ([0-9]{1,3}) ([0-9]{1,3})$')


def parse_goal_line(line: str, line_no: int) -> dict:
    raw = line.strip()
    if not raw or raw.startswith('#'):
        return {"op": "comment", "line": line_no, "source": line.rstrip('\n')}
    match = GOAL_RE.match(raw)
    if match:
        return {"op": "goal", "line": line_no, "source": raw, "name": match.group(1)}
    if raw == 'priority runtime speed first':
        return {"op": "priority", "line": line_no, "source": raw, "value": "runtime_speed_first"}
    if raw == 'output assembly':
        return {"op": "output", "line": line_no, "source": raw, "value": "assembly"}
    if raw == 'constraint no main.c':
        return {"op": "constraint", "line": line_no, "source": raw, "value": "no_main_c"}
    if raw == 'constraint generated assembly is the app':
        return {"op": "constraint", "line": line_no, "source": raw, "value": "generated_assembly_is_app"}
    if raw == 'visual yellow pac-man sprite':
        return {"op": "visual", "line": line_no, "source": raw, "subject": "yellow_pacman_sprite"}
    if raw == 'animation crunching mouth opens and closes':
        return {"op": "animation_goal", "line": line_no, "source": raw, "model": "pacman_mouth_crunch"}
    if raw in {'animation mouth faces dx/dy movement vector', 'animation mouth faces movement vector', 'animation mouth faces horizontal direction of motion'}:
        return {"op": "animation_goal", "line": line_no, "source": raw, "model": "pacman_mouth_faces_dxdy_vector"}
    if raw == 'motion linear path':
        return {"op": "motion", "line": line_no, "source": raw, "model": "linear_path"}
    if raw == 'bounce screen edges with incidence angle equals outgoing angle':
        return {"op": "bounce_goal", "line": line_no, "source": raw, "model": "reflect_edges_equal_angle"}
    raise ValueError(f"goal line {line_no}: unknown command {raw!r}")


def parse_goal(text: str) -> list[dict]:
    return [parse_goal_line(line, n) for n, line in enumerate(text.splitlines(), start=1)]


def parse_program_line(line: str, line_no: int) -> dict:
    raw = line.strip()
    if not raw or raw.startswith('#'):
        return {"op": "comment", "line": line_no, "source": line.rstrip('\n')}
    match = IMPLEMENTS_RE.match(raw)
    if match:
        return {"op": "implements_goal", "line": line_no, "source": raw, "goal": match.group(1)}
    if raw == 'optimize for speed':
        return {"op": "optimize", "line": line_no, "source": raw, "strategy": "runtime_speed_first"}
    for prefix, op, register in [("set border ", "set_border", "$d020"), ("set background ", "set_background", "$d021")]:
        if raw.startswith(prefix):
            color_name = raw[len(prefix):]
            if color_name not in COLOR:
                raise ValueError(f"line {line_no}: unsupported color {color_name!r}")
            return {"op": op, "line": line_no, "source": raw, "color": color_name, "value": COLOR[color_name], "register": register}
    if raw.startswith('clear screen color '):
        color_name = raw[len('clear screen color '):]
        if color_name not in COLOR:
            raise ValueError(f"line {line_no}: unsupported color {color_name!r}")
        return {"op": "clear_screen", "line": line_no, "source": raw, "color": color_name, "color_value": COLOR[color_name], "strategy": "exact_1000_byte_y_loop"}
    match = SPRITE_RE.match(raw)
    if match:
        x, y = map(int, match.groups())
        return {"op": "use_pacman_sprite", "line": line_no, "source": raw, "color": "yellow", "color_value": COLOR['yellow'], "x": x, "y": y}
    if raw == 'animate mouth crunch every 8 frames':
        return {"op": "animate_mouth", "line": line_no, "source": raw, "model": "toggle_sprite_frame", "period_frames": 8}
    if raw in {'face mouth with dx/dy vector', 'face mouth from dx/dy vector', 'face mouth left/right with dx'}:
        return {"op": "face_mouth_with_vector", "line": line_no, "source": raw, "model": "cached_direction_index_pointer_table", "directions": DIRECTIONS}
    match = VELOCITY_RE.match(raw)
    if match:
        dx, dy = map(int, match.groups())
        if dx == 0 and dy == 0:
            raise ValueError(f"line {line_no}: velocity cannot be zero in both axes")
        if dx < -8 or dx > 8 or dy < -8 or dy > 8:
            raise ValueError(f"line {line_no}: velocity outside allowed -8..8 range")
        return {"op": "move_sprite_velocity", "line": line_no, "source": raw, "dx": dx, "dy": dy, "dx_byte": dx & 0xFF, "dy_byte": dy & 0xFF}
    match = BOUNDS_RE.match(raw)
    if match:
        min_x, max_x, min_y, max_y = map(int, match.groups())
        if not (0 <= min_x < max_x <= 255 and 0 <= min_y < max_y <= 255):
            raise ValueError(f"line {line_no}: bounds must fit unsigned byte sprite registers")
        return {"op": "bounds", "line": line_no, "source": raw, "min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}
    if raw == 'bounce reflect at screen edge':
        return {"op": "bounce_reflect", "line": line_no, "source": raw, "model": "invert_axis_velocity_on_boundary"}
    if raw == 'loop forever':
        return {"op": "loop_forever", "line": line_no, "source": raw}
    raise ValueError(f"program line {line_no}: unknown command {raw!r}")


def parse_program(text: str) -> list[dict]:
    return [parse_program_line(line, n) for n, line in enumerate(text.splitlines(), start=1)]


def singleton(items: list[dict], op: str) -> dict:
    found = [item for item in items if item.get('op') == op]
    if len(found) != 1:
        raise ValueError(f"expected exactly one {op}, found {len(found)}")
    return found[0]


def goal_name(goal: list[dict]) -> str:
    return singleton(goal, 'goal')['name']


def validate_goal_program(goal: list[dict], program: list[dict]) -> None:
    name = goal_name(goal)
    implemented = [item['goal'] for item in program if item.get('op') == 'implements_goal']
    if implemented != [name]:
        raise ValueError(f"program.lang must implement exactly goal {name!r}")
    if [item.get('value') for item in goal if item.get('op') == 'priority'] != ['runtime_speed_first']:
        raise ValueError('goal.lang must declare priority runtime speed first')
    if [item.get('value') for item in goal if item.get('op') == 'output'] != ['assembly']:
        raise ValueError('goal.lang must declare output assembly')
    constraints = {item.get('value') for item in goal if item.get('op') == 'constraint'}
    if not {'no_main_c', 'generated_assembly_is_app'}.issubset(constraints):
        raise ValueError('goal.lang missing required no-main.c/generated-assembly constraints')
    if not any(item.get('subject') == 'yellow_pacman_sprite' for item in goal):
        raise ValueError('goal.lang must request a yellow pac-man sprite visual')
    if not any(item.get('model') == 'pacman_mouth_crunch' for item in goal):
        raise ValueError('goal.lang must request crunching mouth animation')
    if not any(item.get('model') == 'pacman_mouth_faces_dxdy_vector' for item in goal):
        raise ValueError('goal.lang must request mouth facing dx/dy movement vector')
    if not any(item.get('model') == 'linear_path' for item in goal):
        raise ValueError('goal.lang must request linear path motion')
    if not any(item.get('model') == 'reflect_edges_equal_angle' for item in goal):
        raise ValueError('goal.lang must request incidence-angle reflection at edges')
    for op in ['optimize', 'set_border', 'set_background', 'clear_screen', 'use_pacman_sprite', 'animate_mouth', 'face_mouth_with_vector', 'move_sprite_velocity', 'bounds', 'bounce_reflect', 'loop_forever']:
        singleton(program, op)
    sprite = singleton(program, 'use_pacman_sprite')
    bounds = singleton(program, 'bounds')
    if not (bounds['min_x'] <= sprite['x'] <= bounds['max_x'] and bounds['min_y'] <= sprite['y'] <= bounds['max_y']):
        raise ValueError('initial sprite position must be inside bounds')


def hexbyte(value: int) -> str:
    return f"${value & 0xFF:02x}"


def direction_from_vector(dx: int, dy: int) -> str:
    if dx > 0 and dy < 0: return 'NE'
    if dx < 0 and dy < 0: return 'NW'
    if dx < 0 and dy > 0: return 'SW'
    if dx > 0 and dy > 0: return 'SE'
    if dx > 0: return 'E'
    if dx < 0: return 'W'
    if dy < 0: return 'N'
    if dy > 0: return 'S'
    return 'E'


def _angle_delta(a: float, b: float) -> float:
    return abs((a - b + math.pi) % (2.0 * math.pi) - math.pi)


def pacman_frame(direction: str | None) -> list[int]:
    """Return a 24x21 single-color C64 sprite frame packed into 64 bytes."""
    if direction is not None and direction not in DIRECTIONS:
        raise ValueError(f'unknown direction {direction!r}')
    rows: list[list[int]] = []
    center_x = 11.5
    center_y = 10.0
    radius_x = 10.8
    radius_y = 9.6
    wedge_angle = math.radians(34)
    target = DIRECTION_ANGLE.get(direction or 'E', 0.0)
    for y in range(21):
        row: list[int] = []
        for x in range(24):
            nx = (x - center_x) / radius_x
            ny = (y - center_y) / radius_y
            inside = (nx * nx + ny * ny) <= 1.0
            if inside and direction is not None:
                angle = math.atan2(y - center_y, x - center_x)
                distance = math.hypot(x - center_x, y - center_y)
                if distance > 3.0 and _angle_delta(angle, target) <= wedge_angle:
                    inside = False
            row.append(1 if inside else 0)
        rows.append(row)

    data: list[int] = []
    for row in rows:
        for group in range(3):
            byte = 0
            for bit in range(8):
                byte = (byte << 1) | row[group * 8 + bit]
            data.append(byte)
    data.append(0x00)
    if len(data) != 64:
        raise ValueError('C64 sprite frame must contain 64 bytes')
    return data


PACMAN_CLOSED_BYTES = pacman_frame(None)
PACMAN_OPEN_BYTES = {direction: pacman_frame(direction) for direction in DIRECTIONS}


def emit_fast_clear(lines: list[str], color_value: int) -> None:
    lines.extend([
        '    ; exact 1000-byte clear: four 250-byte stripes, no overlap',
        '    ldy #250',
        'fast_clear_loop_01:',
        '    lda #SPACE_CHAR',
        '    sta SCREEN_RAM-1,y',
        '    sta SCREEN_RAM+249,y',
        '    sta SCREEN_RAM+499,y',
        '    sta SCREEN_RAM+749,y',
        f'    lda #{hexbyte(color_value)}',
        '    sta COLOR_RAM-1,y',
        '    sta COLOR_RAM+249,y',
        '    sta COLOR_RAM+499,y',
        '    sta COLOR_RAM+749,y',
        '    dey',
        '    bne fast_clear_loop_01',
    ])


def sprite_const_lines() -> list[str]:
    return [
        'SPRITE_DATA_CLOSED = $2000',
        'SPRITE_DATA_OPEN_E = $2040',
        'SPRITE_DATA_OPEN_NE = $2080',
        'SPRITE_DATA_OPEN_N = $20c0',
        'SPRITE_DATA_OPEN_NW = $2100',
        'SPRITE_DATA_OPEN_W = $2140',
        'SPRITE_DATA_OPEN_SW = $2180',
        'SPRITE_DATA_OPEN_S = $21c0',
        'SPRITE_DATA_OPEN_SE = $2200',
        'SPRITE_DATA_POINTER_CLOSED = $80',
        'SPRITE_DATA_POINTER_OPEN_E = $81',
        'SPRITE_DATA_POINTER_OPEN_NE = $82',
        'SPRITE_DATA_POINTER_OPEN_N = $83',
        'SPRITE_DATA_POINTER_OPEN_NW = $84',
        'SPRITE_DATA_POINTER_OPEN_W = $85',
        'SPRITE_DATA_POINTER_OPEN_SW = $86',
        'SPRITE_DATA_POINTER_OPEN_S = $87',
        'SPRITE_DATA_POINTER_OPEN_SE = $88',
        'DIR_E = $00',
        'DIR_NE = $01',
        'DIR_N = $02',
        'DIR_NW = $03',
        'DIR_W = $04',
        'DIR_SW = $05',
        'DIR_S = $06',
        'DIR_SE = $07',
        'FRAME_CLOSED = $00',
        'FRAME_OPEN_BASE = $01',
    ]


def emit_asm(goal: list[dict], program: list[dict]) -> str:
    name = goal_name(goal)
    sprite = singleton(program, 'use_pacman_sprite')
    velocity = singleton(program, 'move_sprite_velocity')
    bounds = singleton(program, 'bounds')
    border = singleton(program, 'set_border')
    background = singleton(program, 'set_background')
    clear = singleton(program, 'clear_screen')
    min_x, max_x = bounds['min_x'], bounds['max_x']
    min_y, max_y = bounds['min_y'], bounds['max_y']
    dx, dy = velocity['dx'], velocity['dy']
    initial_direction = direction_from_vector(dx, dy)
    initial_direction_index = DIRECTION_INDEX[initial_direction]

    lines: list[str] = [
        '; Generated by labs/010_goal_language_to_asm_pacman_bounce/src/generate_asm.py',
        '; Goal source: labs/010_goal_language_to_asm_pacman_bounce/src/goal.lang',
        '; Program source: labs/010_goal_language_to_asm_pacman_bounce/src/program.lang',
        f'; Goal: {name}',
        '; No main.c is generated or consumed.',
        '; Motion: linear path; edge bounce reflects by inverting only the hit axis velocity.',
        '; Reflection: left/right edge -> dx = -dx; top/bottom edge -> dy = -dy.',
        '; Arcade optimized mouth path:',
        '; - direction_index caches direction_from_vector(dx_vel, dy_vel).',
        '; - refresh_direction_index_01 runs only after a bounce changes dx_vel/dy_vel.',
        '; - mouth_dirty gates writes to SPRITE_POINTER_0 at $07f8.',
        '; - mouth_pointer_table_01 maps closed/open-vector frames without an open-frame branch chain.',
        '; Open mouth frames: E, NE, N, NW, W, SW, S, SE.',
        '.import __EXEHDR__',
        '.export _main',
        '',
        'SCREEN_RAM = $0400',
        'COLOR_RAM = $d800',
        'SPACE_CHAR = $20',
        'SPRITE_POINTER_0 = $07f8',
        'SPRITE_DATA = $2000',
    ]
    lines.extend(sprite_const_lines())
    lines.extend([
        'VIC_SPRITE0_X = $d000',
        'VIC_SPRITE0_Y = $d001',
        'SPRITE_X_MSB = $d010',
        'SPRITE_ENABLE = $d015',
        'VIC_CONTROL_1 = $d011',
        'RASTER = $d012',
        'SPRITE0_COLOR = $d027',
        'BORDER_COLOR = $d020',
        'BACKGROUND_COLOR = $d021',
        f'MIN_X = {hexbyte(min_x)}',
        f'MAX_X = {hexbyte(max_x)}',
        f'MIN_Y = {hexbyte(min_y)}',
        f'MAX_Y = {hexbyte(max_y)}',
        f'DX_POS = {hexbyte(abs(dx))}',
        f'DX_NEG = {hexbyte((-abs(dx)) & 0xff)}',
        f'DY_POS = {hexbyte(abs(dy))}',
        f'DY_NEG = {hexbyte((-abs(dy)) & 0xff)}',
        f'INITIAL_DIRECTION_INDEX = {hexbyte(initial_direction_index)}',
        '',
        '.segment "STARTUP"',
        '_main:',
        '    ; speed-first generated setup from goal/program language',
        f'    lda #{hexbyte(border["value"])}',
        '    sta BORDER_COLOR',
        f'    lda #{hexbyte(background["value"])}',
        '    sta BACKGROUND_COLOR',
    ])
    emit_fast_clear(lines, clear['color_value'])
    lines.extend([
        '',
        '    ; copy generated closed plus eight vector-facing open-mouth frames once',
        '    ldx #$3f',
        'copy_pacman_sprite_01:',
        '    lda pacman_sprite_closed_data,x',
        '    sta SPRITE_DATA_CLOSED,x',
        '    lda pacman_sprite_open_e_data,x',
        '    sta SPRITE_DATA_OPEN_E,x',
        '    lda pacman_sprite_open_ne_data,x',
        '    sta SPRITE_DATA_OPEN_NE,x',
        '    lda pacman_sprite_open_n_data,x',
        '    sta SPRITE_DATA_OPEN_N,x',
        '    lda pacman_sprite_open_nw_data,x',
        '    sta SPRITE_DATA_OPEN_NW,x',
        '    lda pacman_sprite_open_w_data,x',
        '    sta SPRITE_DATA_OPEN_W,x',
        '    lda pacman_sprite_open_sw_data,x',
        '    sta SPRITE_DATA_OPEN_SW,x',
        '    lda pacman_sprite_open_s_data,x',
        '    sta SPRITE_DATA_OPEN_S,x',
        '    lda pacman_sprite_open_se_data,x',
        '    sta SPRITE_DATA_OPEN_SE,x',
        '    dex',
        '    bpl copy_pacman_sprite_01',
        '',
        '    ; color and enable sprite 0',
        f'    lda #{hexbyte(sprite["color_value"])}',
        '    sta SPRITE0_COLOR',
        '    lda #$01',
        '    sta SPRITE_ENABLE',
        '    lda #$00',
        '    sta SPRITE_X_MSB',
        '',
        f'    lda #{hexbyte(sprite["x"])}',
        '    sta x_pos',
        f'    lda #{hexbyte(sprite["y"])}',
        '    sta y_pos',
        f'    lda #{hexbyte(velocity["dx_byte"])}',
        '    sta dx_vel',
        f'    lda #{hexbyte(velocity["dy_byte"])}',
        '    sta dy_vel',
        '    lda #INITIAL_DIRECTION_INDEX',
        '    sta direction_index',
        '    lda #$ff',
        '    sta current_mouth_frame',
        '    lda #$01',
        '    sta mouth_dirty',
        '    lda #$00',
        '    sta mouth_timer',
        '    sta mouth_state',
        '    jsr apply_mouth_pointer_if_dirty_01',
        '    jsr update_sprite_01',
        '',
        'main_loop_01:',
        '    jsr wait_frame_01',
        '',
        '    ; x = x + dx; reflect at left/right boundaries',
        '    lda x_pos',
        '    clc',
        '    adc dx_vel',
        '    sta x_pos',
        '    cmp #MIN_X',
        '    bcs check_right_edge_01',
        'hit_left_edge_01:',
        '    lda #MIN_X',
        '    sta x_pos',
        '    lda #DX_POS',
        '    sta dx_vel',
        '    jsr refresh_direction_index_01',
        '    jmp update_y_01',
        'check_right_edge_01:',
        '    cmp #MAX_X',
        '    bcc update_y_01',
        'hit_right_edge_01:',
        '    lda #MAX_X',
        '    sta x_pos',
        '    lda #DX_NEG',
        '    sta dx_vel',
        '    jsr refresh_direction_index_01',
        '',
        'update_y_01:',
        '    ; y = y + dy; reflect at top/bottom boundaries',
        '    lda y_pos',
        '    clc',
        '    adc dy_vel',
        '    sta y_pos',
        '    cmp #MIN_Y',
        '    bcs check_bottom_edge_01',
        'hit_top_edge_01:',
        '    lda #MIN_Y',
        '    sta y_pos',
        '    lda #DY_POS',
        '    sta dy_vel',
        '    jsr refresh_direction_index_01',
        '    jmp draw_sprite_01',
        'check_bottom_edge_01:',
        '    cmp #MAX_Y',
        '    bcc draw_sprite_01',
        'hit_bottom_edge_01:',
        '    lda #MAX_Y',
        '    sta y_pos',
        '    lda #DY_NEG',
        '    sta dy_vel',
        '    jsr refresh_direction_index_01',
        '',
        'draw_sprite_01:',
        '    jsr animate_mouth_01',
        '    jsr apply_mouth_pointer_if_dirty_01',
        '    jsr update_sprite_01',
        '    jmp main_loop_01',
        '',
        'animate_mouth_01:',
        '    inc mouth_timer',
        '    lda mouth_timer',
        '    and #$07',
        '    bne mouth_done_01',
        '    lda mouth_state',
        '    eor #$01',
        '    sta mouth_state',
        '    lda #$01',
        '    sta mouth_dirty',
        'mouth_done_01:',
        '    rts',
        '',
        'refresh_direction_index_01:',
        '    ; Recompute direction index only after bounce changed dx_vel/dy_vel.',
        '    lda dx_vel',
        '    bmi direction_dx_negative_01',
        '    beq direction_dx_zero_01',
        'direction_dx_positive_01:',
        '    lda dy_vel',
        '    bmi direction_candidate_ne_01',
        '    beq direction_candidate_e_01',
        '    jmp direction_candidate_se_01',
        'direction_dx_negative_01:',
        '    lda dy_vel',
        '    bmi direction_candidate_nw_01',
        '    beq direction_candidate_w_01',
        '    jmp direction_candidate_sw_01',
        'direction_dx_zero_01:',
        '    lda dy_vel',
        '    bmi direction_candidate_n_01',
        '    beq direction_candidate_e_01',
        '    jmp direction_candidate_s_01',
        'direction_candidate_e_01:',
        '    ldx #DIR_E',
        '    jmp maybe_store_direction_index_01',
        'direction_candidate_ne_01:',
        '    ldx #DIR_NE',
        '    jmp maybe_store_direction_index_01',
        'direction_candidate_n_01:',
        '    ldx #DIR_N',
        '    jmp maybe_store_direction_index_01',
        'direction_candidate_nw_01:',
        '    ldx #DIR_NW',
        '    jmp maybe_store_direction_index_01',
        'direction_candidate_w_01:',
        '    ldx #DIR_W',
        '    jmp maybe_store_direction_index_01',
        'direction_candidate_sw_01:',
        '    ldx #DIR_SW',
        '    jmp maybe_store_direction_index_01',
        'direction_candidate_s_01:',
        '    ldx #DIR_S',
        '    jmp maybe_store_direction_index_01',
        'direction_candidate_se_01:',
        '    ldx #DIR_SE',
        'maybe_store_direction_index_01:',
        '    cpx direction_index',
        '    beq direction_index_done_01',
        '    stx direction_index',
        '    lda #$01',
        '    sta mouth_dirty',
        'direction_index_done_01:',
        '    rts',
        '',
        'apply_mouth_pointer_if_dirty_01:',
        '    ; Fast path: most frames do not touch the sprite pointer.',
        '    lda mouth_dirty',
        '    bne mouth_pointer_dirty_01',
        'mouth_pointer_clean_01:',
        '    rts',
        'mouth_pointer_dirty_01:',
        '    lda #$00',
        '    sta mouth_dirty',
        '    lda mouth_state',
        '    beq mouth_pointer_open_01',
        '    ldx #FRAME_CLOSED',
        '    jmp maybe_apply_mouth_frame_01',
        'mouth_pointer_open_01:',
        '    lda direction_index',
        '    clc',
        '    adc #FRAME_OPEN_BASE',
        '    tax',
        'maybe_apply_mouth_frame_01:',
        '    cpx current_mouth_frame',
        '    beq mouth_pointer_clean_01',
        '    stx current_mouth_frame',
        '    lda mouth_pointer_table_01,x',
        '    sta SPRITE_POINTER_0',
        '    rts',
        '',
        'update_sprite_01:',
        '    lda x_pos',
        '    sta VIC_SPRITE0_X',
        '    lda y_pos',
        '    sta VIC_SPRITE0_Y',
        '    rts',
        '',
        'wait_frame_01:',
        '    lda #$f8',
        'wait_raster_01:',
        '    cmp RASTER',
        '    bne wait_raster_01',
        'wait_raster_leave_01:',
        '    lda RASTER',
        '    cmp #$f8',
        '    beq wait_raster_leave_01',
        '    rts',
        '',
        'x_pos:',
        f'    .byte {hexbyte(sprite["x"])}',
        'y_pos:',
        f'    .byte {hexbyte(sprite["y"])}',
        'dx_vel:',
        f'    .byte {hexbyte(velocity["dx_byte"])}',
        'dy_vel:',
        f'    .byte {hexbyte(velocity["dy_byte"])}',
        'mouth_timer:',
        '    .byte $00',
        'mouth_state:',
        '    .byte $00',
        'direction_index:',
        '    .byte INITIAL_DIRECTION_INDEX',
        'current_mouth_frame:',
        '    .byte $ff',
        'mouth_dirty:',
        '    .byte $01',
        'mouth_pointer_table_01:',
        '    .byte SPRITE_DATA_POINTER_CLOSED',
        '    .byte SPRITE_DATA_POINTER_OPEN_E, SPRITE_DATA_POINTER_OPEN_NE, SPRITE_DATA_POINTER_OPEN_N, SPRITE_DATA_POINTER_OPEN_NW',
        '    .byte SPRITE_DATA_POINTER_OPEN_W, SPRITE_DATA_POINTER_OPEN_SW, SPRITE_DATA_POINTER_OPEN_S, SPRITE_DATA_POINTER_OPEN_SE',
        '',
        'pacman_sprite_closed_data:',
    ])
    for idx in range(0, len(PACMAN_CLOSED_BYTES), 8):
        lines.append('    .byte ' + ', '.join(hexbyte(b) for b in PACMAN_CLOSED_BYTES[idx:idx + 8]))
    for direction in DIRECTIONS:
        lines.append(f'pacman_sprite_open_{direction.lower()}_data:')
        frame = PACMAN_OPEN_BYTES[direction]
        for idx in range(0, len(frame), 8):
            lines.append('    .byte ' + ', '.join(hexbyte(b) for b in frame[idx:idx + 8]))
    lines.extend(['', '.segment "INIT"', '.segment "ONCE"', '.segment "CODE"'])
    return '\n'.join(lines).rstrip() + '\n'


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print('usage: generate_asm.py goal.lang program.lang generated_intent.json generated.s', file=sys.stderr)
        return 2
    goal_path = Path(argv[1])
    program_path = Path(argv[2])
    intent_path = Path(argv[3])
    asm_path = Path(argv[4])
    goal = parse_goal(goal_path.read_text())
    program = parse_program(program_path.read_text())
    validate_goal_program(goal, program)
    velocity = singleton(program, 'move_sprite_velocity')
    payload = {
        'source_chain': ['goal.lang', 'program.lang', 'generated_intent.json', 'generated.s'],
        'goal': goal,
        'program': program,
        'optimization_posture': 'runtime_speed_first',
        'runtime_optimization': 'arcade_optimized_dirty_pointer_cache',
        'output_contract': 'assembly_only_no_main_c',
        'app_model': 'yellow_pacman_sprite_linear_bounce_vector_facing_crunching_mouth',
        'mouth_orientation': 'cached direction_index derived from direction_from_vector(dx_vel, dy_vel)',
        'supported_mouth_directions': DIRECTIONS,
        'initial_mouth_direction': direction_from_vector(velocity['dx'], velocity['dy']),
        'forbidden_orientation_model': 'left/right-only mouth selection',
        'assembly_strategy': {
            'sprite': 'hardware sprite 0 uses a neutral closed frame plus eight vector-facing open-mouth frames copied to $2000..$2200 and pointed from $07f8',
            'motion': 'add signed byte dx/dy per frame',
            'bounce': 'axis reflection: invert dx on vertical edge, invert dy on horizontal edge; refresh direction_index only when a bounce changes dx/dy',
            'animation': 'toggle open/closed every 8 frames and set mouth_dirty',
            'mouth_pointer': 'mouth_dirty gates writes to SPRITE_POINTER_0; mouth_pointer_table_01,x selects closed/open-vector frames',
            'screen_clear': 'exact 1000-byte y loop',
        },
    }
    intent_path.write_text(json.dumps(payload, indent=2) + '\n')
    asm_path.write_text(emit_asm(goal, program))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
