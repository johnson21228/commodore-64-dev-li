#!/usr/bin/env python3
"""Generate a C64 assembly-only proxy-ping app from goal/program language.

This generator intentionally emits ca65 assembly as the app artifact. It does
not emit, require, or depend on main.c. The networking model is a C64-visible
RS232/Hayes-style modem stream connected to a host-side proxy/server.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

COLOR = {
    "black": 0x00,
    "white": 0x01,
    "red": 0x02,
    "cyan": 0x03,
    "purple": 0x04,
    "green": 0x05,
    "blue": 0x06,
    "yellow": 0x07,
    "orange": 0x08,
    "brown": 0x09,
    "light red": 0x0A,
    "dark gray": 0x0B,
    "gray": 0x0C,
    "light green": 0x0D,
    "light blue": 0x0E,
    "light gray": 0x0F,
}


def parse_goal(text: str) -> list[dict[str, object]]:
    ops: list[dict[str, object]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if m := re.fullmatch(r'goal "([^"]+)"', line):
            ops.append({"op": "goal", "name": m.group(1)})
        elif line == "priority runtime speed first":
            ops.append({"op": "priority", "value": "runtime_speed_first"})
        elif line == "output assembly":
            ops.append({"op": "output", "value": "assembly"})
        elif line == "constraint no main.c":
            ops.append({"op": "constraint", "value": "no_main_c"})
        elif line == "constraint generated assembly is the app":
            ops.append({"op": "constraint", "value": "generated_assembly_is_the_app"})
        elif line == "network pattern modem proxy server":
            ops.append({"op": "network_pattern", "value": "modem_proxy_server"})
        elif line == "requires host proxy server":
            ops.append({"op": "requires", "value": "host_proxy_server"})
        elif line == "requires RS232 or WiFi modem bridge":
            ops.append({"op": "requires", "value": "rs232_or_wifi_modem_bridge"})
        elif m := re.fullmatch(r'request line "([^"]+)"', line):
            ops.append({"op": "request_line", "text": m.group(1)})
        elif line == "show proxy response on screen":
            ops.append({"op": "show_response", "target": "screen"})
        else:
            raise SystemExit(f"Unsupported goal language line: {line!r}")
    return ops


def parse_program(text: str) -> list[dict[str, object]]:
    ops: list[dict[str, object]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if m := re.fullmatch(r'implements goal "([^"]+)"', line):
            ops.append({"op": "implements_goal", "name": m.group(1)})
        elif line == "optimize for speed":
            ops.append({"op": "optimize", "value": "speed"})
        elif m := re.fullmatch(r"set border (.+)", line):
            ops.append({"op": "set_border", "color": m.group(1)})
        elif m := re.fullmatch(r"set background (.+)", line):
            ops.append({"op": "set_background", "color": m.group(1)})
        elif m := re.fullmatch(r"clear screen color (.+)", line):
            ops.append({"op": "clear_screen", "color": m.group(1)})
        elif m := re.fullmatch(r'show title "([^"]+)"', line):
            ops.append({"op": "show_title", "text": m.group(1)})
        elif m := re.fullmatch(r"open rs232 device (\d+) config (\d+) 8n1", line):
            ops.append({"op": "open_rs232", "device": int(m.group(1)), "baud": int(m.group(2)), "format": "8n1"})
        elif m := re.fullmatch(r'dial proxy "([^"]+)" using hayes', line):
            ops.append({"op": "dial_proxy", "target": m.group(1), "protocol": "hayes"})
        elif m := re.fullmatch(r'send line "([^"]+)"', line):
            ops.append({"op": "send_line", "text": m.group(1)})
        elif m := re.fullmatch(r"read response line to row (\d+) col (\d+) max (\d+)", line):
            ops.append({"op": "read_response_line", "row": int(m.group(1)), "col": int(m.group(2)), "max": int(m.group(3))})
        elif line == "loop forever":
            ops.append({"op": "loop_forever"})
        else:
            raise SystemExit(f"Unsupported program language line: {line!r}")
    return ops


def color_value(name: str) -> int:
    if name not in COLOR:
        raise SystemExit(f"Unknown C64 color: {name!r}")
    return COLOR[name]


def screen_code(ch: str) -> int:
    # C64 screen-code subset for stable uppercase lab labels.
    o = ord(ch)
    if "A" <= ch <= "Z":
        return o - 64
    if "a" <= ch <= "z":
        return o - 96
    if ch == " ":
        return 0x20
    if ch in "0123456789":
        return o
    table = {"/": 0x2F, ":": 0x3A, ".": 0x2E, "-": 0x2D, "=": 0x3D, "!": 0x21, "?": 0x3F}
    return table.get(ch, 0x20)


def emit_text(row: int, col: int, text: str) -> list[str]:
    base = row * 40 + col
    lines: list[str] = []
    for i, ch in enumerate(text[:40-col]):
        lines.append(f"    lda #${screen_code(ch):02x}")
        lines.append(f"    sta SCREEN_RAM+{base+i}")
    return lines


def ascii_bytes(text: str, cr: bool = True) -> str:
    values = [ord(c) for c in text]
    if cr:
        values.append(13)
    values.append(0)
    return ", ".join(f"${v:02x}" for v in values)


def generate_asm(intent: dict[str, object]) -> str:
    program: list[dict[str, object]] = intent["program"]  # type: ignore[assignment]
    goal_name = next((g["name"] for g in intent["goal"] if g.get("op") == "goal"), "C64NET PROXY PING")  # type: ignore[index]
    border = next((color_value(op["color"]) for op in program if op["op"] == "set_border"), 6)  # type: ignore[index]
    background = next((color_value(op["color"]) for op in program if op["op"] == "set_background"), 0)  # type: ignore[index]
    clear_color = next((color_value(op["color"]) for op in program if op["op"] == "clear_screen"), 0)  # type: ignore[index]
    title = next((op["text"] for op in program if op["op"] == "show_title"), str(goal_name))  # type: ignore[index]
    dial_target = next((op["target"] for op in program if op["op"] == "dial_proxy"), "127.0.0.1:6464")  # type: ignore[index]
    request_line = next((op["text"] for op in program if op["op"] == "send_line"), "GET /c64/ping")  # type: ignore[index]
    read_op = next((op for op in program if op["op"] == "read_response_line"), {"row": 15, "col": 2, "max": 36})
    response_offset = int(read_op["row"]) * 40 + int(read_op["col"])  # type: ignore[index]
    max_chars = int(read_op["max"])  # type: ignore[index]

    lines: list[str] = []
    lines.extend([
        "; Generated by labs/011_goal_language_to_asm_net_proxy/src/generate_asm.py",
        "; Goal source: labs/011_goal_language_to_asm_net_proxy/src/goal.lang",
        "; Program source: labs/011_goal_language_to_asm_net_proxy/src/program.lang",
        f"; Goal: {goal_name}",
        "; Priority: runtime speed first; teaching clarity is secondary.",
        "; Output: assembly app source. No main.c is generated or consumed.",
        "; Network pattern: C64 RS232/Hayes stream -> host proxy/server -> internet-facing work.",
        "; This app opens KERNAL RS232 device 2, sends AT/Hayes text, sends a line request, then reads one response line.",
        ".import __EXEHDR__",
        ".export _main",
        "",
        "SCREEN_RAM = $0400",
        "COLOR_RAM = $d800",
        "SPACE_CHAR = $20",
        "BORDER_COLOR = $d020",
        "BACKGROUND_COLOR = $d021",
        "SETLFS = $ffba",
        "SETNAM = $ffbd",
        "OPEN = $ffc0",
        "CLOSE = $ffc3",
        "CHKIN = $ffc6",
        "CHKOUT = $ffc9",
        "CLRCHN = $ffcc",
        "CHRIN = $ffcf",
        "CHROUT = $ffd2",
        "RS232_LFN = $02",
        "RS232_DEVICE = $02",
        "RESPONSE_SCREEN = SCREEN_RAM+%d" % response_offset,
        "RESPONSE_MAX = %d" % max_chars,
        "SCREEN_PTR_LO = $fb",
        "SCREEN_PTR_HI = $fc",
        "TEXT_PTR_LO = $fd",
        "TEXT_PTR_HI = $fe",
        "",
        ".segment \"STARTUP\"",
        "_main:",
        "    lda #$%02x" % border,
        "    sta BORDER_COLOR",
        "    lda #$%02x" % background,
        "    sta BACKGROUND_COLOR",
        "    ; exact 1000-byte clear: four 250-byte stripes, no overlap",
        "    ldy #250",
        "fast_clear_loop_01:",
        "    lda #SPACE_CHAR",
        "    sta SCREEN_RAM-1,y",
        "    sta SCREEN_RAM+249,y",
        "    sta SCREEN_RAM+499,y",
        "    sta SCREEN_RAM+749,y",
        "    lda #$%02x" % clear_color,
        "    sta COLOR_RAM-1,y",
        "    sta COLOR_RAM+249,y",
        "    sta COLOR_RAM+499,y",
        "    sta COLOR_RAM+749,y",
        "    dey",
        "    bne fast_clear_loop_01",
        "",
    ])
    # Static UI rows.
    lines += emit_text(2, 2, str(title))
    lines += emit_text(5, 2, "LANGUAGE GENERATED ASM")
    lines += emit_text(7, 2, "NO MAIN.C")
    lines += emit_text(9, 2, "RS232 MODEM PROXY")
    lines += emit_text(11, 2, "SENDING GET /C64/PING")
    lines += emit_text(14, 2, "RESPONSE:")
    lines.extend([
        "",
        "    jsr open_rs232_01",
        "    jsr send_at_01",
        "    jsr read_response_01",
        "    jsr send_dial_01",
        "    jsr read_response_01",
        "    jsr send_request_01",
        "    jsr read_response_01",
        "",
        "hold_forever_01:",
        "    jmp hold_forever_01",
        "",
        "open_rs232_01:",
        "    lda #RS232_LFN",
        "    ldx #RS232_DEVICE",
        "    ldy #$00",
        "    jsr SETLFS",
        "    lda #$02",
        "    ldx #<rs232_control_name",
        "    ldy #>rs232_control_name",
        "    jsr SETNAM",
        "    jsr OPEN",
        "    rts",
        "",
        "send_at_01:",
        "    lda #<at_command",
        "    sta TEXT_PTR_LO",
        "    lda #>at_command",
        "    sta TEXT_PTR_HI",
        "    jmp send_rs232_zstring_01",
        "",
        "send_dial_01:",
        "    lda #<dial_command",
        "    sta TEXT_PTR_LO",
        "    lda #>dial_command",
        "    sta TEXT_PTR_HI",
        "    jmp send_rs232_zstring_01",
        "",
        "send_request_01:",
        "    lda #<request_command",
        "    sta TEXT_PTR_LO",
        "    lda #>request_command",
        "    sta TEXT_PTR_HI",
        "    jmp send_rs232_zstring_01",
        "",
        "send_rs232_zstring_01:",
        "    ldx #RS232_LFN",
        "    jsr CHKOUT",
        "    ldy #$00",
        "send_rs232_loop_01:",
        "    lda (TEXT_PTR_LO),y",
        "    beq send_rs232_done_01",
        "    jsr CHROUT",
        "    iny",
        "    bne send_rs232_loop_01",
        "send_rs232_done_01:",
        "    jsr CLRCHN",
        "    rts",
        "",
        "read_response_01:",
        "    lda #<RESPONSE_SCREEN",
        "    sta SCREEN_PTR_LO",
        "    lda #>RESPONSE_SCREEN",
        "    sta SCREEN_PTR_HI",
        "    ; clear previous response field",
        "    ldy #$00",
        "clear_response_loop_01:",
        "    lda #SPACE_CHAR",
        "    sta (SCREEN_PTR_LO),y",
        "    iny",
        "    cpy #RESPONSE_MAX",
        "    bcc clear_response_loop_01",
        "    ldx #RS232_LFN",
        "    jsr CHKIN",
        "    ldy #$00",
        "read_response_loop_01:",
        "    jsr CHRIN",
        "    cmp #$0d",
        "    beq read_response_done_01",
        "    cmp #$0a",
        "    beq read_response_loop_01",
        "    jsr ascii_to_screen_01",
        "    sta (SCREEN_PTR_LO),y",
        "    iny",
        "    cpy #RESPONSE_MAX",
        "    bcc read_response_loop_01",
        "read_response_done_01:",
        "    jsr CLRCHN",
        "    rts",
        "",
        "ascii_to_screen_01:",
        "    cmp #$41",
        "    bcc ascii_not_upper_01",
        "    cmp #$5b",
        "    bcs ascii_not_upper_01",
        "    sec",
        "    sbc #$40",
        "    rts",
        "ascii_not_upper_01:",
        "    cmp #$61",
        "    bcc ascii_keep_01",
        "    cmp #$7b",
        "    bcs ascii_keep_01",
        "    sec",
        "    sbc #$60",
        "    rts",
        "ascii_keep_01:",
        "    rts",
        "",
        "    ; TEXT_PTR_LO/TEXT_PTR_HI are zero-page scratch constants.",
        "    ; They must not be allocated as normal CODE labels because (zp),y addressing is zero-page only.",
        "",
        "rs232_control_name:",
        "    ; KERNAL RS232 open control bytes matching the classic OPEN 2,2,0,CHR$(8)+CHR$(1) pattern.",
        "    .byte $08, $01",
        "at_command:",
        "    ; AT",
        "    .byte %s" % ascii_bytes("AT"),
        "dial_command:",
        "    ; ATDT" + str(dial_target),
        "    .byte %s" % ascii_bytes("ATDT" + str(dial_target)),
        "request_command:",
        "    ; " + str(request_line),
        "    .byte %s" % ascii_bytes(str(request_line)),
        "",
        ".segment \"INIT\"",
        ".segment \"ONCE\"",
        ".segment \"CODE\"",
        "",
    ])
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print("usage: generate_asm.py goal.lang program.lang generated_intent.json generated.s", file=sys.stderr)
        return 2
    goal_path = Path(argv[1])
    program_path = Path(argv[2])
    intent_path = Path(argv[3])
    asm_path = Path(argv[4])
    goal_ops = parse_goal(goal_path.read_text())
    program_ops = parse_program(program_path.read_text())
    intent = {
        "schemaVersion": 1,
        "lab": "011_goal_language_to_asm_net_proxy",
        "optimization_posture": "runtime_speed_first",
        "output_contract": "assembly_only_no_main_c",
        "app_model": "rs232_hayes_proxy_ping_client",
        "internet_boundary": "host_proxy_server_owns_tcp_http_tls",
        "goal": goal_ops,
        "program": program_ops,
    }
    intent_path.write_text(json.dumps(intent, indent=2) + "\n")
    asm_path.write_text(generate_asm(intent))
    print(f"Generated {intent_path} and {asm_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
