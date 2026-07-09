#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
BASE_BUILDER = LAB / "tools" / "build_p02_domino_top_endpoint_preview_prg.py"
OUT_PRG = LAB / "dist" / "p04_l_true_axis_above_pit_preview.prg"
OUT_META = LAB / "dist" / "p04_l_true_axis_above_pit_preview_metadata.json"

LOAD_ADDR = 0x0801
SYS_ADDR = 0x080D
SCREEN_ADDR = 0x4400
BITMAP_ADDR = 0x6000
END_ADDR = 0x8000

ORIENT_ADDR = 0x02
PTR_LO = 0xFB
PTR_HI = 0xFC
CNT_LO = 0xFD
CNT_HI = 0xFE
MASK_ZP = 0x03

# P04_L canonical shape.
CANONICAL = [(0,0,0), (1,0,0), (2,0,0), (0,1,0)]

# Keep the active block at the top/opening of the pit, not on the floor.
# In this lab projection, z=0 is the opening/top plane and larger z recedes into the pit.
ANCHOR = (1, 1, 0)

KEYS = {
    "A": ("x", 1),
    "Q": ("x", -1),
    "S": ("y", 1),
    "W": ("y", -1),
    "D": ("z", 1),
    "E": ("z", -1),
}

def load_base():
    spec = importlib.util.spec_from_file_location("blockout_true_axis_base", BASE_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base builder: {BASE_BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def bitmap_offset(x: int, y: int) -> int:
    return (y // 8) * 320 + (x // 8) * 8 + (y % 8)

def screen_cell(x: int, y: int) -> int:
    return (y // 8) * 40 + (x // 8)

def plot(record_map: dict[int, int], touched_cells: set[int], x: int, y: int) -> None:
    if not (0 <= x < 320 and 0 <= y < 200):
        return
    off = bitmap_offset(x, y)
    record_map[BITMAP_ADDR + off] = record_map.get(BITMAP_ADDR + off, 0) | (1 << (7 - (x % 8)))
    touched_cells.add(screen_cell(x, y))

def draw_dot(record_map: dict[int, int], touched_cells: set[int], x: int, y: int) -> None:
    # Single-pixel dot.
    plot(record_map, touched_cells, x, y)

def solid_line(base, record_map: dict[int, int], touched_cells: set[int], a: tuple[int, int], b: tuple[int, int]) -> None:
    for x, y in base.bresenham(a, b):
        plot(record_map, touched_cells, x, y)

def green_wall_dot_records(base) -> tuple[dict[int, int], set[int]]:
    records: dict[int, int] = {}
    touched: set[int] = set()

    # Single-pixel green wall/opening dots only. No floor/interior dots.
    visible_z = [0, 1, 2, 3, 4, 5, 6, 8, 10]
    for z in visible_z:
        for x in range(0, 6):
            for y in range(0, 6):
                if x in (0, 5) or y in (0, 5):
                    px, py = base.project_vertex((x, y, z))
                    draw_dot(records, touched, px, py)
    return records, touched

def normalize(cells: list[tuple[int, int, int]]) -> tuple[tuple[int, int, int], ...]:
    minx = min(x for x, _, _ in cells)
    miny = min(y for _, y, _ in cells)
    minz = min(z for _, _, z in cells)
    return tuple(sorted((x-minx, y-miny, z-minz) for x, y, z in cells))

def rotate_cell(cell: tuple[int, int, int], axis: str, direction: int) -> tuple[int, int, int]:
    x, y, z = cell
    if axis == "x":
        return (x, -z, y) if direction > 0 else (x, z, -y)
    if axis == "y":
        return (z, y, -x) if direction > 0 else (-z, y, x)
    if axis == "z":
        return (-y, x, z) if direction > 0 else (y, -x, z)
    raise ValueError(axis)

def rotate_shape(shape: tuple[tuple[int, int, int], ...], axis: str, direction: int) -> tuple[tuple[int, int, int], ...]:
    return normalize([rotate_cell(c, axis, direction) for c in shape])

def generate_orientations():
    start = normalize(CANONICAL)
    seen = {start}
    frontier = [start]
    while frontier:
        current = frontier.pop(0)
        for axis in ["x", "y", "z"]:
            for direction in [1, -1]:
                nxt = rotate_shape(current, axis, direction)
                if nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
    shapes = sorted(seen)
    id_by_shape = {shape: idx for idx, shape in enumerate(shapes)}
    transitions = {}
    for idx, shape in enumerate(shapes):
        transitions[idx] = {}
        for key, (axis, direction) in KEYS.items():
            transitions[idx][key] = id_by_shape[rotate_shape(shape, axis, direction)]
    return shapes, transitions

def place_shape(shape: tuple[tuple[int, int, int], ...]) -> list[tuple[int, int, int]]:
    ax, ay, az = ANCHOR
    # Center each normalized orientation near the pit opening.
    maxx = max(x for x, _, _ in shape)
    maxy = max(y for _, y, _ in shape)
    shift_x = ax
    shift_y = ay
    if maxx <= 1:
        shift_x = ax + 1
    if maxy <= 1:
        shift_y = ay + 1
    return sorted((x + shift_x, y + shift_y, z + az) for x, y, z in shape)

def segments_for_cells(base, cells):
    occupied = set(cells)
    face_defs = [
        ((-1,0,0), [(0,0,0),(0,1,0),(0,1,1),(0,0,1)]),
        ((1,0,0), [(1,0,0),(1,0,1),(1,1,1),(1,1,0)]),
        ((0,-1,0), [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
        ((0,1,0), [(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
        ((0,0,-1), [(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
        ((0,0,1), [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),
    ]
    edges=set()
    for x,y,z in cells:
        for (dx,dy,dz), corners in face_defs:
            if (x+dx, y+dy, z+dz) in occupied:
                continue
            verts=[(x+cx,y+cy,z+cz) for cx,cy,cz in corners]
            for i in range(4):
                edges.add(tuple(sorted([verts[i], verts[(i+1)%4]])))
    out=[]
    for a,b in sorted(edges):
        x1,y1=base.project_vertex(a)
        x2,y2=base.project_vertex(b)
        if (x1,y1)!=(x2,y2):
            out.append((x1,y1,x2,y2))
    return sorted(set(out))

def frame_records(base, placed_cells) -> tuple[dict[int, int], set[int], set[int]]:
    records, pit_cells = green_wall_dot_records(base)
    block_cells: set[int] = set()
    for x1,y1,x2,y2 in segments_for_cells(base, placed_cells):
        solid_line(base, records, block_cells, (x1,y1), (x2,y2))
    return records, pit_cells, block_cells

class Asm:
    def __init__(self, addr:int):
        self.addr=addr; self.bytes=bytearray(); self.labels={}; self.patches=[]
    @property
    def pc(self): return self.addr+len(self.bytes)
    def label(self,n): self.labels[n]=self.pc
    def emit(self,*vals): self.bytes.extend(v & 0xff for v in vals)
    def abs_patch(self,label): pos=len(self.bytes); self.emit(0,0); self.patches.append((pos,label,"abs"))
    def rel_patch(self,label): pos=len(self.bytes); self.emit(0); self.patches.append((pos,label,"rel"))
    def resolve(self):
        out=bytearray(self.bytes)
        for pos,label,kind in self.patches:
            target=self.labels[label]
            if kind=="abs":
                out[pos]=target&0xff; out[pos+1]=(target>>8)&0xff
            else:
                branch_from=self.addr+pos+1
                delta=target-branch_from
                if not -128 <= delta <= 127:
                    raise RuntimeError(f"branch to {label} out of range: {delta}")
                out[pos]=delta&0xff
        return bytes(out)

def build_code(bitmap_table_addrs, bitmap_counts, white_table_addrs, white_counts, transition_addr, orientation_count):
    a=Asm(SYS_ADDR)
    def lda_imm(v): a.emit(0xA9,v)
    def ldx_imm(v): a.emit(0xA2,v)
    def ldy_imm(v): a.emit(0xA0,v)
    def lda_zp(z): a.emit(0xA5,z)
    def sta_zp(z): a.emit(0x85,z)
    def sta_abs(addr): a.emit(0x8D,addr&0xff,(addr>>8)&0xff)
    def lda_abs(addr): a.emit(0xAD,addr&0xff,(addr>>8)&0xff)
    def cmp_imm(v): a.emit(0xC9,v)
    def and_imm(v): a.emit(0x29,v)
    def ora_imm(v): a.emit(0x09,v)
    def beq(label): a.emit(0xF0); a.rel_patch(label)
    def bne(label): a.emit(0xD0); a.rel_patch(label)
    def bpl(label): a.emit(0x10); a.rel_patch(label)
    def jsr(label): a.emit(0x20); a.abs_patch(label)
    def jmp(label): a.emit(0x4C); a.abs_patch(label)

    lda_abs(0xDD00); and_imm(0xFC); ora_imm(0x02); sta_abs(0xDD00)
    lda_imm(0x00); sta_abs(0xD020); sta_abs(0xD021)
    lda_imm(0x3B); sta_abs(0xD011)
    lda_imm(0x08); sta_abs(0xD016)
    lda_imm(0x18); sta_abs(0xD018)
    lda_imm(0); sta_zp(ORIENT_ADDR)
    jsr("draw_by_orientation")

    a.label("main")
    a.emit(0x20,0xE4,0xFF)
    cmp_imm(0); beq("main")
    cmp_imm(ord("A")); beq("key_a")
    cmp_imm(ord("Q")); beq("key_q")
    cmp_imm(ord("S")); beq("key_s")
    cmp_imm(ord("W")); beq("key_w")
    cmp_imm(ord("D")); beq("key_d")
    cmp_imm(ord("E")); beq("key_e")
    jmp("main")

    def key_handler(label, offset):
        a.label(label)
        lda_zp(ORIENT_ADDR)
        a.emit(0x0A) # *2
        a.emit(0x0A) # *4
        a.emit(0x18)
        a.emit(0x69, offset)
        a.emit(0xAA) # TAX
        a.emit(0xBD, transition_addr & 0xff, (transition_addr >> 8) & 0xff)
        sta_zp(ORIENT_ADDR)
        jsr("draw_by_orientation")
        jmp("main")

    # transition row layout: A,Q,S,W,D,E uses 6 bytes, but multiply-by-4 is not enough.
    # For compact/simple runtime, transition lookup below is replaced by six explicit tables.
    # This label body will be patched by using transition_addr as the first of six tables and X=orientation.
    a.bytes = a.bytes[:-0]  # no-op

    # Rebuild key handlers with table-per-key: table + orientation.
    # A=$transition_addr, Q=+N, S=+2N, W=+3N, D=+4N, E=+5N
    a.labels.pop("key_a", None)

    def key_table_handler(label, table_offset):
        a.label(label)
        ldx_imm(0)
        lda_zp(ORIENT_ADDR)
        a.emit(0xAA)
        a.emit(0xBD, (transition_addr + table_offset) & 0xff, ((transition_addr + table_offset) >> 8) & 0xff)
        sta_zp(ORIENT_ADDR)
        jsr("draw_by_orientation")
        jmp("main")

    key_table_handler("key_a", 0 * orientation_count)
    key_table_handler("key_q", 1 * orientation_count)
    key_table_handler("key_s", 2 * orientation_count)
    key_table_handler("key_w", 3 * orientation_count)
    key_table_handler("key_d", 4 * orientation_count)
    key_table_handler("key_e", 5 * orientation_count)

    a.label("draw_by_orientation")
    lda_zp(ORIENT_ADDR)
    # Long dispatch: 6502 branches are relative and can only reach about ±127 bytes.
    # Use BNE-over-JMP so each matching orientation can jump to a far draw routine.
    for i in range(orientation_count - 1):
        cmp_imm(i)
        bne(f"not_draw_{i}")
        jmp(f"draw_{i}")
        a.label(f"not_draw_{i}")
    jmp(f"draw_{orientation_count-1}")

    def draw_state(label,state):
        a.label(label)
        jsr("clear_bitmap")
        jsr("fill_screen_green")
        addr=white_table_addrs[state]
        lda_imm(addr&0xff); sta_zp(PTR_LO)
        lda_imm((addr>>8)&0xff); sta_zp(PTR_HI)
        count=white_counts[state]
        lda_imm(count&0xff); sta_zp(CNT_LO)
        lda_imm((count>>8)&0xff); sta_zp(CNT_HI)
        jsr("paint_white_cells")
        addr=bitmap_table_addrs[state]
        lda_imm(addr&0xff); sta_zp(PTR_LO)
        lda_imm((addr>>8)&0xff); sta_zp(PTR_HI)
        count=bitmap_counts[state]
        lda_imm(count&0xff); sta_zp(CNT_LO)
        lda_imm((count>>8)&0xff); sta_zp(CNT_HI)
        jsr("draw_bitmap_records")
        a.emit(0x60)
    for state in range(orientation_count):
        draw_state(f"draw_{state}", state)

    a.label("fill_screen_green")
    lda_imm(0x50); ldx_imm(0)
    a.label("fill_loop")
    for base in [SCREEN_ADDR, SCREEN_ADDR+0x100, SCREEN_ADDR+0x200]:
        a.emit(0x9D, base&0xff, (base>>8)&0xff)
    a.emit(0xE0,0xE8); beq("fill_skip_tail")
    a.emit(0x9D, (SCREEN_ADDR+0x2E8)&0xff, ((SCREEN_ADDR+0x2E8)>>8)&0xff)
    a.label("fill_skip_tail")
    a.emit(0xE8); bne("fill_loop"); a.emit(0x60)

    a.label("clear_bitmap")
    lda_imm(0); ldx_imm(0)
    a.label("clear_page_loop")
    for high in range(0x60,0x7F):
        a.emit(0x9D,0x00,high)
    a.emit(0xE8); bne("clear_page_loop")
    ldx_imm(0x3F)
    a.label("clear_tail_loop")
    a.emit(0x9D,0x00,0x7F); a.emit(0xCA); bpl("clear_tail_loop")
    a.emit(0x60)

    a.label("paint_white_cells")
    a.label("white_loop")
    lda_zp(CNT_LO); a.emit(0x05,CNT_HI); beq("white_done")
    ldy_imm(0)
    a.emit(0xB1,PTR_LO); sta_abs(0x0330)
    a.emit(0xC8)
    a.emit(0xB1,PTR_LO); sta_abs(0x0331)
    lda_imm(0x10)
    a.emit(0x8D); a.label("white_target_lo"); a.emit(0); a.label("white_target_hi"); a.emit(0)
    a.emit(0x18); lda_zp(PTR_LO); a.emit(0x69,0x02); sta_zp(PTR_LO); a.emit(0x90,0x02); a.emit(0xE6,PTR_HI)
    lda_zp(CNT_LO); a.emit(0xD0,0x02); a.emit(0xC6,CNT_HI); a.emit(0xC6,CNT_LO)
    jmp("white_loop")
    a.label("white_done"); a.emit(0x60)

    a.label("draw_bitmap_records")
    a.label("draw_loop")
    lda_zp(CNT_LO); a.emit(0x05,CNT_HI); beq("draw_done")
    ldy_imm(0)
    a.emit(0xB1,PTR_LO); sta_abs(0x0332); sta_abs(0x0335)
    a.emit(0xC8)
    a.emit(0xB1,PTR_LO); sta_abs(0x0333); sta_abs(0x0336)
    a.emit(0xC8)
    a.emit(0xB1,PTR_LO); sta_zp(MASK_ZP)
    a.emit(0xAD); a.label("target_lda_lo"); a.emit(0); a.label("target_lda_hi"); a.emit(0)
    a.emit(0x05,MASK_ZP)
    a.emit(0x8D); a.label("target_sta_lo"); a.emit(0); a.label("target_sta_hi"); a.emit(0)
    a.emit(0x18); lda_zp(PTR_LO); a.emit(0x69,0x03); sta_zp(PTR_LO); a.emit(0x90,0x02); a.emit(0xE6,PTR_HI)
    lda_zp(CNT_LO); a.emit(0xD0,0x02); a.emit(0xC6,CNT_HI); a.emit(0xC6,CNT_LO)
    jmp("draw_loop")
    a.label("draw_done"); a.emit(0x60)

    code=bytearray(a.resolve())
    replacements=[
        (0x0330,"white_target_lo"),(0x0331,"white_target_hi"),
        (0x0332,"target_lda_lo"),(0x0333,"target_lda_hi"),
        (0x0335,"target_sta_lo"),(0x0336,"target_sta_hi"),
    ]
    for placeholder,label in replacements:
        target=a.labels[label]
        needle=bytes([placeholder&0xff,(placeholder>>8)&0xff])
        idx=code.find(needle)
        if idx<0:
            raise RuntimeError(f"Could not find placeholder {hex(placeholder)}")
        code[idx:idx+2]=bytes([target&0xff,(target>>8)&0xff])
    return bytes(code)

def basic_stub():
    return bytes([0x0c,0x08,0x0a,0x00,0x9e,0x32,0x30,0x36,0x31,0x00,0x00,0x00])

def make_blobs(records_by_orientation, white_cells_by_orientation):
    bitmap_blobs={}
    white_blobs={}
    for state,recs in records_by_orientation.items():
        blob=bytearray()
        for addr,mask in sorted(recs.items()):
            blob.extend([addr&0xff,(addr>>8)&0xff,mask&0xff])
        bitmap_blobs[state]=bytes(blob)
    for state,cells in white_cells_by_orientation.items():
        blob=bytearray()
        for cell in sorted(cells):
            addr=SCREEN_ADDR+cell
            blob.extend([addr&0xff,(addr>>8)&0xff])
        white_blobs[state]=bytes(blob)
    return bitmap_blobs, white_blobs

def make_transition_blob(transitions, orientation_count):
    blob=bytearray()
    for key in ["A","Q","S","W","D","E"]:
        for idx in range(orientation_count):
            blob.append(transitions[idx][key])
    return bytes(blob)

def main():
    base=load_base()
    shapes, transitions = generate_orientations()
    orientation_count=len(shapes)

    records_by_orientation={}
    white_cells_by_orientation={}
    placed_by_orientation={}
    pit_cell_count=None

    for idx, shape in enumerate(shapes):
        placed=place_shape(shape)
        placed_by_orientation[idx]=placed
        records, pit_cells, block_cells=frame_records(base, placed)
        records_by_orientation[idx]=records
        white_cells_by_orientation[idx]=block_cells
        if pit_cell_count is None:
            pit_cell_count=len(pit_cells)

    bitmap_blobs, white_blobs = make_blobs(records_by_orientation, white_cells_by_orientation)
    bitmap_counts={i: len(bitmap_blobs[i])//3 for i in range(orientation_count)}
    white_counts={i: len(white_blobs[i])//2 for i in range(orientation_count)}
    transition_blob = make_transition_blob(transitions, orientation_count)

    dummy_bitmap={i:0x2000+i*0x100 for i in range(orientation_count)}
    dummy_white={i:0x3000+i*0x100 for i in range(orientation_count)}
    dummy_transition=0x5000
    code0=build_code(dummy_bitmap,bitmap_counts,dummy_white,white_counts,dummy_transition,orientation_count)

    base_len=len(basic_stub())+len(code0)
    pad=(16-((LOAD_ADDR+base_len)%16))%16
    cursor=LOAD_ADDR+base_len+pad
    bitmap_table_addrs={}
    white_table_addrs={}
    for idx in range(orientation_count):
        bitmap_table_addrs[idx]=cursor
        cursor += len(bitmap_blobs[idx])
        white_table_addrs[idx]=cursor
        cursor += len(white_blobs[idx])
    transition_addr=cursor
    cursor += len(transition_blob)

    code=build_code(bitmap_table_addrs,bitmap_counts,white_table_addrs,white_counts,transition_addr,orientation_count)

    program=bytearray()
    program.extend(basic_stub())
    program.extend(code)
    while (LOAD_ADDR+len(program))%16 != 0:
        program.append(0)

    actual_bitmap={}
    actual_white={}
    for idx in range(orientation_count):
        actual_bitmap[idx]=LOAD_ADDR+len(program)
        program.extend(bitmap_blobs[idx])
        actual_white[idx]=LOAD_ADDR+len(program)
        program.extend(white_blobs[idx])
    actual_transition=LOAD_ADDR+len(program)
    program.extend(transition_blob)

    if actual_bitmap != bitmap_table_addrs or actual_white != white_table_addrs or actual_transition != transition_addr:
        raise RuntimeError("table address mismatch")

    image_size=END_ADDR-LOAD_ADDR
    if len(program)+2 > image_size:
        raise RuntimeError(f"program too large: {len(program)+2}")

    image=bytearray([0]*image_size)
    image[0:2]=bytes([LOAD_ADDR&0xff,LOAD_ADDR>>8])
    image[2:2+len(program)]=program
    OUT_PRG.parent.mkdir(parents=True, exist_ok=True)
    OUT_PRG.write_bytes(bytes(image))

    meta={
        "schemaVersion":1,
        "program":str(OUT_PRG),
        "pieceId":"P04_L",
        "mode":"true axis rotation preview above pit",
        "shortcutRemoved":True,
        "abovePit":True,
        "anchor":ANCHOR,
        "axisControls":{"A":"+x","Q":"-x","S":"+y","W":"-y","D":"+z","E":"-z"},
        "orientationCount":orientation_count,
        "pitStyle":"single-pixel green wall/opening dots only; no floor dots",
        "floorDots":False,
        "colorStrategy":"screen cells default green; active-block touched cells are set to white",
        "knownArtifact":"Any green pit dot in an active-block touched 8x8 cell will still become white; sparse wall dots reduce collisions.",
        "runtimeTruth":"axis-specific orientation transition table generated upstream; C64 runtime does table lookup and draws prepared payload",
        "transitions":{str(k):v for k,v in transitions.items()},
        "orientations":{
            str(idx):{
                "normalizedCells":list(shapes[idx]),
                "placedCells":placed_by_orientation[idx],
                "bitmapRecordCount":bitmap_counts[idx],
                "whiteScreenCellCount":white_counts[idx],
            } for idx in range(orientation_count)
        },
        "pitTouchedCells":pit_cell_count,
        "transitionTableBytes":len(transition_blob),
        "prgBytes":len(image),
        "runtimeKeyboard":True,
        "runtimeStatefulRotation":True,
        "runtimeLineDrawing":False,
        "previewOnly":True,
    }
    OUT_META.write_text(json.dumps(meta, indent=2)+"\n", encoding="utf-8")
    print(f"Wrote {OUT_PRG}")
    print(f"Wrote {OUT_META}")
    print(json.dumps({
        "pieceId":meta["pieceId"],
        "mode":meta["mode"],
        "shortcutRemoved":meta["shortcutRemoved"],
        "abovePit":meta["abovePit"],
        "orientationCount":meta["orientationCount"],
        "axisControls":meta["axisControls"],
        "pitStyle":meta["pitStyle"],
        "floorDots":meta["floorDots"],
        "transitionTableBytes":meta["transitionTableBytes"],
        "prgBytes":meta["prgBytes"],
    }, indent=2))

if __name__ == "__main__":
    main()
