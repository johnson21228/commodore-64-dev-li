#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
BASE_BUILDER = LAB / "tools" / "build_p02_domino_top_endpoint_preview_prg.py"
OUT_PRG = LAB / "dist" / "p02_domino_full_rotation_keys_preview.prg"
OUT_META = LAB / "dist" / "p02_domino_full_rotation_keys_preview_metadata.json"

LOAD_ADDR = 0x0801
SYS_ADDR = 0x080D
SCREEN_ADDR = 0x4400
BITMAP_ADDR = 0x6000
END_ADDR = 0x8000

ZP_PTR = 0xFB
ZP_CNT = 0xFD
ZP_MASK = 0x02

def load_base():
    spec = importlib.util.spec_from_file_location("p02_top_endpoint_base", BASE_BUILDER)
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

def occupied_cells_for_orientation(orientation: str) -> list[tuple[int, int, int]]:
    if orientation == "x_axis":
        return [(1, 2, 0), (2, 2, 0)]
    if orientation == "y_axis":
        return [(2, 1, 0), (2, 2, 0)]
    if orientation == "z_axis":
        return [(2, 2, 0), (2, 2, 1)]
    raise ValueError(orientation)

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

def frame_records(base, orientation: str) -> dict[int, int]:
    records: dict[int, int] = {}
    for a, b in base.add_pit_segments():
        dashed_line(base, records, a, b)
    for x1, y1, x2, y2 in segments_for_cells(base, occupied_cells_for_orientation(orientation)):
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

    def imm_lohi(self, addr: int) -> tuple[int, int]:
        return addr & 0xff, (addr >> 8) & 0xff

    def rel(self, label: str) -> None:
        pos = len(self.bytes)
        self.emit(0)
        self.patches.append((pos, label, "rel"))

    def abs(self, label: str) -> None:
        pos = len(self.bytes)
        self.emit(0, 0)
        self.patches.append((pos, label, "abs"))

    def resolve(self) -> bytes:
        out = bytearray(self.bytes)
        for pos, label, kind in self.patches:
            target = self.labels[label]
            if kind == "abs":
                out[pos] = target & 0xff
                out[pos + 1] = (target >> 8) & 0xff
            elif kind == "rel":
                branch_from = self.addr + pos + 1
                delta = target - branch_from
                if not -128 <= delta <= 127:
                    raise RuntimeError(f"relative branch out of range to {label}: {delta}")
                out[pos] = delta & 0xff
        return bytes(out)

def build_code(table_addrs: dict[str, int], counts: dict[str, int]) -> bytes:
    a = Asm(SYS_ADDR)

    def lda_imm(v): a.emit(0xA9, v)
    def ldx_imm(v): a.emit(0xA2, v)
    def ldy_imm(v): a.emit(0xA0, v)
    def sta_abs(addr): a.emit(0x8D, addr & 0xff, (addr >> 8) & 0xff)
    def lda_abs(addr): a.emit(0xAD, addr & 0xff, (addr >> 8) & 0xff)
    def and_imm(v): a.emit(0x29, v)
    def ora_imm(v): a.emit(0x09, v)
    def cmp_imm(v): a.emit(0xC9, v)
    def beq(label): a.emit(0xF0); a.rel(label)
    def bne(label): a.emit(0xD0); a.rel(label)
    def jsr(label): a.emit(0x20); a.abs(label)
    def jmp(label): a.emit(0x4C); a.abs(label)

    # Init VIC: bank $4000-$7fff, screen $4400, bitmap $6000.
    lda_abs(0xDD00); and_imm(0xFC); ora_imm(0x02); sta_abs(0xDD00)
    lda_imm(0x00); sta_abs(0xD020); sta_abs(0xD021)
    lda_imm(0x3B); sta_abs(0xD011)
    lda_imm(0x08); sta_abs(0xD016)
    lda_imm(0x18); sta_abs(0xD018)

    jsr("fill_screen")
    jsr("draw_x")

    a.label("main")
    a.emit(0x20, 0xE4, 0xFF)       # JSR GETIN
    cmp_imm(0x00); beq("main")
    cmp_imm(ord("A")); beq("do_x")
    cmp_imm(ord("Q")); beq("do_x")
    cmp_imm(ord("S")); beq("do_y")
    cmp_imm(ord("W")); beq("do_y")
    cmp_imm(ord("D")); beq("do_z")
    cmp_imm(ord("E")); beq("do_z")
    jmp("main")

    a.label("do_x"); jsr("draw_x"); jmp("main")
    a.label("do_y"); jsr("draw_y"); jmp("main")
    a.label("do_z"); jsr("draw_z"); jmp("main")

    def draw_sub(label: str, table: str, count_key: str):
        a.label(label)
        jsr("clear_bitmap")
        addr = table_addrs[table]
        lda_imm(addr & 0xff); a.emit(0x85, ZP_PTR)
        lda_imm((addr >> 8) & 0xff); a.emit(0x85, ZP_PTR + 1)
        count = counts[count_key]
        lda_imm(count & 0xff); a.emit(0x85, ZP_CNT)
        lda_imm((count >> 8) & 0xff); a.emit(0x85, ZP_CNT + 1)
        jsr("draw_records")
        a.emit(0x60)

    draw_sub("draw_x", "records_x", "x_axis")
    draw_sub("draw_y", "records_y", "y_axis")
    draw_sub("draw_z", "records_z", "z_axis")

    # Fill screen color bytes with white foreground / black background.
    a.label("fill_screen")
    lda_imm(0x10)
    ldx_imm(0x00)
    a.label("fill_loop")
    for base in [SCREEN_ADDR, SCREEN_ADDR + 0x100, SCREEN_ADDR + 0x200]:
        a.emit(0x9D, base & 0xff, (base >> 8) & 0xff)  # STA base,X
    # Last 232 bytes at $46E8-$47CF
    a.emit(0xE0, 0xE8)  # CPX #$E8
    beq("fill_no_tail")
    a.emit(0x9D, (SCREEN_ADDR + 0x2E8) & 0xff, ((SCREEN_ADDR + 0x2E8) >> 8) & 0xff)
    a.label("fill_no_tail")
    a.emit(0xE8)  # INX
    bne("fill_loop")
    a.emit(0x60)

    # Clear $6000-$7F3F = 8000 bytes.
    a.label("clear_bitmap")
    lda_imm(0x00)
    ldx_imm(0x00)
    a.label("clear_page_loop")
    for high in range(0x60, 0x7F):
        a.emit(0x9D, 0x00, high)
    a.emit(0xE8)
    bne("clear_page_loop")
    ldx_imm(0x3F)
    a.label("clear_tail_loop")
    a.emit(0x9D, 0x00, 0x7F)
    a.emit(0xCA)       # DEX
    a.emit(0x10); a.rel("clear_tail_loop")  # BPL
    a.emit(0x60)

    # Draw count records from (ZP_PTR). Each record is addr_lo, addr_hi, mask.
    a.label("draw_records")
    a.label("draw_loop")
    a.emit(0xA5, ZP_CNT)       # LDA count lo
    a.emit(0x05, ZP_CNT + 1)   # ORA count hi
    beq("draw_done")

    ldy_imm(0x00)
    a.emit(0xB1, ZP_PTR)       # LDA (ptr),Y
    sta_abs(0x0330)            # self-mod target low
    sta_abs(0x0333)
    a.emit(0xC8)               # INY
    a.emit(0xB1, ZP_PTR)
    sta_abs(0x0331)            # self-mod target high
    sta_abs(0x0334)
    a.emit(0xC8)
    a.emit(0xB1, ZP_PTR)
    a.emit(0x85, ZP_MASK)

    # Self-modified:
    # LDA $0000 / ORA mask / STA $0000
    a.emit(0xAD)
    a.label("target_lda_lo"); a.emit(0x00)
    a.label("target_lda_hi"); a.emit(0x00)
    a.emit(0x05, ZP_MASK)
    a.emit(0x8D)
    a.label("target_sta_lo"); a.emit(0x00)
    a.label("target_sta_hi"); a.emit(0x00)

    # Patch locations must be the actual operand bytes.
    # Labels are left for readability; the runtime writes into absolute addresses below.
    # Now PTR += 3.
    a.emit(0x18)               # CLC
    a.emit(0xA5, ZP_PTR)
    a.emit(0x69, 0x03)
    a.emit(0x85, ZP_PTR)
    a.emit(0x90, 0x02)         # BCC +2
    a.emit(0xE6, ZP_PTR + 1)

    # count--
    a.emit(0xA5, ZP_CNT)
    a.emit(0xD0, 0x02)
    a.emit(0xC6, ZP_CNT + 1)
    a.emit(0xC6, ZP_CNT)
    jmp("draw_loop")

    a.label("draw_done")
    a.emit(0x60)

    code = bytearray(a.resolve())

    # Find self-mod operand addresses dynamically and patch the two STA $0330/$0331/$0333/$0334 sites.
    # We know labels became code addresses; convert them to fixed RAM addresses to self-modify.
    # The prior generated code wrote to $0330 etc as placeholders. Replace those operands with
    # target operand byte locations in the loaded program.
    addr_labels = {
        0x0330: a.labels["target_lda_lo"],
        0x0331: a.labels["target_lda_hi"],
        0x0333: a.labels["target_sta_lo"],
        0x0334: a.labels["target_sta_hi"],
    }
    for placeholder, target in addr_labels.items():
        needle = bytes([placeholder & 0xff, (placeholder >> 8) & 0xff])
        replace = bytes([target & 0xff, (target >> 8) & 0xff])
        # Replace first occurrence for each placeholder in order.
        idx = code.find(needle)
        if idx < 0:
            raise RuntimeError(f"Could not find placeholder {hex(placeholder)}")
        code[idx:idx+2] = replace

    return bytes(code)

def basic_stub() -> bytes:
    # 10 SYS 2061
    return bytes([0x0c, 0x08, 0x0a, 0x00, 0x9e, 0x32, 0x30, 0x36, 0x31, 0x00, 0x00, 0x00])

def main() -> None:
    base = load_base()
    orientations = ["x_axis", "y_axis", "z_axis"]
    records = {o: frame_records(base, o) for o in orientations}
    counts = {o: len(records[o]) for o in orientations}

    # Build record bytes first.
    table_blobs = {}
    for orientation in orientations:
        blob = bytearray()
        for addr, mask in sorted(records[orientation].items()):
            blob.extend([addr & 0xff, (addr >> 8) & 0xff, mask & 0xff])
        table_blobs[orientation] = bytes(blob)

    # Estimate code length by placing tables at dummy addresses, then compute actual addresses and rebuild.
    dummy = {"records_x": 0x2000, "records_y": 0x2200, "records_z": 0x2400}
    code0 = build_code(dummy, counts)
    program_without_tables_len = len(basic_stub()) + len(code0)
    align_pad = (16 - ((LOAD_ADDR + program_without_tables_len) % 16)) % 16
    records_x_addr = LOAD_ADDR + program_without_tables_len + align_pad
    records_y_addr = records_x_addr + len(table_blobs["x_axis"])
    records_z_addr = records_y_addr + len(table_blobs["y_axis"])
    table_addrs = {"records_x": records_x_addr, "records_y": records_y_addr, "records_z": records_z_addr}
    code = build_code(table_addrs, counts)

    program = bytearray()
    program.extend(basic_stub())
    program.extend(code)
    while (LOAD_ADDR + len(program)) % 16 != 0:
        program.append(0x00)
    actual_x = LOAD_ADDR + len(program)
    program.extend(table_blobs["x_axis"])
    actual_y = LOAD_ADDR + len(program)
    program.extend(table_blobs["y_axis"])
    actual_z = LOAD_ADDR + len(program)
    program.extend(table_blobs["z_axis"])

    if (actual_x, actual_y, actual_z) != (records_x_addr, records_y_addr, records_z_addr):
        raise RuntimeError("record table address planning mismatch")

    image_size = END_ADDR - LOAD_ADDR
    if len(program) + 2 > image_size:
        raise RuntimeError(f"Program too large for image: {len(program)+2} > {image_size}")

    image = bytearray([0x00] * image_size)
    image[0:2] = bytes([LOAD_ADDR & 0xff, LOAD_ADDR >> 8])
    image[2:2 + len(program)] = program
    screen_start = SCREEN_ADDR - LOAD_ADDR + 2
    image[screen_start:screen_start + 1000] = bytes([0x10] * 1000)

    OUT_PRG.parent.mkdir(parents=True, exist_ok=True)
    OUT_PRG.write_bytes(bytes(image))

    meta = {
        "schemaVersion": 2,
        "program": str(OUT_PRG),
        "mode": "P02_DOMINO full rotation keys preview",
        "controls": {
            "A": "x_axis orientation",
            "Q": "x_axis orientation",
            "S": "y_axis orientation",
            "W": "y_axis orientation",
            "D": "z_axis orientation",
            "E": "z_axis orientation"
        },
        "note": "ASAP interactive proof. Keys select the three unique domino orientations. This is not final gameplay rotation state or lean endpoint runtime yet.",
        "lineLanguage": {
            "pit": "white subtle dashed lines",
            "activeBlock": "solid white outline"
        },
        "orientations": {
            "x_axis": {"occupiedCells": occupied_cells_for_orientation("x_axis"), "recordBytes": len(table_blobs["x_axis"]), "recordCount": counts["x_axis"]},
            "y_axis": {"occupiedCells": occupied_cells_for_orientation("y_axis"), "recordBytes": len(table_blobs["y_axis"]), "recordCount": counts["y_axis"]},
            "z_axis": {"occupiedCells": occupied_cells_for_orientation("z_axis"), "recordBytes": len(table_blobs["z_axis"]), "recordCount": counts["z_axis"]},
        },
        "memoryLayout": {
            "loadAddress": hex(LOAD_ADDR),
            "sysAddress": hex(SYS_ADDR),
            "screenAddress": hex(SCREEN_ADDR),
            "bitmapAddress": hex(BITMAP_ADDR),
            "endAddress": hex(END_ADDR),
            "recordTableAddresses": {k: hex(v) for k, v in table_addrs.items()},
            "machineCodeBytes": len(code),
            "programBytesBeforeImagePad": len(program) + 2,
        },
        "prgBytes": len(image),
        "runtimeKeyboard": True,
        "runtimeLineDrawing": False,
        "previewOnly": True,
    }
    OUT_META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_PRG}")
    print(f"Wrote {OUT_META}")
    print(json.dumps({
        "controls": meta["controls"],
        "orientations": meta["orientations"],
        "memoryLayout": meta["memoryLayout"],
        "prgBytes": meta["prgBytes"],
    }, indent=2))

if __name__ == "__main__":
    main()
