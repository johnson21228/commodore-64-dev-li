#!/usr/bin/env python3
"""Generate a speed-oriented ca65 C64 Pac-Man bounce app from language.

Lab 010 proves a two-language front end:

    goal.lang      -> declares the app goal and constraints
    program.lang   -> implements the goal in a controlled language
    generated.s    -> assembly app source; no main.c is produced or consumed

The important gameplay invariant is vector-owned: the open mouth faces the
current signed dx/dy motion vector, not merely left or right.
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
DIR_VECTOR = {
    "E": (1, 0), "NE": (1, -1), "N": (0, -1), "NW": (-1, -1),
    "W": (-1, 0), "SW": (-1, 1), "S": (0, 1), "SE": (1, 1),
}

GOAL_RE = re.compile(r'^goal "([A-Z0-9 ,.:!.?\\-]+)"$')
IMPLEMENTS_RE = re.compile(r'^implements goal "([A-Z0-9 ,.:!.?\\-]+)"$')
SPRITE_RE = re.compile(r'^use yellow pacman sprite at x ([0-9]{1,3}) y ([0-9]{1,3})$')
VELOCITY_RE = re.compile(r'^move sprite velocity dx (-?[0-9]{1,2}) dy (-?[0-9]{1,2})$')
BOUNDS_RE = re.compile(r'^bounds x ([0-9]{1,3}) ([0-9]{1,3}) y ([0-9]{1,3}) ([0-9]{1,3})$')


def parse_goal_line(line: str, line_no: int) -> dict:
    raw = line.strip()
    if not raw or raw.startswith("#"):
        return {"op": "comment", "line": line_no, "source": line.rstrip("\n")}
    match = GOAL_RE.match(raw)
    if match:
        return {"op": "goal", "line": line_no, "source": raw, "name": match.group(1)}
    if raw == "priority runtime speed first":
        return {"op": "priority", "line": line_no, "source": raw, "value": "runtime_speed_first"}
    if raw == "output assembly":
        return {"op": "output", "line": line_no, "source": raw, "value": "assembly"}
    if raw == "constraint no main.c":
        return {"op": "constraint", "line": line_no, "source": raw, "value": "no_main_c"}
    if raw == "constraint generated assembly is the app":
        return {"op": "constraint", "line": line_no, "source": raw, "value": "generated_assembly_is_app"}
    if raw == "visual yellow pac-man sprite":
        return {"op": "visual", "line": line_no, "source": raw, "subject": "yellow_pacman_sprite"}
    if raw == "animation crunching mouth opens and closes":
        return {"op": "animation_goal", "line": line_no, "source": raw, "model": "pacman_mouth_crunch"}
    if raw == "animation mouth faces direction_from_vector dx dy":
        return {"op": "animation_goal", "line": line_no, "source": raw, "model": "pacman_mouth_faces_vector"}
    if raw == "motion linear path":
        return {"op": "motion", "line": line_no, "source": raw, "model": "linear_path"}
    if raw == "bounce screen edges with incidence angle equals outgoing angle":
        return {"op": "bounce_goal", "line": line_no, "source": raw, "model": "reflect_edges_equal_angle"}
    if raw == "support mouth directions E NE N NW W SW S SE":
        return {"op": "mouth_direction_support", "line": line_no, "source": raw, "directions": DIRECTIONS}
    raise ValueError(f"goal line {line_no}: unknown command {raw!r}")


def parse_program_line(line: str, line_no: int) -> dict:
    raw = line.strip()
    if not raw or raw.startswith("#"):
        return {"op": "comment", "line": line_no, "source": line.rstrip("\n")}
    match = IMPLEMENTS_RE.match(raw)
    if match:
        return {"op": "implements_goal", "line": line_no, "source": raw, "goal": match.group(1)}
    if raw == "optimize for speed":
        return {"op": "optimize", "line": line_no, "source": raw, "strategy": "runtime_speed_first"}
    for prefix, op, register in [("set border ", "set_border", "$d020"), ("set background ", "set_background", "$d021")]:
        if raw.startswith(prefix):
            color_name = raw[len(prefix):]
            if color_name not in COLOR:
                raise ValueError(f"line {line_no}: unsupported color {color_name!r}")
            return {"op": op, "line": line_no, "source": raw, "color": color_name, "value": COLOR[color_name], "register": register}
    if raw.startswith("clear screen color "):
        color_name = raw[len("clear screen color "):]
        if color_name not in COLOR:
            raise ValueError(f"line {line_no}: unsupported color {color_name!r}")
        return {"op": "clear_screen", "line": line_no, "source": raw, "color": color_name, "color_value": COLOR[color_name], "strategy": "exact_1000_byte_y_loop"}
    match = SPRITE_RE.match(raw)
    if match:
        x, y = map(int, match.groups())
        return {"op": "use_pacman_sprite", "line": line_no, "source": raw, "color": "yellow", "color_value": COLOR["yellow"], "x": x, "y": y}
    if raw == "animate mouth crunch every 8 frames":
        return {"op": "animate_mouth", "line": line_no, "source": raw, "model": "toggle_sprite_frame", "period_frames": 8}
    if raw == "face mouth with dx dy vector":
        return {"op": "face_mouth_with_vector", "line": line_no, "source": raw, "model": "select_sprite_frame_from_dx_dy_vector", "directions": DIRECTIONS}
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
    if raw == "bounce reflect at screen edge":
        return {"op": "bounce_reflect", "line": line_no, "source": raw, "model": "invert_axis_velocity_on_boundary"}
    if raw == "loop forever":
        return {"op": "loop_forever", "line": line_no, "source": raw}
    raise ValueError(f"program line {line_no}: unknown command {raw!r}")


def parse_goal(text: str) -> list[dict]:
    return [parse_goal_line(line, n) for n, line in enumerate(text.splitlines(), start=1)]


def parse_program(text: str) -> list[dict]:
    return [parse_program_line(line, n) for n, line in enumerate(text.splitlines(), start=1)]


def singleton(items: list[dict], op: str) -> dict:
    found = [item for item in items if item.get("op") == op]
    if len(found) != 1:
        raise ValueError(f"expected exactly one {op}, found {len(found)}")
    return found[0]


def goal_name(goal: list[dict]) -> str:
    return singleton(goal, "goal")["name"]


def validate_goal_program(goal: list[dict], program: list[dict]) -> None:
    name = goal_name(goal)
    implemented = [item["goal"] for item in program if item.get("op") == "implements_goal"]
    if implemented != [name]:
        raise ValueError(f"program.lang must implement exactly goal {name!r}")
    if [item.get("value") for item in goal if item.get("op") == "priority"] != ["runtime_speed_first"]:
        raise ValueError("goal.lang must declare priority runtime speed first")
    if [item.get("value") for item in goal if item.get("op") == "output"] != ["assembly"]:
        raise ValueError("goal.lang must declare output assembly")
    constraints = {item.get("value") for item in goal if item.get("op") == "constraint"}
    if not {"no_main_c", "generated_assembly_is_app"}.issubset(constraints):
        raise ValueError("goal.lang missing required no-main.c/generated-assembly constraints")
    if not any(item.get("model") == "pacman_mouth_faces_vector" for item in goal):
        raise ValueError("goal.lang must request vector-facing mouth animation")
    if singleton(goal, "mouth_direction_support").get("directions") != DIRECTIONS:
        raise ValueError("goal.lang must support all eight mouth directions")
    for op in ["optimize", "set_border", "set_background", "clear_screen", "use_pacman_sprite", "animate_mouth", "face_mouth_with_vector", "move_sprite_velocity", "bounds", "bounce_reflect", "loop_forever"]:
        singleton(program, op)
    sprite = singleton(program, "use_pacman_sprite")
    bounds = singleton(program, "bounds")
    if not (bounds["min_x"] <= sprite["x"] <= bounds["max_x"] and bounds["min_y"] <= sprite["y"] <= bounds["max_y"]):
        raise ValueError("initial sprite position must be inside bounds")


def hexbyte(value: int) -> str:
    return f"${value & 0xFF:02x}"


def direction_from_vector(dx: int, dy: int) -> str:
    if dx > 0 and dy < 0: return "NE"
    if dx < 0 and dy < 0: return "NW"
    if dx < 0 and dy > 0: return "SW"
    if dx > 0 and dy > 0: return "SE"
    if dx > 0: return "E"
    if dx < 0: return "W"
    if dy < 0: return "N"
    if dy > 0: return "S"
    return "E"


def make_pacman_frame(direction: str | None, closed: bool = False) -> list[int]:
    cx, cy = 11.5, 10.0
    rx, ry = 10.5, 9.6
    wedge_half_angle = math.radians(26)
    vx, vy = DIR_VECTOR.get(direction or "E", (1, 0))
    mouth_angle = math.atan2(vy, vx)
    rows: list[int] = []
    for y in range(21):
        bits = []
        for x in range(24):
            nx = (x - cx) / rx
            ny = (y - cy) / ry
            inside = nx * nx + ny * ny <= 1.0
            if inside and not closed:
                angle = math.atan2(y - cy, x - cx)
                delta = math.atan2(math.sin(angle - mouth_angle), math.cos(angle - mouth_angle))
                distance_along = ((x - cx) * vx + (y - cy) * vy)
                if abs(delta) < wedge_half_angle and distance_along > 1.0:
                    inside = False
            bits.append(1 if inside else 0)
        for group in range(3):
            byte = 0
            for bit in bits[group * 8:(group + 1) * 8]:
                byte = (byte << 1) | bit
            rows.append(byte)
    rows.append(0)
    return rows


PACMAN_CLOSED_BYTES = make_pacman_frame(None, closed=True)
PACMAN_OPEN_BYTES = {direction: make_pacman_frame(direction, closed=False) for direction in DIRECTIONS}


def emit_bytes(lines: list[str], label: str, data: list[int]) -> None:
    lines.append(f"{label}:")
    for idx in range(0, len(data), 8):
        chunk = data[idx:idx + 8]
        lines.append("    .byte " + ", ".join(hexbyte(b) for b in chunk))


def emit_fast_clear(lines: list[str], color_value: int) -> None:
    lines.extend([
        "    ; exact 1000-byte clear: four 250-byte stripes, no overlap",
        "    ldy #250",
        "fast_clear_loop_01:",
        "    lda #SPACE_CHAR",
        "    sta SCREEN_RAM-1,y",
        "    sta SCREEN_RAM+249,y",
        "    sta SCREEN_RAM+499,y",
        "    sta SCREEN_RAM+749,y",
        f"    lda #{hexbyte(color_value)}",
        "    sta COLOR_RAM-1,y",
        "    sta COLOR_RAM+249,y",
        "    sta COLOR_RAM+499,y",
        "    sta COLOR_RAM+749,y",
        "    dey",
        "    bne fast_clear_loop_01",
    ])


def emit_copy_frames(lines: list[str]) -> None:
    labels = ["closed"] + [d.lower() for d in DIRECTIONS]
    lines.extend(["    ; copy generated closed and eight vector-facing open-mouth frames", "    ldx #$3f", "copy_pacman_sprite_01:"])
    for label in labels:
        source = "pacman_sprite_closed_data" if label == "closed" else f"pacman_sprite_open_{label}_data"
        target = f"SPRITE_DATA_{label.upper()}" if label == "closed" else f"SPRITE_DATA_OPEN_{label.upper()}"
        lines.extend([f"    lda {source},x", f"    sta {target},x"])
    lines.extend(["    dex", "    bpl copy_pacman_sprite_01"])


def emit_asm(goal: list[dict], program: list[dict]) -> str:
    name = goal_name(goal)
    sprite = singleton(program, "use_pacman_sprite")
    velocity = singleton(program, "move_sprite_velocity")
    bounds = singleton(program, "bounds")
    border = singleton(program, "set_border")
    background = singleton(program, "set_background")
    clear = singleton(program, "clear_screen")
    min_x, max_x = bounds["min_x"], bounds["max_x"]
    min_y, max_y = bounds["min_y"], bounds["max_y"]
    dx, dy = velocity["dx"], velocity["dy"]
    lines: list[str] = [
        "; Generated by labs/010_goal_language_to_asm_pacman_bounce/src/generate_asm.py",
        "; Goal source: labs/010_goal_language_to_asm_pacman_bounce/src/goal.lang",
        "; Program source: labs/010_goal_language_to_asm_pacman_bounce/src/program.lang",
        f"; Goal: {name}",
        "; Priority: runtime speed first; teaching clarity is secondary.",
        "; Output: assembly app source. No main.c is generated or consumed.",
        "; Motion: signed dx_vel/dy_vel vector; edge bounce reflects only the hit axis.",
        "; Mouth: direction_from_vector(dx_vel, dy_vel) selects E NE N NW W SW S SE.",
        "; Guardrail: left/right-only mouth selection is forbidden.",
        ".import __EXEHDR__", ".export _main", "",
        "SCREEN_RAM = $0400", "COLOR_RAM = $d800", "SPACE_CHAR = $20", "SPRITE_POINTER_0 = $07f8", "SPRITE_DATA = $2000",
        "SPRITE_DATA_CLOSED = $2000", "SPRITE_DATA_POINTER_CLOSED = $80",
    ]
    for idx, d in enumerate(DIRECTIONS, start=1):
        addr = 0x2000 + idx * 0x40
        ptr = 0x80 + idx
        lines.append(f"SPRITE_DATA_OPEN_{d} = ${addr:04x}")
        lines.append(f"SPRITE_DATA_POINTER_OPEN_{d} = ${ptr:02x}")
    lines.extend([
        "VIC_SPRITE0_X = $d000", "VIC_SPRITE0_Y = $d001", "SPRITE_X_MSB = $d010", "SPRITE_ENABLE = $d015", "RASTER = $d012",
        "SPRITE0_COLOR = $d027", "BORDER_COLOR = $d020", "BACKGROUND_COLOR = $d021",
        f"MIN_X = {hexbyte(min_x)}", f"MAX_X = {hexbyte(max_x)}", f"MIN_Y = {hexbyte(min_y)}", f"MAX_Y = {hexbyte(max_y)}",
        f"DX_POS = {hexbyte(abs(dx))}", f"DX_NEG = {hexbyte((-abs(dx)) & 0xff)}", f"DY_POS = {hexbyte(abs(dy))}", f"DY_NEG = {hexbyte((-abs(dy)) & 0xff)}",
        "", '.segment "STARTUP"', "_main:", "    ; speed-first generated setup from goal/program language",
        f"    lda #{hexbyte(border['value'])}", "    sta BORDER_COLOR", f"    lda #{hexbyte(background['value'])}", "    sta BACKGROUND_COLOR",
    ])
    emit_fast_clear(lines, clear["color_value"])
    lines.append("")
    emit_copy_frames(lines)
    lines.extend([
        "", "    ; color and enable sprite 0", f"    lda #{hexbyte(sprite['color_value'])}", "    sta SPRITE0_COLOR", "    lda #$01", "    sta SPRITE_ENABLE", "    lda #$00", "    sta SPRITE_X_MSB",
        "", f"    lda #{hexbyte(sprite['x'])}", "    sta x_pos", f"    lda #{hexbyte(sprite['y'])}", "    sta y_pos", f"    lda #{hexbyte(velocity['dx_byte'])}", "    sta dx_vel", f"    lda #{hexbyte(velocity['dy_byte'])}", "    sta dy_vel",
        "    lda #$00", "    sta mouth_timer", "    sta mouth_state", "    jsr update_mouth_pointer_01", "    jsr update_sprite_01", "",
        "main_loop_01:", "    jsr wait_frame_01", "", "    ; x = x + dx; reflect at left/right boundaries", "    lda x_pos", "    clc", "    adc dx_vel", "    sta x_pos", "    cmp #MIN_X", "    bcs check_right_edge_01",
        "hit_left_edge_01:", "    lda #MIN_X", "    sta x_pos", "    lda #DX_POS", "    sta dx_vel", "    jmp update_y_01", "check_right_edge_01:", "    cmp #MAX_X", "    bcc update_y_01",
        "hit_right_edge_01:", "    lda #MAX_X", "    sta x_pos", "    lda #DX_NEG", "    sta dx_vel", "", "update_y_01:", "    ; y = y + dy; reflect at top/bottom boundaries", "    lda y_pos", "    clc", "    adc dy_vel", "    sta y_pos", "    cmp #MIN_Y", "    bcs check_bottom_edge_01",
        "hit_top_edge_01:", "    lda #MIN_Y", "    sta y_pos", "    lda #DY_POS", "    sta dy_vel", "    jmp draw_sprite_01", "check_bottom_edge_01:", "    cmp #MAX_Y", "    bcc draw_sprite_01",
        "hit_bottom_edge_01:", "    lda #MAX_Y", "    sta y_pos", "    lda #DY_NEG", "    sta dy_vel", "", "draw_sprite_01:", "    jsr animate_mouth_01", "    jsr update_mouth_pointer_01", "    jsr update_sprite_01", "    jmp main_loop_01", "",
        "animate_mouth_01:", "    inc mouth_timer", "    lda mouth_timer", "    and #$07", "    bne mouth_done_01", "    lda mouth_state", "    eor #$01", "    sta mouth_state", "mouth_done_01:", "    rts", "",
        "update_mouth_pointer_01:", "    ; closed mouth is neutral; open mouth faces direction_from_vector(dx_vel, dy_vel)", "    lda mouth_state", "    bne mouth_closed_01", "    lda dy_vel", "    beq mouth_vector_horizontal_01", "    bmi mouth_vector_north_01",
        "mouth_vector_south_01:", "    lda dx_vel", "    beq mouth_open_s_01", "    bmi mouth_open_sw_01", "    jmp mouth_open_se_01",
        "mouth_vector_north_01:", "    lda dx_vel", "    beq mouth_open_n_01", "    bmi mouth_open_nw_01", "    jmp mouth_open_ne_01",
        "mouth_vector_horizontal_01:", "    lda dx_vel", "    bmi mouth_open_w_01",
        "mouth_open_e_01:", "    lda #SPRITE_DATA_POINTER_OPEN_E", "    sta SPRITE_POINTER_0", "    rts",
        "mouth_open_ne_01:", "    lda #SPRITE_DATA_POINTER_OPEN_NE", "    sta SPRITE_POINTER_0", "    rts",
        "mouth_open_n_01:", "    lda #SPRITE_DATA_POINTER_OPEN_N", "    sta SPRITE_POINTER_0", "    rts",
        "mouth_open_nw_01:", "    lda #SPRITE_DATA_POINTER_OPEN_NW", "    sta SPRITE_POINTER_0", "    rts",
        "mouth_open_w_01:", "    lda #SPRITE_DATA_POINTER_OPEN_W", "    sta SPRITE_POINTER_0", "    rts",
        "mouth_open_sw_01:", "    lda #SPRITE_DATA_POINTER_OPEN_SW", "    sta SPRITE_POINTER_0", "    rts",
        "mouth_open_s_01:", "    lda #SPRITE_DATA_POINTER_OPEN_S", "    sta SPRITE_POINTER_0", "    rts",
        "mouth_open_se_01:", "    lda #SPRITE_DATA_POINTER_OPEN_SE", "    sta SPRITE_POINTER_0", "    rts",
        "mouth_closed_01:", "    lda #SPRITE_DATA_POINTER_CLOSED", "    sta SPRITE_POINTER_0", "    rts", "",
        "update_sprite_01:", "    lda x_pos", "    sta VIC_SPRITE0_X", "    lda y_pos", "    sta VIC_SPRITE0_Y", "    rts", "",
        "wait_frame_01:", "    lda #$f8", "wait_raster_01:", "    cmp RASTER", "    bne wait_raster_01", "wait_raster_leave_01:", "    lda RASTER", "    cmp #$f8", "    beq wait_raster_leave_01", "    rts", "",
        "x_pos:", f"    .byte {hexbyte(sprite['x'])}", "y_pos:", f"    .byte {hexbyte(sprite['y'])}", "dx_vel:", f"    .byte {hexbyte(velocity['dx_byte'])}", "dy_vel:", f"    .byte {hexbyte(velocity['dy_byte'])}", "mouth_timer:", "    .byte $00", "mouth_state:", "    .byte $00", "",
    ])
    emit_bytes(lines, "pacman_sprite_closed_data", PACMAN_CLOSED_BYTES)
    for d in DIRECTIONS:
        emit_bytes(lines, f"pacman_sprite_open_{d.lower()}_data", PACMAN_OPEN_BYTES[d])
    lines.extend(["", '.segment "INIT"', '.segment "ONCE"', '.segment "CODE"'])
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print("usage: generate_asm.py goal.lang program.lang generated_intent.json generated.s", file=sys.stderr)
        return 2
    goal_path = Path(argv[1])
    program_path = Path(argv[2])
    intent_path = Path(argv[3])
    asm_path = Path(argv[4])
    goal = parse_goal(goal_path.read_text())
    program = parse_program(program_path.read_text())
    validate_goal_program(goal, program)
    payload = {
        "source_chain": ["goal.lang", "program.lang", "generated_intent.json", "generated.s"],
        "goal": goal,
        "program": program,
        "optimization_posture": "runtime_speed_first",
        "output_contract": "assembly_only_no_main_c",
        "app_model": "yellow_pacman_sprite_linear_bounce_vector_facing_crunching_mouth",
        "movement_truth": "signed dx_vel/dy_vel vector",
        "mouth_orientation": "direction_from_vector(dx_vel, dy_vel)",
        "supported_mouth_directions": DIRECTIONS,
        "forbidden_orientation_model": "left/right-only mouth selection",
        "assembly_strategy": {
            "sprite": "hardware sprite 0 uses one closed frame plus eight vector-facing open-mouth frames copied to VIC-visible sprite blocks",
            "motion": "add signed byte dx/dy per frame",
            "bounce": "axis reflection: invert dx on vertical edge, invert dy on horizontal edge",
            "animation": "toggle open/closed state every 8 frames and select open frame from dx/dy vector",
            "screen_clear": "exact 1000-byte y loop",
        },
    }
    intent_path.write_text(json.dumps(payload, indent=2) + "\n")
    asm_path.write_text(emit_asm(goal, program))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
