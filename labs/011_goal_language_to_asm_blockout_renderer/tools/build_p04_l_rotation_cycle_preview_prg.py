#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
BASE_BUILDER = LAB / "tools" / "build_p02_domino_top_endpoint_preview_prg.py"
OUT_PRG = LAB / "dist" / "p04_l_rotation_cycle_preview.prg"
OUT_META = LAB / "dist" / "p04_l_rotation_cycle_preview_metadata.json"

LOAD_ADDR = 0x0801
SYS_ADDR = 0x080D
SCREEN_ADDR = 0x4400
BITMAP_ADDR = 0x6000
END_ADDR = 0x8000

STATE_ADDR = 0x02
PTR_LO = 0xFB
PTR_HI = 0xFC
CNT_LO = 0xFD
CNT_HI = 0xFE
MASK_ZP = 0x03

def load_base():
    spec = importlib.util.spec_from_file_location("p04_l_base", BASE_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base builder: {BASE_BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def bitmap_offset(x: int, y: int) -> int:
    return (y // 8) * 320 + (x // 8) * 8 + (y % 8)

def plot(record_map: dict[int, int], x: int, y: int) -> None:
    if not (0 <= x < 320 and 0 <= y < 200):
        return
    off = bitmap_offset(x, y)
    record_map[BITMAP_ADDR + off] = record_map.get(BITMAP_ADDR + off, 0) | (1 << (7 - (x % 8)))

def dashed_line(base, record_map: dict[int, int], a: tuple[int, int], b: tuple[int, int]) -> None:
    for i, (x, y) in enumerate(base.bresenham(a, b)):
        if (i % 7) < 2:
            plot(record_map, x, y)

def solid_line(base, record_map: dict[int, int], a: tuple[int, int], b: tuple[int, int]) -> None:
    for x, y in base.bresenham(a, b):
        plot(record_map, x, y)

# P04_L canonical from source:
# [[0,0,0], [1,0,0], [2,0,0], [0,1,0]]
# Shifted to fit center-ish in the 5x5 top level.
P04_L_Z_STATES = {
    0: [(1, 1, 0), (2, 1, 0), (3, 1, 0), (1, 2, 0)],
    1: [(3, 1, 0), (3, 2, 0), (3, 3, 0), (2, 1, 0)],
    2: [(1, 3, 0), (2, 3, 0), (3, 3, 0), (3, 2, 0)],
    3: [(1, 1, 0), (1, 2, 0), (1, 3, 0), (2, 3, 0)],
}

def segments_for_cells(base, cells: list[tuple[int, int, int]]) -> list[tuple[int, int, int, int]]:
    occupied = set(cells)
    face_defs = [
        ((-1, 0, 0), [(0,0,0),(0,1,0),(0,1,1),(0,0,1)]),
        ((1, 0, 0), [(1,0,0),(1,0,1),(1,1,1),(1,1,0)]),
        ((0, -1, 0), [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
        ((0, 1, 0), [(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
        ((0, 0, -1), [(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
        ((0, 0, 1), [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),
    ]
    edges = set()
    for x, y, z in cells:
        for (dx, dy, dz), corners in face_defs:
            if (x + dx, y + dy, z + dz) in occupied:
                continue
            verts = [(x + cx, y + cy, z + cz) for cx, cy, cz in corners]
            for i in range(4):
                a = verts[i]
                b = verts[(i + 1) % 4]
                edges.add(tuple(sorted([a, b])))

    out = []
    for a, b in sorted(edges):
        x1, y1 = base.project_vertex(a)
        x2, y2 = base.project_vertex(b)
        if (x1, y1) != (x2, y2):
            out.append((x1, y1, x2, y2))
    return sorted(set(out))

def frame_records(base, state: int) -> dict[int, int]:
    records: dict[int, int] = {}
    for a, b in base.add_pit_segments():
        dashed_line(base, records, a, b)
    for x1, y1, x2, y2 in segments_for_cells(base, P04_L_Z_STATES[state]):
        solid_line(base, records, (x1, y1), (x2, y2))
    return records

class Asm:
    def __init__(self, addr: int):
        self.addr = addr
        self.bytes = bytearray()
        self.labels: dict[str, int] = {}
        self.patches: list[tuple[int, str, str]] = []

    @property
    def pc(self) -> int:
        return self.addr + len(self.bytes)

    def label(self, name: str) -> None:
        self.labels[name] = self.pc

    def emit(self, *vals: int) -> None:
        self.bytes.extend(v & 0xff for v in vals)

    def abs_patch(self, label: str) -> None:
        pos = len(self.bytes)
        self.emit(0, 0)
        self.patches.append((pos, label, "abs"))

    def rel_patch(self, label: str) -> None:
        pos = len(self.bytes)
        self.emit(0)
        self.patches.append((pos, label, "rel"))

    def resolve(self) -> bytes:
        out = bytearray(self.bytes)
        for pos, label, kind in self.patches:
            target = self.labels[label]
            if kind == "abs":
                out[pos] = target & 0xff
                out[pos + 1] = (target >> 8) & 0xff
            else:
                branch_from = self.addr + pos + 1
                delta = target - branch_from
                if not -128 <= delta <= 127:
                    raise RuntimeError(f"branch to {label} out of range: {delta}")
                out[pos] = delta & 0xff
        return bytes(out)

def build_code(table_addrs: dict[int, int], counts: dict[int, int]) -> bytes:
    a = Asm(SYS_ADDR)

    def lda_imm(v): a.emit(0xA9, v)
    def ldx_imm(v): a.emit(0xA2, v)
    def ldy_imm(v): a.emit(0xA0, v)
    def lda_zp(z): a.emit(0xA5, z)
    def sta_zp(z): a.emit(0x85, z)
    def inc_zp(z): a.emit(0xE6, z)
    def dec_zp(z): a.emit(0xC6, z)
    def sta_abs(addr): a.emit(0x8D, addr & 0xff, (addr >> 8) & 0xff)
    def lda_abs(addr): a.emit(0xAD, addr & 0xff, (addr >> 8) & 0xff)
    def cmp_imm(v): a.emit(0xC9, v)
    def and_imm(v): a.emit(0x29, v)
    def ora_imm(v): a.emit(0x09, v)
    def beq(label): a.emit(0xF0); a.rel_patch(label)
    def bne(label): a.emit(0xD0); a.rel_patch(label)
    def bpl(label): a.emit(0x10); a.rel_patch(label)
    def jsr(label): a.emit(0x20); a.abs_patch(label)
    def jmp(label): a.emit(0x4C); a.abs_patch(label)

    # Init video.
    lda_abs(0xDD00); and_imm(0xFC); ora_imm(0x02); sta_abs(0xDD00)
    lda_imm(0x00); sta_abs(0xD020); sta_abs(0xD021)
    lda_imm(0x3B); sta_abs(0xD011)
    lda_imm(0x08); sta_abs(0xD016)
    lda_imm(0x18); sta_abs(0xD018)

    lda_imm(0); sta_zp(STATE_ADDR)
    jsr("fill_screen")
    jsr("draw_by_state")

    a.label("main")
    a.emit(0x20, 0xE4, 0xFF)  # GETIN
    cmp_imm(0x00); beq("main")

    # ASAP visual proof: all positive rotation keys advance; all negative keys reverse.
    # This makes repeated keypresses visibly continue around the L shape.
    cmp_imm(ord("A")); beq("next")
    cmp_imm(ord("S")); beq("next")
    cmp_imm(ord("D")); beq("next")
    cmp_imm(ord("Q")); beq("prev")
    cmp_imm(ord("W")); beq("prev")
    cmp_imm(ord("E")); beq("prev")
    jmp("main")

    a.label("next")
    inc_zp(STATE_ADDR)
    lda_zp(STATE_ADDR)
    cmp_imm(4)
    bne("redraw")
    lda_imm(0)
    sta_zp(STATE_ADDR)
    jmp("redraw")

    a.label("prev")
    lda_zp(STATE_ADDR)
    bne("prev_dec")
    lda_imm(3)
    sta_zp(STATE_ADDR)
    jmp("redraw")
    a.label("prev_dec")
    dec_zp(STATE_ADDR)
    jmp("redraw")

    a.label("redraw")
    jsr("draw_by_state")
    jmp("main")

    a.label("draw_by_state")
    lda_zp(STATE_ADDR)
    cmp_imm(0); beq("draw_0")
    cmp_imm(1); beq("draw_1")
    cmp_imm(2); beq("draw_2")
    jmp("draw_3")

    def draw_state(label: str, state: int):
        a.label(label)
        jsr("clear_bitmap")
        addr = table_addrs[state]
        lda_imm(addr & 0xff); sta_zp(PTR_LO)
        lda_imm((addr >> 8) & 0xff); sta_zp(PTR_HI)
        count = counts[state]
        lda_imm(count & 0xff); sta_zp(CNT_LO)
        lda_imm((count >> 8) & 0xff); sta_zp(CNT_HI)
        jsr("draw_records")
        a.emit(0x60)

    for state in range(4):
        draw_state(f"draw_{state}", state)

    a.label("fill_screen")
    lda_imm(0x10)
    ldx_imm(0)
    a.label("fill_loop")
    for base in [SCREEN_ADDR, SCREEN_ADDR + 0x100, SCREEN_ADDR + 0x200]:
        a.emit(0x9D, base & 0xff, (base >> 8) & 0xff)
    a.emit(0xE0, 0xE8)  # CPX #232
    beq("fill_skip_tail")
    a.emit(0x9D, (SCREEN_ADDR + 0x2E8) & 0xff, ((SCREEN_ADDR + 0x2E8) >> 8) & 0xff)
    a.label("fill_skip_tail")
    a.emit(0xE8)
    bne("fill_loop")
    a.emit(0x60)

    a.label("clear_bitmap")
    lda_imm(0)
    ldx_imm(0)
    a.label("clear_page_loop")
    for high in range(0x60, 0x7F):
        a.emit(0x9D, 0x00, high)
    a.emit(0xE8)
    bne("clear_page_loop")
    ldx_imm(0x3F)
    a.label("clear_tail_loop")
    a.emit(0x9D, 0x00, 0x7F)
    a.emit(0xCA)  # DEX
    bpl("clear_tail_loop")
    a.emit(0x60)

    a.label("draw_records")
    a.label("draw_loop")
    lda_zp(CNT_LO)
    a.emit(0x05, CNT_HI)  # ORA cnt hi
    beq("draw_done")
    ldy_imm(0)
    a.emit(0xB1, PTR_LO)  # LDA (ptr),Y addr lo
    sta_abs(0x0330)
    sta_abs(0x0333)
    a.emit(0xC8)
    a.emit(0xB1, PTR_LO)  # addr hi
    sta_abs(0x0331)
    sta_abs(0x0334)
    a.emit(0xC8)
    a.emit(0xB1, PTR_LO)  # mask
    sta_zp(MASK_ZP)

    a.emit(0xAD)
    a.label("target_lda_lo"); a.emit(0)
    a.label("target_lda_hi"); a.emit(0)
    a.emit(0x05, MASK_ZP)
    a.emit(0x8D)
    a.label("target_sta_lo"); a.emit(0)
    a.label("target_sta_hi"); a.emit(0)

    # ptr += 3
    a.emit(0x18)
    lda_zp(PTR_LO)
    a.emit(0x69, 0x03)
    sta_zp(PTR_LO)
    a.emit(0x90, 0x02)
    a.emit(0xE6, PTR_HI)
    # count -= 1
    lda_zp(CNT_LO)
    a.emit(0xD0, 0x02)
    a.emit(0xC6, CNT_HI)
    a.emit(0xC6, CNT_LO)
    jmp("draw_loop")

    a.label("draw_done")
    a.emit(0x60)

    code = bytearray(a.resolve())
    for placeholder, label in [
        (0x0330, "target_lda_lo"),
        (0x0331, "target_lda_hi"),
        (0x0333, "target_sta_lo"),
        (0x0334, "target_sta_hi"),
    ]:
        target = a.labels[label]
        needle = bytes([placeholder & 0xff, (placeholder >> 8) & 0xff])
        idx = code.find(needle)
        if idx < 0:
            raise RuntimeError(f"Could not find placeholder {hex(placeholder)}")
        code[idx:idx+2] = bytes([target & 0xff, (target >> 8) & 0xff])
    return bytes(code)

def basic_stub() -> bytes:
    return bytes([0x0c, 0x08, 0x0a, 0x00, 0x9e, 0x32, 0x30, 0x36, 0x31, 0x00, 0x00, 0x00])

def main() -> None:
    base = load_base()
    records = {state: frame_records(base, state) for state in range(4)}
    counts = {state: len(records[state]) for state in records}
    blobs = {}
    for state, recs in records.items():
        blob = bytearray()
        for addr, mask in sorted(recs.items()):
            blob.extend([addr & 0xff, (addr >> 8) & 0xff, mask & 0xff])
        blobs[state] = bytes(blob)

    dummy = {0: 0x2000, 1: 0x3000, 2: 0x4000, 3: 0x5000}
    code0 = build_code(dummy, counts)
    base_len = len(basic_stub()) + len(code0)
    pad = (16 - ((LOAD_ADDR + base_len) % 16)) % 16
    table_addrs = {}
    cursor = LOAD_ADDR + base_len + pad
    for state in range(4):
        table_addrs[state] = cursor
        cursor += len(blobs[state])
    code = build_code(table_addrs, counts)

    program = bytearray()
    program.extend(basic_stub())
    program.extend(code)
    while (LOAD_ADDR + len(program)) % 16 != 0:
        program.append(0)

    actual = {}
    for state in range(4):
        actual[state] = LOAD_ADDR + len(program)
        program.extend(blobs[state])
    if actual != table_addrs:
        raise RuntimeError(f"table address mismatch: planned {table_addrs}, actual {actual}")

    image_size = END_ADDR - LOAD_ADDR
    if len(program) + 2 > image_size:
        raise RuntimeError(f"program too large: {len(program) + 2}")

    image = bytearray([0] * image_size)
    image[0:2] = bytes([LOAD_ADDR & 0xff, LOAD_ADDR >> 8])
    image[2:2 + len(program)] = program
    screen_start = SCREEN_ADDR - LOAD_ADDR + 2
    image[screen_start:screen_start + 1000] = bytes([0x10] * 1000)

    OUT_PRG.parent.mkdir(parents=True, exist_ok=True)
    OUT_PRG.write_bytes(bytes(image))

    meta = {
        "schemaVersion": 1,
        "program": str(OUT_PRG),
        "pieceId": "P04_L",
        "mode": "P04_L visible four-state rotation-cycle preview",
        "sourcePiece": {
            "pieceId": "P04_L",
            "canonicalCubes": [[0,0,0], [1,0,0], [2,0,0], [0,1,0]],
            "description": "Four-cube long L from existing blockout_piece_source.json"
        },
        "controls": {
            "A/S/D": "advance one visible 90-degree step",
            "Q/W/E": "reverse one visible 90-degree step"
        },
        "states": {
            str(state): {
                "rotationDegrees": state * 90,
                "occupiedCells": P04_L_Z_STATES[state],
                "recordCount": counts[state],
                "recordBytes": len(blobs[state])
            }
            for state in range(4)
        },
        "cycle": "0 -> 1 -> 2 -> 3 -> 0",
        "lineLanguage": {
            "pit": "white subtle dashed lines",
            "activeBlock": "solid white outline"
        },
        "note": "ASAP visual proof that an asymmetric L-shaped block keeps rotating around. This uses z-plane four-state visual rotation before generalized 3D axis rotation.",
        "memoryLayout": {
            "loadAddress": hex(LOAD_ADDR),
            "sysAddress": hex(SYS_ADDR),
            "screenAddress": hex(SCREEN_ADDR),
            "bitmapAddress": hex(BITMAP_ADDR),
            "tableAddresses": {str(k): hex(v) for k, v in table_addrs.items()},
            "machineCodeBytes": len(code),
            "programBytesBeforeImagePad": len(program) + 2,
        },
        "prgBytes": len(image),
        "runtimeKeyboard": True,
        "runtimeStatefulRotation": True,
        "runtimeLineDrawing": False,
        "previewOnly": True,
    }
    OUT_META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_PRG}")
    print(f"Wrote {OUT_META}")
    print(json.dumps({
        "pieceId": meta["pieceId"],
        "controls": meta["controls"],
        "cycle": meta["cycle"],
        "states": meta["states"],
        "prgBytes": meta["prgBytes"],
    }, indent=2))

if __name__ == "__main__":
    main()
