#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

LOAD_ADDR = 0x0801
CODE_ADDR = 0x080D
BITMAP_ADDR = 0x2000
SCREEN_ADDR = 0x0400
COLOR_RAM_ADDR = 0xD800

BITMAP_SOURCE_ADDR = 0x4000
SCREEN_SOURCE_ADDR = BITMAP_SOURCE_ADDR + 8000
COLOR_SOURCE_ADDR = SCREEN_SOURCE_ADDR + 1000

C64_SHADE_TO_COLOR = {
    "red_light": 2,
    "red_mid": 8,
    "red_mid_dark": 9,
    "red_dark": 11,
    "red_deep": 0,
}

def ensure_spans() -> None:
    if not (DIST / "single_cube_polygon_spans.json").exists():
        subprocess.run(["python3", "tools/generate_single_cube_polygon_spans.py"], cwd=ROOT, check=True)

def c64_bitmap_offset(x: int, y: int) -> int:
    return (y // 8) * 320 + (x // 8) * 8 + (y % 8)

def set_pixel(bitmap: bytearray, x: int, y: int) -> None:
    if not 0 <= x <= 319 or not 0 <= y <= 199:
        return
    offset = c64_bitmap_offset(x, y)
    if 0 <= offset < len(bitmap):
        bitmap[offset] |= 1 << (7 - (x % 8))

def cell_index(x: int, y: int) -> int:
    return (y // 8) * 40 + (x // 8)

def add_line(bitmap: bytearray, x1: int, y1: int, x2: int, y2: int) -> None:
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy
    x, y = x1, y1
    while True:
        set_pixel(bitmap, x, y)
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy

def paint_cell(screen: bytearray, color_ram: bytearray, x: int, y: int, fg: int, bg: int = 0) -> None:
    idx = cell_index(x, y)
    if 0 <= idx < 1000:
        screen[idx] = ((fg & 0x0F) << 4) | (bg & 0x0F)
        color_ram[idx] = fg & 0x0F

def build_bitmap_and_color(spans_data: dict, faces_data: dict, pit_segments: list[dict]) -> tuple[bytearray, bytearray, bytearray]:
    bitmap = bytearray(8000)
    screen = bytearray([0x10] * 1000)    # white-ish line foreground, black bg
    color_ram = bytearray([0x01] * 1000)

    # Pit wireframe context first.
    for s in pit_segments:
        add_line(bitmap, s["x1"], s["y1"], s["x2"], s["y2"])
        paint_cell(screen, color_ram, s["x1"], s["y1"], 1)
        paint_cell(screen, color_ram, s["x2"], s["y2"], 1)

    face_shade = {face["face_index"]: face["shade"] for face in spans_data["faces"]}

    # Filled cube spans over the pit.
    for face in spans_data["faces"]:
        shade = face_shade[face["face_index"]]
        c64_color = C64_SHADE_TO_COLOR.get(shade, 2)
        for span in face["spans"]:
            y = span["y"]
            for x in range(span["x_start"], span["x_end"] + 1):
                set_pixel(bitmap, x, y)
                paint_cell(screen, color_ram, x, y, c64_color)

    # Light outlines over faces so cube sides read.
    for face in faces_data["faces"]:
        pts = [(p["x"], p["y"]) for p in face["points"]]
        for i in range(len(pts)):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % len(pts)]
            add_line(bitmap, x1, y1, x2, y2)
            paint_cell(screen, color_ram, x1, y1, 2)
            paint_cell(screen, color_ram, x2, y2, 2)

    return bitmap, screen, color_ram

def le_word(value: int) -> list[int]:
    return [value & 0xFF, (value >> 8) & 0xFF]

def emit_basic_stub() -> bytearray:
    return bytearray([0x0C, 0x08, 0x0A, 0x00, 0x9E, ord("2"), ord("0"), ord("6"), ord("1"), 0x00, 0x00, 0x00])

def lda_imm(v: int) -> list[int]: return [0xA9, v & 0xFF]
def ldx_imm(v: int) -> list[int]: return [0xA2, v & 0xFF]
def sta_abs(addr: int) -> list[int]: return [0x8D, addr & 0xFF, (addr >> 8) & 0xFF]
def lda_abs_x(addr: int) -> list[int]: return [0xBD, addr & 0xFF, (addr >> 8) & 0xFF]
def sta_abs_x(addr: int) -> list[int]: return [0x9D, addr & 0xFF, (addr >> 8) & 0xFF]

def copy_page_loop(src: int, dst: int, count: int) -> list[int]:
    code: list[int] = []
    code += ldx_imm(0)
    loop_start = len(code)
    code += lda_abs_x(src)
    code += sta_abs_x(dst)
    code += [0xE8]
    if count == 256:
        offset = (loop_start - (len(code) + 2)) & 0xFF
        code += [0xD0, offset]
    else:
        code += [0xE0, count & 0xFF]
        offset = (loop_start - (len(code) + 2)) & 0xFF
        code += [0xD0, offset]
    return code

def copy_block(src: int, dst: int, length: int) -> list[int]:
    code: list[int] = []
    full_pages = length // 256
    remainder = length % 256
    for page in range(full_pages):
        code += copy_page_loop(src + page * 256, dst + page * 256, 256)
    if remainder:
        code += copy_page_loop(src + full_pages * 256, dst + full_pages * 256, remainder)
    return code

def build_machine_code() -> bytearray:
    code: list[int] = []
    code += lda_imm(0x00) + sta_abs(0xD020) + sta_abs(0xD021)
    code += copy_block(BITMAP_SOURCE_ADDR, BITMAP_ADDR, 8000)
    code += copy_block(SCREEN_SOURCE_ADDR, SCREEN_ADDR, 1000)
    code += copy_block(COLOR_SOURCE_ADDR, COLOR_RAM_ADDR, 1000)
    code += lda_imm(0x3B) + sta_abs(0xD011)
    code += lda_imm(0x18) + sta_abs(0xD018)
    code += [0x4C, 0x00, 0x00]
    loop_addr = CODE_ADDR + len(code) - 3
    code[-2] = loop_addr & 0xFF
    code[-1] = (loop_addr >> 8) & 0xFF
    return bytearray(code)

def main() -> None:
    ensure_spans()

    spans_data = json.loads((DIST / "single_cube_polygon_spans.json").read_text(encoding="utf-8"))
    faces_data = json.loads((DIST / "single_cube_polygon_faces.json").read_text(encoding="utf-8"))
    pit_segments = json.loads((DIST / "pit_line_segments.json").read_text(encoding="utf-8"))

    bitmap, screen, color_ram = build_bitmap_and_color(spans_data, faces_data, pit_segments)

    basic = emit_basic_stub()
    code = build_machine_code()

    program = bytearray()
    program += bytes(le_word(LOAD_ADDR))
    program += basic

    if LOAD_ADDR + len(basic) != CODE_ADDR:
        raise SystemExit(f"BASIC stub does not end at expected code address ${CODE_ADDR:04x}")

    program += code
    current_addr = LOAD_ADDR + len(basic) + len(code)

    if current_addr > BITMAP_SOURCE_ADDR:
        raise SystemExit("Machine code too large; overlaps source payload area")

    program += bytes([0x00] * (BITMAP_SOURCE_ADDR - current_addr))
    program += bitmap
    program += screen
    program += color_ram

    out_prg = DIST / "single_cube_span_fill.prg"
    out_meta = DIST / "single_cube_span_fill_metadata.json"

    out_prg.write_bytes(program)
    out_meta.write_text(json.dumps({
        "load_addr": f"${LOAD_ADDR:04x}",
        "code_addr": f"${CODE_ADDR:04x}",
        "bitmap_addr": f"${BITMAP_ADDR:04x}",
        "screen_addr": f"${SCREEN_ADDR:04x}",
        "source_spans": "dist/single_cube_polygon_spans.json",
        "source_pit_segments": "dist/pit_line_segments.json",
        "cube_context": "off_side_cube_in_perspective_pit",
        "total_spans": spans_data["total_spans"],
        "pit_line_segments": len(pit_segments),
        "mode": "C64 standard hi-res bitmap span-fill proof with pit context",
        "bitmap_bytes": len(bitmap),
        "screen_bytes": len(screen),
        "color_ram_bytes": len(color_ram),
        "program_bytes": len(program) - 2,
    }, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {out_prg}")
    print(f"Wrote {out_meta}")
    print(f"Built C64 pit-context span-fill PRG from {spans_data['total_spans']} generated spans and {len(pit_segments)} pit lines.")

if __name__ == "__main__":
    main()
