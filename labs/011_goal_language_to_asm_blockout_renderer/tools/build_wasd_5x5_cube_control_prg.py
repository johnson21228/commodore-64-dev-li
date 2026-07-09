#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

LOAD_ADDR = 0x0801
CODE_ADDR = 0x080D
BITMAP_ADDR = 0x6000
SCREEN_ADDR = 0x4400
COLOR_RAM_ADDR = 0xD800

WHITE = 1
GREEN = 5
BG = 0

PIT_W = 5
PIT_H = 5
PIT_VISUAL_DEPTH = 10

DEPTH_T_BY_Z = [0.00, 0.34, 0.56, 0.71, 0.81, 0.88, 0.93, 0.96, 0.98, 0.99, 1.00]
VISIBLE_RING_ZS = [0, 1, 2, 3, 4, 5, 6, 8, 10]

ZP_DST_LO = 0xF9
ZP_DST_HI = 0xFA
ZP_SRC_LO = 0xFB
ZP_SRC_HI = 0xFC
ZP_COUNT_LO = 0xFD
ZP_COUNT_HI = 0xFE
ZP_VALUE = 0xF8

def ensure_projection() -> None:
    subprocess.run(["python3", "tools/generate_blockout_renderer.py"], cwd=ROOT, check=True)

def project(intent: dict, x: float, y: float, z: float) -> tuple[int, int]:
    # Maximum square pit viewport inside the left playfield.
    play_y0 = 2
    play_y1 = 198
    pit_size = play_y1 - play_y0
    play_x0 = 30
    play_x1 = play_x0 + pit_size

    z_clamped = max(0.0, min(float(PIT_VISUAL_DEPTH), float(z)))
    z0 = int(z_clamped)
    z1 = min(PIT_VISUAL_DEPTH, z0 + 1)
    frac = z_clamped - z0
    t = DEPTH_T_BY_Z[z0] + (DEPTH_T_BY_Z[z1] - DEPTH_T_BY_Z[z0]) * frac

    near_w = play_x1 - play_x0
    near_h = play_y1 - play_y0
    far_w = 72
    far_h = 72

    width = near_w + (far_w - near_w) * t
    height = near_h + (far_h - near_h) * t

    cx = (play_x0 + play_x1) / 2
    cy = (play_y0 + play_y1) / 2

    left = cx - width / 2
    top = cy - height / 2

    # Use PIT_H for the in-plane Y dimension. Some older intent files use "depth"
    # for this footprint dimension; the proof is explicitly 5x5.
    return round(left + x * width / PIT_W), round(top + y * height / PIT_H)

def line_pixels(x1: int, y1: int, x2: int, y2: int):
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy
    x, y = x1, y1
    while True:
        if 0 <= x <= 319 and 0 <= y <= 199:
            yield x, y
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy

def bitmap_offset_mask(x: int, y: int) -> tuple[int, int]:
    off = (y // 8) * 320 + (x // 8) * 8 + (y % 8)
    mask = 1 << (7 - (x % 8))
    return off, mask

def add_line(bitmap: bytearray, x1: int, y1: int, x2: int, y2: int) -> None:
    for x, y in line_pixels(x1, y1, x2, y2):
        off, mask = bitmap_offset_mask(x, y)
        bitmap[off] |= mask

def pit_bitmap(intent: dict) -> bytearray:
    bitmap = bytearray(8000)

    # Selected rings reduce far/bottom pile-up while preserving true depth 10.
    for z in VISIBLE_RING_ZS:
        add_line(bitmap, *project(intent, 0, 0, z), *project(intent, PIT_W, 0, z))
        add_line(bitmap, *project(intent, PIT_W, 0, z), *project(intent, PIT_W, PIT_H, z))
        add_line(bitmap, *project(intent, PIT_W, PIT_H, z), *project(intent, 0, PIT_H, z))
        add_line(bitmap, *project(intent, 0, PIT_H, z), *project(intent, 0, 0, z))

    # All wall boundary grid guides for the 5x5 pit, no top-plane helper clutter.
    for x in range(PIT_W + 1):
        add_line(bitmap, *project(intent, x, 0, 0), *project(intent, x, 0, PIT_VISUAL_DEPTH))
        add_line(bitmap, *project(intent, x, PIT_H, 0), *project(intent, x, PIT_H, PIT_VISUAL_DEPTH))

    for y in range(PIT_H + 1):
        add_line(bitmap, *project(intent, 0, y, 0), *project(intent, 0, y, PIT_VISUAL_DEPTH))
        add_line(bitmap, *project(intent, PIT_W, y, 0), *project(intent, PIT_W, y, PIT_VISUAL_DEPTH))

    return bitmap

def pit_byte_records(bitmap: bytearray) -> list[tuple[int, int]]:
    return [(i, b) for i, b in enumerate(bitmap) if b != 0]

def le(v: int) -> list[int]:
    return [v & 255, (v >> 8) & 255]

def basic_stub() -> bytearray:
    return bytearray([0x0C, 0x08, 0x0A, 0x00, 0x9E, 50, 48, 54, 49, 0, 0, 0])

class A:
    def __init__(self, start: int):
        self.start = start
        self.c: list[int] = []
        self.labels: dict[str, int] = {}
        self.abs: list[tuple[int, str]] = []
        self.rel: list[tuple[int, str]] = []

    @property
    def pc(self) -> int:
        return self.start + len(self.c)

    def label(self, name: str) -> None:
        self.labels[name] = self.pc

    def e(self, *bs: int) -> None:
        self.c.extend(b & 255 for b in bs)

    def data(self, bs: bytes | bytearray) -> None:
        self.c.extend(bs)

    def lda_i(self, v: int): self.e(0xA9, v)
    def ldx_i(self, v: int): self.e(0xA2, v)
    def ldy_i(self, v: int): self.e(0xA0, v)
    def lda_abs(self, a: int): self.e(0xAD, *le(a))
    def sta_abs(self, a: int): self.e(0x8D, *le(a))
    def sta_zp(self, z: int): self.e(0x85, z)
    def lda_zp(self, z: int): self.e(0xA5, z)
    def ora_zp(self, z: int): self.e(0x05, z)
    def cmp_i(self, v: int): self.e(0xC9, v)
    def adc_i(self, v: int): self.e(0x69, v)
    def clc(self): self.e(0x18)
    def inc_zp(self, z: int): self.e(0xE6, z)
    def dec_zp(self, z: int): self.e(0xC6, z)
    def lda_x(self, a: int): self.e(0xBD, *le(a))
    def sta_x(self, a: int): self.e(0x9D, *le(a))
    def lda_ind_y(self, z: int): self.e(0xB1, z)
    def sta_ind_y(self, z: int): self.e(0x91, z)
    def jmp(self, l: str): self.e(0x4C, 0, 0); self.abs.append((len(self.c) - 2, l))
    def jsr(self, l: str): self.e(0x20, 0, 0); self.abs.append((len(self.c) - 2, l))
    def rts(self): self.e(0x60)
    def beq(self, l: str): self.e(0xF0, 0); self.rel.append((len(self.c) - 1, l))
    def bne(self, l: str): self.e(0xD0, 0); self.rel.append((len(self.c) - 1, l))

    def copy_page_fill(self, dst: int, count: int, value: int) -> None:
        self.lda_i(value)
        self.ldx_i(0)
        loop = self.pc
        self.sta_x(dst)
        self.e(0xE8)
        if count == 256:
            self.e(0xD0, (loop - (self.pc + 2)) & 255)
        else:
            self.e(0xE0, count & 255)
            self.e(0xD0, (loop - (self.pc + 2)) & 255)

    def fill_block(self, dst: int, n: int, value: int) -> None:
        for page in range(n // 256):
            self.copy_page_fill(dst + page * 256, 256, value)
        if n % 256:
            self.copy_page_fill(dst + (n // 256) * 256, n % 256, value)

    def fin(self) -> bytearray:
        for pos, label in self.abs:
            addr = self.labels[label]
            self.c[pos] = addr & 255
            self.c[pos + 1] = (addr >> 8) & 255
        for pos, label in self.rel:
            rel = self.labels[label] - (self.start + pos + 1)
            if not -128 <= rel <= 127:
                raise SystemExit(f"branch {label} out of range {rel}")
            self.c[pos] = rel & 255
        return bytearray(self.c)

def build_prg(records: list[tuple[int, int]]) -> tuple[bytearray, dict]:
    a = A(CODE_ADDR)

    # Black border/background.
    a.lda_i(0)
    a.sta_abs(0xD020)
    a.sta_abs(0xD021)

    # Prepare VIC-II bank 1: $4000-$7fff.
    # D018=$18 then means screen=$4400 and bitmap=$6000.
    # This keeps bitmap memory away from the program/compact-record table near $0801.
    a.lda_abs(0xDD00)
    a.e(0x29, 0xFC)  # AND #$FC
    a.e(0x09, 0x02)  # ORA #$02 -> VIC bank 1
    a.sta_abs(0xDD00)

    # Prepare VIC-II hi-res bitmap mode.
    a.lda_i(0x3B)
    a.sta_abs(0xD011)
    a.lda_i(0x18)
    a.sta_abs(0xD018)

    # Runtime generates static memory instead of loading full 8K+2K source payloads.
    a.fill_block(BITMAP_ADDR, 8000, 0)
    a.fill_block(SCREEN_ADDR, 1000, (GREEN << 4) | BG)
    a.fill_block(COLOR_RAM_ADDR, 1000, GREEN)

    # Draw compact pit byte records once.
    a.lda_i(0)
    a.sta_zp(ZP_SRC_LO)
    a.lda_i(0)
    a.sta_zp(ZP_SRC_HI)
    a.lda_i(len(records) & 255)
    a.sta_zp(ZP_COUNT_LO)
    a.lda_i((len(records) >> 8) & 255)
    a.sta_zp(ZP_COUNT_HI)
    a.jsr("draw_pit_records")

    a.label("idle")
    a.jmp("idle")

    a.label("draw_pit_records")
    a.lda_zp(ZP_COUNT_LO)
    a.ora_zp(ZP_COUNT_HI)
    a.bne("record_loop")
    a.rts()

    a.label("record_loop")
    # offset low
    a.ldy_i(0)
    a.lda_ind_y(ZP_SRC_LO)
    a.sta_zp(ZP_DST_LO)
    a.inc_zp(ZP_SRC_LO)
    a.bne("src1_ok")
    a.inc_zp(ZP_SRC_HI)
    a.label("src1_ok")

    # offset high + bitmap base high
    a.ldy_i(0)
    a.lda_ind_y(ZP_SRC_LO)
    a.clc()
    a.adc_i(BITMAP_ADDR >> 8)
    a.sta_zp(ZP_DST_HI)
    a.inc_zp(ZP_SRC_LO)
    a.bne("src2_ok")
    a.inc_zp(ZP_SRC_HI)
    a.label("src2_ok")

    # value
    a.ldy_i(0)
    a.lda_ind_y(ZP_SRC_LO)
    a.sta_zp(ZP_VALUE)
    a.inc_zp(ZP_SRC_LO)
    a.bne("src3_ok")
    a.inc_zp(ZP_SRC_HI)
    a.label("src3_ok")

    # write byte
    a.ldy_i(0)
    a.lda_zp(ZP_VALUE)
    a.sta_ind_y(ZP_DST_LO)

    # decrement count
    a.lda_zp(ZP_COUNT_LO)
    a.bne("dec_lo")
    a.dec_zp(ZP_COUNT_HI)
    a.label("dec_lo")
    a.dec_zp(ZP_COUNT_LO)

    a.lda_zp(ZP_COUNT_LO)
    a.ora_zp(ZP_COUNT_HI)
    a.bne("record_loop")
    a.rts()

    a.label("pit_records")
    for off, value in records:
        a.data(bytes([off & 255, (off >> 8) & 255, value]))

    code = a.fin()

    # Patch source pointer to pit_records.
    pit_addr = a.labels["pit_records"]
    patched = bytearray(code)
    pattern = bytes([0xA9, 0, 0x85, ZP_SRC_LO, 0xA9, 0, 0x85, ZP_SRC_HI])
    idx = patched.find(pattern)
    if idx < 0:
        raise SystemExit("missing pit record source pointer placeholder")
    patched[idx + 1] = pit_addr & 255
    patched[idx + 5] = (pit_addr >> 8) & 255

    program_end = LOAD_ADDR + len(basic_stub()) + len(patched)
    if program_end >= 0x4000:
        raise SystemExit(f"compact PRG code/data too large for VIC bank-1 layout: ends ${program_end:04x}")

    prg = bytearray()
    prg += bytes(le(LOAD_ADDR))
    prg += basic_stub()
    prg += patched

    meta = {
        "mode": "C64 pit-only compact-payload projection tuning proof",
        "pit": {"width": PIT_W, "height": PIT_H, "visual_depth": PIT_VISUAL_DEPTH, "target_style": "Blockout_like_5x5x10"},
        "projection_viewport": {
            "playfield": "left_square_max_height",
            "x_min": 30,
            "x_max": 226,
            "y_min": 2,
            "y_max": 198,
            "hud": "right_reserved_256_319",
            "square": True,
            "height_pixels": 196,
            "near_square_pixels": 196,
            "far_square_pixels": 72,
            "depth_bands": PIT_VISUAL_DEPTH,
            "visible_rings": PIT_VISUAL_DEPTH + 1,
            "drawn_ring_count": len(VISIBLE_RING_ZS),
            "visible_ring_zs": VISIBLE_RING_ZS,
            "ring_density": "skip_some_far_bottom_rings",
            "depth_spacing": "strong_explicit_near_rows_larger",
            "depth_t_by_z": DEPTH_T_BY_Z,
            "wall_grid_guides": "all_5x5_boundary_divisions",
            "top_plane_clutter": "none",
            "straight_depth_guides": True,
        },
        "active_piece_render": "disabled_pit_tuning",
        "payload_strategy": "compact_nonzero_bitmap_byte_records",
        "memory_layout": {"vic_bank": 1, "vic_bank_range": "$4000-$7fff", "screen_addr": "$4400", "bitmap_addr": "$6000", "reason": "avoid compact-record table overlap with bitmap memory"},
        "removed_payloads": ["full_8000_byte_pit_bitmap_source", "1000_byte_screen_source", "1000_byte_color_source"],
        "pit_record_count": len(records),
        "pit_record_payload_bytes": len(records) * 3,
        "program_bytes": len(prg) - 2,
        "note": "PIT-ONLY OPTIMIZED: the PRG no longer embeds a full 8000-byte pit bitmap plus screen/color source, and VIC display memory is moved to bank 1 to avoid compact-record overlap. It clears bitmap memory, fills screen/color at startup, then draws compact nonzero pit byte records once.",
    }
    return prg, meta

def main() -> None:
    ensure_projection()
    intent = json.loads((ROOT / "goal/renderer_intent.json").read_text(encoding="utf-8"))
    bitmap = pit_bitmap(intent)
    records = pit_byte_records(bitmap)

    DIST.mkdir(parents=True, exist_ok=True)
    prg, meta = build_prg(records)
    (DIST / "wasd_5x5_cube_control.prg").write_bytes(prg)
    (DIST / "wasd_5x5_cube_control_metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print("Wrote dist/wasd_5x5_cube_control.prg")
    print("Wrote dist/wasd_5x5_cube_control_metadata.json")
    print(f"Pit nonzero byte records: {len(records)}")
    print(f"Compact pit record payload bytes: {len(records) * 3}")
    print("Built pit-only compact-payload PRG.")

if __name__ == "__main__":
    main()
