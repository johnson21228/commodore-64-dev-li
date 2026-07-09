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

# This proof uses generated unrolled byte writes. It is not a general renderer yet.
CUBE_COLOR = 2
PIT_COLOR = 1
BG_COLOR = 0

def ensure_byte_spans() -> None:
    subprocess.run(["python3", "tools/generate_moving_cube_byte_spans.py"], cwd=ROOT, check=True)

def c64_bitmap_offset(x: int, y: int) -> int:
    return (y // 8) * 320 + (x // 8) * 8 + (y % 8)

def set_pixel(bitmap: bytearray, x: int, y: int) -> None:
    if not 0 <= x <= 319 or not 0 <= y <= 199:
        return
    off = c64_bitmap_offset(x, y)
    if 0 <= off < len(bitmap):
        bitmap[off] |= 1 << (7 - (x % 8))

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

def add_pit_context(bitmap: bytearray) -> None:
    pit_path = DIST / "pit_line_segments.json"
    if not pit_path.exists():
        subprocess.run(["python3", "tools/generate_blockout_renderer.py"], cwd=ROOT, check=True)
    for s in json.loads(pit_path.read_text(encoding="utf-8")):
        add_line(bitmap, s["x1"], s["y1"], s["x2"], s["y2"])

def le_word(v: int) -> list[int]:
    return [v & 0xFF, (v >> 8) & 0xFF]

def emit_basic_stub() -> bytearray:
    # BASIC: 10 SYS2061
    return bytearray([0x0C, 0x08, 0x0A, 0x00, 0x9E, ord("2"), ord("0"), ord("6"), ord("1"), 0x00, 0x00, 0x00])

def lda_imm(v: int) -> list[int]: return [0xA9, v & 0xFF]
def ldx_imm(v: int) -> list[int]: return [0xA2, v & 0xFF]
def ldy_imm(v: int) -> list[int]: return [0xA0, v & 0xFF]
def sta_abs(addr: int) -> list[int]: return [0x8D, addr & 0xFF, (addr >> 8) & 0xFF]
def ora_abs(addr: int) -> list[int]: return [0x0D, addr & 0xFF, (addr >> 8) & 0xFF]
def and_abs(addr: int) -> list[int]: return [0x2D, addr & 0xFF, (addr >> 8) & 0xFF]

def delay_code(outer: int = 12) -> list[int]:
    # Approx small visible delay: nested X/Y countdown.
    # LDY #outer
    # outer_loop:
    #   LDX #255
    # inner_loop:
    #   DEX
    #   BNE inner_loop
    #   DEY
    #   BNE outer_loop
    code = []
    code += ldy_imm(outer)
    outer_loop_index = len(code)
    code += ldx_imm(255)
    inner_loop_index = len(code)
    code += [0xCA]  # DEX
    code += [0xD0, ((inner_loop_index - (len(code) + 2)) & 0xFF)]
    code += [0x88]  # DEY
    code += [0xD0, ((outer_loop_index - (len(code) + 2)) & 0xFF)]
    return code

def copy_page_loop(src: int, dst: int, count: int) -> list[int]:
    code: list[int] = []
    code += ldx_imm(0)
    loop_start = len(code)
    code += [0xBD, src & 0xFF, (src >> 8) & 0xFF]  # LDA src,X
    code += [0x9D, dst & 0xFF, (dst >> 8) & 0xFF]  # STA dst,X
    code += [0xE8]  # INX
    if count == 256:
        code += [0xD0, ((loop_start - (len(code) + 2)) & 0xFF)]
    else:
        code += [0xE0, count & 0xFF]  # CPX #count
        code += [0xD0, ((loop_start - (len(code) + 2)) & 0xFF)]
    return code

def copy_block(src: int, dst: int, length: int) -> list[int]:
    code: list[int] = []
    for page in range(length // 256):
        code += copy_page_loop(src + page * 256, dst + page * 256, 256)
    rem = length % 256
    if rem:
        code += copy_page_loop(src + (length // 256) * 256, dst + (length // 256) * 256, rem)
    return code

def frame_records(byte_data: dict) -> list[list[dict]]:
    frames = []
    for frame in byte_data["frames"]:
        frames.append(frame["records"])
    return frames

def union_offsets(frames: list[list[dict]]) -> list[int]:
    return sorted({r["bitmap_offset"] for records in frames for r in records})

def emit_clear_offsets(offsets: list[int]) -> list[int]:
    code: list[int] = []
    code += lda_imm(0)
    for off in offsets:
        code += sta_abs(BITMAP_ADDR + off)
    return code

def emit_draw_records(records: list[dict]) -> list[int]:
    code: list[int] = []
    for r in records:
        addr = BITMAP_ADDR + r["bitmap_offset"]
        mask = r["mask"] & 0xFF
        # LDA #mask ; ORA bitmap_addr ; STA bitmap_addr
        code += lda_imm(mask)
        code += ora_abs(addr)
        code += sta_abs(addr)
    return code

def emit_screen_color_init() -> tuple[bytearray, bytearray]:
    screen = bytearray([((CUBE_COLOR & 0x0F) << 4) | BG_COLOR] * 1000)
    color = bytearray([CUBE_COLOR] * 1000)
    return screen, color

def build_prg(byte_data: dict) -> tuple[bytearray, dict]:
    frames = frame_records(byte_data)
    offsets = union_offsets(frames)

    pit_bitmap = bytearray(8000)
    add_pit_context(pit_bitmap)
    screen, color = emit_screen_color_init()

    # Payload is copied once: pit bitmap + screen/color. Cube movement is code.
    PIT_SOURCE_ADDR = 0x6000
    SCREEN_SOURCE_ADDR = PIT_SOURCE_ADDR + 8000
    COLOR_SOURCE_ADDR = SCREEN_SOURCE_ADDR + 1000

    code: list[int] = []
    code += lda_imm(0x00) + sta_abs(0xD020) + sta_abs(0xD021)
    code += copy_block(PIT_SOURCE_ADDR, BITMAP_ADDR, 8000)
    code += copy_block(SCREEN_SOURCE_ADDR, SCREEN_ADDR, 1000)
    code += copy_block(COLOR_SOURCE_ADDR, COLOR_RAM_ADDR, 1000)

    # bitmap mode, screen at $0400, bitmap at $2000
    code += lda_imm(0x3B) + sta_abs(0xD011)
    code += lda_imm(0x18) + sta_abs(0xD018)

    animation_start_offset = len(code)

    for records in frames:
        code += emit_clear_offsets(offsets)
        code += emit_draw_records(records)
        code += delay_code(outer=18)

    # JMP animation_start
    animation_start_addr = CODE_ADDR + animation_start_offset
    code += [0x4C, animation_start_addr & 0xFF, (animation_start_addr >> 8) & 0xFF]

    basic = emit_basic_stub()
    program = bytearray()
    program += bytes(le_word(LOAD_ADDR))
    program += basic

    if LOAD_ADDR + len(basic) != CODE_ADDR:
        raise SystemExit("BASIC stub/code address mismatch")

    program += bytes(code)
    current_addr = LOAD_ADDR + len(basic) + len(code)
    if current_addr > PIT_SOURCE_ADDR:
        raise SystemExit(f"Generated animation code too large: ends at ${current_addr:04x}, payload starts at ${PIT_SOURCE_ADDR:04x}")

    program += bytes([0] * (PIT_SOURCE_ADDR - current_addr))
    program += pit_bitmap
    program += screen
    program += color

    metadata = {
        "mode": "C64 moving cube byte-span animation proof",
        "source": "dist/moving_cube_same_depth_byte_spans.json",
        "load_addr": f"${LOAD_ADDR:04x}",
        "code_addr": f"${CODE_ADDR:04x}",
        "bitmap_addr": f"${BITMAP_ADDR:04x}",
        "frame_count": len(frames),
        "union_clear_offsets": len(offsets),
        "max_frame_byte_records": max(len(f) for f in frames),
        "generated_code_bytes": len(code),
        "program_bytes": len(program) - 2,
        "timing_note": "This is emulator-visible byte-span animation. Next milestone should add raster/timer instrumentation for cycle measurement."
    }

    return program, metadata

def main() -> None:
    ensure_byte_spans()
    byte_data = json.loads((DIST / "moving_cube_same_depth_byte_spans.json").read_text(encoding="utf-8"))
    program, metadata = build_prg(byte_data)

    out_prg = DIST / "moving_cube_byte_span_animation.prg"
    out_meta = DIST / "moving_cube_byte_span_animation_metadata.json"
    out_prg.write_bytes(program)
    out_meta.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {out_prg}")
    print(f"Wrote {out_meta}")
    print(f"Built moving cube byte-span animation PRG with {metadata['frame_count']} frames.")

if __name__ == "__main__":
    main()
