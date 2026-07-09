#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"
BASE_BUILDER = LAB / "tools" / "build_p02_domino_top_endpoint_preview_prg.py"
OUT_PRG = LAB / "dist" / "p03_elbow_wasd_3x3x10_pit_solid_active_preview.prg"
OUT_META = LAB / "dist" / "p03_elbow_wasd_3x3x10_pit_solid_active_preview_metadata.json"

LOAD_ADDR = 0x0801
SYS_ADDR = 0x080D
SCREEN_ADDR = 0x4400
BITMAP_ADDR = 0x6000
END_ADDR = 0x8000

# Zero-page workspace.
ORIENT = 0x02
PTR_LO = 0xFB
PTR_HI = 0xFC
CNT = 0xFD
PIT_CNT_HI = 0x15  # high byte for static pit-record count only; do not overlap ORIENT
TMP = 0xFE
MASK_ZP = 0x03
X0 = 0x04
Y0 = 0x05
X1 = 0x06
Y1 = 0x07
DX = 0x08
DY = 0x09
SX = 0x0A
SY = 0x0B
ACC = 0x0C
MAJOR = 0x0D
MINOR = 0x0E
LOOP = 0x0F
XCUR = 0x10
YCUR = 0x11
PLOT_WHITE = 0x12
PLOT_PTR_LO = 0x13
PLOT_PTR_HI = 0x14
XPOS = 0x16
YPOS = 0x17
BOX_R0 = 0x18
BOX_R1 = 0x19
BOX_C0 = 0x1A
BOX_C1 = 0x1B
ROW_CUR = 0x1C
COL_CUR = 0x1D


def bitmap_offset(x: int, y: int) -> int:
    return (y // 8) * 320 + (x // 8) * 8 + (y % 8)

def screen_cell(x: int, y: int) -> int:
    return (y // 8) * 40 + (x // 8)

def load_report():
    if not REPORT.exists():
        raise RuntimeError(f"Missing endpoint report: {REPORT}")
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("pieceId") != "P03_ELBOW":
        raise RuntimeError("endpoint report must be for P03_ELBOW")
    if report.get("summary", {}).get("classification") not in {"PATCH", "WATCH"}:
        raise RuntimeError("endpoint report must be PATCH/WATCH to build preview")
    return report

def load_base_projection():
    spec = importlib.util.spec_from_file_location("blockout_green_line_pit_projection", BASE_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base projection builder: {BASE_BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def pit_dot_records() -> dict[int, int]:
    # Green dotted pit renderer, using the same WASD 3x3x10 projection contract
    # as the active P03 endpoint payload. Dots are intentionally sparse to reduce
    # C64 hi-res 8x8 color-cell collisions with the white active piece.
    PIT_W = 3
    PIT_H = 3
    PIT_VISUAL_DEPTH = 10
    DOTS_PER_CELL_EDGE = 4
    DEPTH_T_BY_Z = [0.00, 0.34, 0.56, 0.71, 0.81, 0.88, 0.93, 0.96, 0.98, 0.99, 1.00]
    VISIBLE_RING_ZS = [0, 1, 2, 3, 4, 5, 6, 8, 10]

    def project(x: float, y: float, z: float) -> tuple[int, int]:
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
        return round(left + x * width / PIT_W), round(top + y * height / PIT_H)

    bitmap = bytearray(8000)

    def put_dot(px: int, py: int) -> None:
        if 0 <= px <= 319 and 0 <= py <= 199:
            off = bitmap_offset(px, py)
            bitmap[off] |= (1 << (7 - (px % 8)))

    def add_edge_dots(a: tuple[float, float, float], b: tuple[float, float, float]) -> None:
        ax, ay, az = a
        bx, by, bz = b
        for i in range(1, DOTS_PER_CELL_EDGE + 1):
            t = i / (DOTS_PER_CELL_EDGE + 1)
            px, py = project(ax + (bx - ax) * t, ay + (by - ay) * t, az + (bz - az) * t)
            put_dot(px, py)

    for z in VISIBLE_RING_ZS:
        for x in range(PIT_W):
            add_edge_dots((x, 0, z), (x + 1, 0, z))
            add_edge_dots((x, PIT_H, z), (x + 1, PIT_H, z))
        for y in range(PIT_H):
            add_edge_dots((0, y, z), (0, y + 1, z))
            add_edge_dots((PIT_W, y, z), (PIT_W, y + 1, z))

    for z in range(PIT_VISUAL_DEPTH):
        for x in range(PIT_W + 1):
            add_edge_dots((x, 0, z), (x, 0, z + 1))
            add_edge_dots((x, PIT_H, z), (x, PIT_H, z + 1))
        for y in range(PIT_H + 1):
            add_edge_dots((0, y, z), (0, y, z + 1))
            add_edge_dots((PIT_W, y, z), (PIT_W, y, z + 1))

    records: dict[int, int] = {}
    for off, value in enumerate(bitmap):
        if value:
            records[BITMAP_ADDR + off] = value
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
        self.bytes.extend(v & 0xFF for v in vals)

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
                out[pos] = target & 0xFF
                out[pos + 1] = (target >> 8) & 0xFF
            else:
                branch_from = self.addr + pos + 1
                delta = target - branch_from
                if not -128 <= delta <= 127:
                    raise RuntimeError(f"branch to {label} out of range: {delta}")
                out[pos] = delta & 0xFF
        return bytes(out)

def build_code(symbols: dict[str, int], orientation_count: int, pit_record_count: int) -> bytes:
    a = Asm(SYS_ADDR)

    def lda_imm(v): a.emit(0xA9, v)
    def ldx_imm(v): a.emit(0xA2, v)
    def ldy_imm(v): a.emit(0xA0, v)
    def lda_zp(z): a.emit(0xA5, z)
    def sta_zp(z): a.emit(0x85, z)
    def cmp_imm(v): a.emit(0xC9, v)
    def and_imm(v): a.emit(0x29, v)
    def ora_imm(v): a.emit(0x09, v)
    def sta_abs(addr): a.emit(0x8D, addr & 0xFF, (addr >> 8) & 0xFF)
    def lda_abs(addr): a.emit(0xAD, addr & 0xFF, (addr >> 8) & 0xFF)
    def beq(label): a.emit(0xF0); a.rel_patch(label)
    def bne(label): a.emit(0xD0); a.rel_patch(label)
    def bcc(label): a.emit(0x90); a.rel_patch(label)
    def bcs(label): a.emit(0xB0); a.rel_patch(label)
    def bpl(label): a.emit(0x10); a.rel_patch(label)
    def dec_zp(zp): a.emit(0xC6, zp)  # DEC zp
    def inc_zp(zp): a.emit(0xE6, zp)  # INC zp
    def jsr(label): a.emit(0x20); a.abs_patch(label)
    def jmp(label): a.emit(0x4C); a.abs_patch(label)

    # Init VIC: bank $4000, screen $4400, bitmap $6000, hi-res bitmap.
    lda_abs(0xDD00); and_imm(0xFC); ora_imm(0x02); sta_abs(0xDD00)
    lda_imm(0x00); sta_abs(0xD020); sta_abs(0xD021)
    lda_imm(0x3B); sta_abs(0xD011)
    lda_imm(0x08); sta_abs(0xD016)
    lda_imm(0x18); sta_abs(0xD018)
    lda_imm(0); sta_zp(ORIENT); sta_zp(XPOS); sta_zp(YPOS)
    jsr("draw_frame")

    a.label("main")
    a.emit(0x20, 0xE4, 0xFF)  # GETIN
    cmp_imm(0); bne("input_nonzero")
    jmp("main")
    a.label("input_nonzero")
    cmp_imm(ord("A")); beq("key_a")
    cmp_imm(ord("Q")); beq("key_q")
    cmp_imm(ord("S")); beq("key_s")
    cmp_imm(ord("W")); beq("key_w")
    cmp_imm(ord("D")); beq("key_d")
    cmp_imm(ord("E")); beq("key_e")
    # Cursor keys use absolute JMP trampolines so 6502 relative branches stay in range.
    cmp_imm(0x9D); bne("not_cursor_left"); jmp("key_left")
    a.label("not_cursor_left")
    cmp_imm(0x1D); bne("not_cursor_right"); jmp("key_right")
    a.label("not_cursor_right")
    cmp_imm(0x91); bne("not_cursor_up"); jmp("key_up")
    a.label("not_cursor_up")
    cmp_imm(0x11); bne("not_cursor_down"); jmp("key_down")
    a.label("not_cursor_down")
    jmp("main")

    def key_handler(label: str, table_name: str) -> None:
        a.label(label)
        ldx_imm(0)
        lda_zp(ORIENT)
        a.emit(0xAA)  # TAX
        a.emit(0xBD, symbols[table_name] & 0xFF, (symbols[table_name] >> 8) & 0xFF)
        sta_zp(ORIENT)
        jsr("draw_frame")
        jmp("main")

    for label, table in [
        ("key_a", "trans_A"), ("key_q", "trans_Q"),
        ("key_s", "trans_S"), ("key_w", "trans_W"),
        ("key_d", "trans_D"), ("key_e", "trans_E"),
    ]:
        key_handler(label, table)

    def move_handler(label: str, zp: int, direction: int) -> None:
        a.label(label)
        lda_zp(zp)
        if direction < 0:
            bne(f"{label}_can_dec")
            jmp("main")
            a.label(f"{label}_can_dec")
            dec_zp(zp)
        else:
            cmp_imm(2)
            bne(f"{label}_can_inc")
            jmp("main")
            a.label(f"{label}_can_inc")
            inc_zp(zp)
        jsr("draw_frame")
        jmp("main")

    move_handler("key_left", XPOS, -1)
    move_handler("key_right", XPOS, 1)
    move_handler("key_up", YPOS, -1)
    move_handler("key_down", YPOS, 1)

    a.label("draw_frame")
    jsr("clear_bitmap")
    jsr("fill_screen_green")
    jsr("draw_pit_records")
    jsr("load_active_box_payload")
    jsr("draw_active_boxes")
    a.emit(0x60)

    a.label("load_active_box_payload")
    # poseIndex = orientation*9 + y*3 + x
    lda_zp(ORIENT)
    a.emit(0x0A); a.emit(0x0A); a.emit(0x0A)
    a.emit(0x18); a.emit(0x65, ORIENT)
    sta_zp(TMP)
    lda_zp(YPOS)
    a.emit(0x0A)
    a.emit(0x18); a.emit(0x65, YPOS)
    a.emit(0x18); a.emit(0x65, TMP)
    a.emit(0x18); a.emit(0x65, XPOS)
    a.emit(0xAA)  # TAX
    a.emit(0xBD, symbols["active_box_lo"] & 0xFF, (symbols["active_box_lo"] >> 8) & 0xFF); sta_zp(PTR_LO)
    a.emit(0xBD, symbols["active_box_hi"] & 0xFF, (symbols["active_box_hi"] >> 8) & 0xFF); sta_zp(PTR_HI)
    ldy_imm(0)
    a.emit(0xB1, PTR_LO); sta_zp(CNT)
    lda_zp(PTR_LO); a.emit(0x18); a.emit(0x69, 0x01); sta_zp(PTR_LO)
    bcc("load_active_box_no_carry")
    a.emit(0xE6, PTR_HI)
    a.label("load_active_box_no_carry")
    a.emit(0x60)

    # Draw compact active boxes: count, then row0,row1,col0,col1 for each placed cube.
    # Each 8x8 hi-res cell in the box is filled with $FF and its screen color cell is white.
    a.label("draw_active_boxes")
    lda_zp(CNT); beq("active_boxes_done")
    a.label("active_box_loop")
    ldy_imm(0)
    a.emit(0xB1, PTR_LO); sta_zp(BOX_R0); a.emit(0xC8)
    a.emit(0xB1, PTR_LO); sta_zp(BOX_R1); a.emit(0xC8)
    a.emit(0xB1, PTR_LO); sta_zp(BOX_C0); a.emit(0xC8)
    a.emit(0xB1, PTR_LO); sta_zp(BOX_C1)
    lda_zp(PTR_LO); a.emit(0x18); a.emit(0x69, 0x04); sta_zp(PTR_LO)
    bcc("active_box_ptr_no_carry")
    a.emit(0xE6, PTR_HI)
    a.label("active_box_ptr_no_carry")

    lda_zp(BOX_R0); sta_zp(ROW_CUR)
    a.label("active_row_loop")
    lda_zp(BOX_C0); sta_zp(COL_CUR)
    a.label("active_col_loop")
    jsr("fill_active_cell")
    lda_zp(COL_CUR); a.emit(0xC5, BOX_C1)  # CMP BOX_C1
    beq("active_col_done")
    a.emit(0xE6, COL_CUR)
    jmp("active_col_loop")
    a.label("active_col_done")
    lda_zp(ROW_CUR); a.emit(0xC5, BOX_R1)  # CMP BOX_R1
    beq("active_one_box_done")
    a.emit(0xE6, ROW_CUR)
    jmp("active_row_loop")

    a.label("active_one_box_done")
    a.emit(0xC6, CNT)
    bne("active_box_loop")
    a.label("active_boxes_done")
    a.emit(0x60)

    a.label("fill_active_cell")
    lda_zp(ROW_CUR); a.emit(0xAA)
    a.emit(0xBD, symbols["bitmapcellrow_lo"] & 0xFF, (symbols["bitmapcellrow_lo"] >> 8) & 0xFF); sta_zp(PLOT_PTR_LO)
    a.emit(0xBD, symbols["bitmapcellrow_hi"] & 0xFF, (symbols["bitmapcellrow_hi"] >> 8) & 0xFF); sta_zp(PLOT_PTR_HI)
    lda_zp(COL_CUR); a.emit(0xAA)
    lda_zp(PLOT_PTR_LO); a.emit(0x18); a.emit(0x7D, symbols["col8_lo"] & 0xFF, (symbols["col8_lo"] >> 8) & 0xFF); sta_zp(PLOT_PTR_LO)
    lda_zp(PLOT_PTR_HI); a.emit(0x7D, symbols["col8_hi"] & 0xFF, (symbols["col8_hi"] >> 8) & 0xFF); sta_zp(PLOT_PTR_HI)

    # Build an 8-bit fill mask for a white cell with black left/right wireframe cuts.
    lda_imm(0xFF); sta_zp(MASK_ZP)
    lda_zp(COL_CUR); a.emit(0xC5, BOX_C0); bne("active_not_left_edge")
    lda_zp(MASK_ZP); a.emit(0x29, 0x7F); sta_zp(MASK_ZP)
    a.label("active_not_left_edge")
    lda_zp(COL_CUR); a.emit(0xC5, BOX_C1); bne("active_not_right_edge")
    lda_zp(MASK_ZP); a.emit(0x29, 0xFE); sta_zp(MASK_ZP)
    a.label("active_not_right_edge")

    # Top and bottom box rows are black-cut for a coarse wireframe around each active cube box.
    lda_zp(ROW_CUR); a.emit(0xC5, BOX_R0); bne("active_row0_not_top")
    lda_imm(0x00); jmp("active_store_byte0")
    a.label("active_row0_not_top")
    lda_zp(MASK_ZP)
    a.label("active_store_byte0")
    ldy_imm(0); a.emit(0x91, PLOT_PTR_LO)

    for byte_index in range(1, 7):
        lda_zp(MASK_ZP)
        ldy_imm(byte_index)
        a.emit(0x91, PLOT_PTR_LO)

    lda_zp(ROW_CUR); a.emit(0xC5, BOX_R1); bne("active_row7_not_bottom")
    lda_imm(0x00); jmp("active_store_byte7")
    a.label("active_row7_not_bottom")
    lda_zp(MASK_ZP)
    a.label("active_store_byte7")
    ldy_imm(7); a.emit(0x91, PLOT_PTR_LO)

    lda_zp(ROW_CUR); a.emit(0xAA)
    a.emit(0xBD, symbols["screencellrow_lo"] & 0xFF, (symbols["screencellrow_lo"] >> 8) & 0xFF); sta_zp(PLOT_PTR_LO)
    a.emit(0xBD, symbols["screencellrow_hi"] & 0xFF, (symbols["screencellrow_hi"] >> 8) & 0xFF); sta_zp(PLOT_PTR_HI)
    lda_zp(PLOT_PTR_LO); a.emit(0x18); a.emit(0x65, COL_CUR); sta_zp(PLOT_PTR_LO)
    bcc("fill_active_screen_no_carry")
    a.emit(0xE6, PLOT_PTR_HI)
    a.label("fill_active_screen_no_carry")
    lda_imm(0x10)
    ldy_imm(0)
    a.emit(0x91, PLOT_PTR_LO)
    a.emit(0x60)

    a.label("load_orientation_payload")
    # poseIndex = orientation*9 + y*3 + x
    lda_zp(ORIENT)
    a.emit(0x0A); a.emit(0x0A); a.emit(0x0A)  # A = orientation*8
    a.emit(0x18); a.emit(0x65, ORIENT)        # A = orientation*9
    sta_zp(TMP)
    lda_zp(YPOS)
    a.emit(0x0A)                              # A = y*2
    a.emit(0x18); a.emit(0x65, YPOS)          # A = y*3
    a.emit(0x18); a.emit(0x65, TMP)
    a.emit(0x18); a.emit(0x65, XPOS)
    a.emit(0xAA)  # TAX
    a.emit(0xBD, symbols["payload_lo"] & 0xFF, (symbols["payload_lo"] >> 8) & 0xFF); sta_zp(PTR_LO)
    a.emit(0xBD, symbols["payload_hi"] & 0xFF, (symbols["payload_hi"] >> 8) & 0xFF); sta_zp(PTR_HI)
    ldy_imm(0)
    a.emit(0xB1, PTR_LO); sta_zp(CNT)  # first byte is line count
    lda_zp(PTR_LO); a.emit(0x18); a.emit(0x69, 0x01); sta_zp(PTR_LO)
    bcc("load_payload_no_carry")
    a.emit(0xE6, PTR_HI)
    a.label("load_payload_no_carry")
    a.emit(0x60)

    # Draw endpoint records: x0,y0,x1,y1
    a.label("draw_endpoint_lines")
    lda_zp(CNT); beq("endpoint_done")
    a.label("endpoint_loop")
    ldy_imm(0)
    a.emit(0xB1, PTR_LO); sta_zp(X0); a.emit(0xC8)
    a.emit(0xB1, PTR_LO); sta_zp(Y0); a.emit(0xC8)
    a.emit(0xB1, PTR_LO); sta_zp(X1); a.emit(0xC8)
    a.emit(0xB1, PTR_LO); sta_zp(Y1)
    # ptr += 4
    lda_zp(PTR_LO); a.emit(0x18); a.emit(0x69, 0x04); sta_zp(PTR_LO)
    bcc("endpoint_ptr_no_carry")
    a.emit(0xE6, PTR_HI)
    a.label("endpoint_ptr_no_carry")
    jsr("draw_line")
    a.emit(0xC6, CNT)
    bne("endpoint_loop")
    a.label("endpoint_done")
    a.emit(0x60)

    # Draw precomputed pit bitmap OR records, green by screen default.
    a.label("draw_pit_records")
    lda_imm(symbols["pit_records"] & 0xFF); sta_zp(PTR_LO)
    lda_imm((symbols["pit_records"] >> 8) & 0xFF); sta_zp(PTR_HI)
    lda_imm(pit_record_count & 0xFF); sta_zp(CNT)
    lda_imm((pit_record_count >> 8) & 0xFF); sta_zp(PIT_CNT_HI)
    lda_imm(0); sta_zp(PLOT_WHITE)
    a.label("pit_loop")
    lda_zp(CNT); a.emit(0x05, PIT_CNT_HI); beq("pit_done")
    ldy_imm(0)
    a.emit(0xB1, PTR_LO); sta_abs(0x0330); sta_abs(0x0333); a.emit(0xC8)
    a.emit(0xB1, PTR_LO); sta_abs(0x0331); sta_abs(0x0334); a.emit(0xC8)
    a.emit(0xB1, PTR_LO); sta_zp(MASK_ZP)
    a.emit(0xAD); a.label("pit_lda_lo"); a.emit(0); a.label("pit_lda_hi"); a.emit(0)
    a.emit(0x05, MASK_ZP)
    a.emit(0x8D); a.label("pit_sta_lo"); a.emit(0); a.label("pit_sta_hi"); a.emit(0)
    lda_zp(PTR_LO); a.emit(0x18); a.emit(0x69, 0x03); sta_zp(PTR_LO)
    bcc("pit_ptr_no_carry")
    a.emit(0xE6, PTR_HI)
    a.label("pit_ptr_no_carry")
    # Decrement 16-bit pit-record counter.
    lda_zp(CNT); bne("pit_dec_low")
    a.emit(0xC6, PIT_CNT_HI)
    a.label("pit_dec_low")
    a.emit(0xC6, CNT)
    lda_zp(CNT); a.emit(0x05, PIT_CNT_HI); bne("pit_loop")
    a.label("pit_done")
    a.emit(0x60)

    # Simple unsigned accumulator line drawer.
    a.label("draw_line")
    lda_zp(X0); sta_zp(XCUR)
    lda_zp(Y0); sta_zp(YCUR)
    # dx/sx
    lda_zp(X1); a.emit(0x38); a.emit(0xE5, X0)  # SBC X0
    bcs("dx_positive")
    lda_zp(X0); a.emit(0x38); a.emit(0xE5, X1); sta_zp(DX)
    lda_imm(0xFF); sta_zp(SX)
    jmp("dy_calc")
    a.label("dx_positive")
    sta_zp(DX)
    lda_imm(0x01); sta_zp(SX)
    # dy/sy
    a.label("dy_calc")
    lda_zp(Y1); a.emit(0x38); a.emit(0xE5, Y0)
    bcs("dy_positive")
    lda_zp(Y0); a.emit(0x38); a.emit(0xE5, Y1); sta_zp(DY)
    lda_imm(0xFF); sta_zp(SY)
    jmp("choose_major")
    a.label("dy_positive")
    sta_zp(DY)
    lda_imm(0x01); sta_zp(SY)

    a.label("choose_major")
    lda_zp(DX); a.emit(0xC5, DY)  # CMP DY
    bcc("y_major")

    # X major.
    lda_zp(DX); sta_zp(MAJOR); sta_zp(LOOP)
    a.emit(0xE6, LOOP)  # loop = major + 1
    lda_zp(DY); sta_zp(MINOR)
    lda_imm(0); sta_zp(ACC)
    a.label("x_loop")
    jsr("plot_pixel")
    a.emit(0xC6, LOOP); beq("line_done")
    lda_zp(SX); cmp_imm(0x01); bne("x_dec")
    a.emit(0xE6, XCUR); jmp("x_after_step")
    a.label("x_dec")
    a.emit(0xC6, XCUR)
    a.label("x_after_step")
    lda_zp(ACC); a.emit(0x18); a.emit(0x65, MINOR); sta_zp(ACC)
    lda_zp(ACC); a.emit(0xC5, MAJOR); bcc("x_loop")
    lda_zp(ACC); a.emit(0x38); a.emit(0xE5, MAJOR); sta_zp(ACC)
    lda_zp(SY); cmp_imm(0x01); bne("x_y_dec")
    a.emit(0xE6, YCUR); jmp("x_loop")
    a.label("x_y_dec")
    a.emit(0xC6, YCUR); jmp("x_loop")

    # Y major.
    a.label("y_major")
    lda_zp(DY); sta_zp(MAJOR); sta_zp(LOOP)
    a.emit(0xE6, LOOP)
    lda_zp(DX); sta_zp(MINOR)
    lda_imm(0); sta_zp(ACC)
    a.label("y_loop")
    jsr("plot_pixel")
    a.emit(0xC6, LOOP); beq("line_done")
    lda_zp(SY); cmp_imm(0x01); bne("y_dec")
    a.emit(0xE6, YCUR); jmp("y_after_step")
    a.label("y_dec")
    a.emit(0xC6, YCUR)
    a.label("y_after_step")
    lda_zp(ACC); a.emit(0x18); a.emit(0x65, MINOR); sta_zp(ACC)
    lda_zp(ACC); a.emit(0xC5, MAJOR); bcc("y_loop")
    lda_zp(ACC); a.emit(0x38); a.emit(0xE5, MAJOR); sta_zp(ACC)
    lda_zp(SX); cmp_imm(0x01); bne("y_x_dec")
    a.emit(0xE6, XCUR); jmp("y_loop")
    a.label("y_x_dec")
    a.emit(0xC6, XCUR); jmp("y_loop")

    a.label("line_done")
    a.emit(0x60)

    # Plot current XCUR/YCUR into bitmap. Also set touched screen cell white for active block.
    a.label("plot_pixel")
    # Compute address = yrow[YCUR] + xoffset[XCUR].
    ldx_imm(0)
    lda_zp(YCUR); a.emit(0xAA)
    a.emit(0xBD, symbols["yrow_lo"] & 0xFF, (symbols["yrow_lo"] >> 8) & 0xFF); sta_zp(PLOT_PTR_LO)
    a.emit(0xBD, symbols["yrow_hi"] & 0xFF, (symbols["yrow_hi"] >> 8) & 0xFF); sta_zp(PLOT_PTR_HI)
    lda_zp(XCUR); a.emit(0xAA)
    lda_zp(PLOT_PTR_LO); a.emit(0x18); a.emit(0x7D, symbols["xoff_lo"] & 0xFF, (symbols["xoff_lo"] >> 8) & 0xFF); sta_zp(PLOT_PTR_LO)
    lda_zp(PLOT_PTR_HI); a.emit(0x7D, symbols["xoff_hi"] & 0xFF, (symbols["xoff_hi"] >> 8) & 0xFF); sta_zp(PLOT_PTR_HI)
    a.emit(0xBD, symbols["xmask"] & 0xFF, (symbols["xmask"] >> 8) & 0xFF); sta_zp(MASK_ZP)
    ldy_imm(0)
    a.emit(0xB1, PLOT_PTR_LO)
    a.emit(0x05, MASK_ZP)
    a.emit(0x91, PLOT_PTR_LO)

    # If active line mode, set screen color cell to white.
    lda_zp(PLOT_WHITE); beq("plot_done")
    lda_zp(YCUR); a.emit(0xAA)
    a.emit(0xBD, symbols["screenrow_lo"] & 0xFF, (symbols["screenrow_lo"] >> 8) & 0xFF); sta_zp(PLOT_PTR_LO)
    a.emit(0xBD, symbols["screenrow_hi"] & 0xFF, (symbols["screenrow_hi"] >> 8) & 0xFF); sta_zp(PLOT_PTR_HI)
    lda_zp(XCUR); a.emit(0xAA)
    lda_zp(PLOT_PTR_LO); a.emit(0x18); a.emit(0x7D, symbols["xcell"] & 0xFF, (symbols["xcell"] >> 8) & 0xFF); sta_zp(PLOT_PTR_LO)
    bcc("screen_no_carry")
    a.emit(0xE6, PLOT_PTR_HI)
    a.label("screen_no_carry")
    lda_imm(0x10)
    ldy_imm(0)
    a.emit(0x91, PLOT_PTR_LO)
    a.label("plot_done")
    a.emit(0x60)

    a.label("fill_screen_green")
    lda_imm(0x50); ldx_imm(0)
    a.label("fill_loop")
    for base in [SCREEN_ADDR, SCREEN_ADDR + 0x100, SCREEN_ADDR + 0x200]:
        a.emit(0x9D, base & 0xFF, (base >> 8) & 0xFF)
    a.emit(0xE0, 0xE8); beq("fill_skip_tail")
    a.emit(0x9D, (SCREEN_ADDR + 0x2E8) & 0xFF, ((SCREEN_ADDR + 0x2E8) >> 8) & 0xFF)
    a.label("fill_skip_tail")
    a.emit(0xE8); bne("fill_loop")
    a.emit(0x60)

    a.label("clear_bitmap")
    lda_imm(0); ldx_imm(0)
    a.label("clear_page_loop")
    for high in range(0x60, 0x7F):
        a.emit(0x9D, 0x00, high)
    a.emit(0xE8); bne("clear_page_loop")
    ldx_imm(0x3F)
    a.label("clear_tail_loop")
    a.emit(0x9D, 0x00, 0x7F)
    a.emit(0xCA); bpl("clear_tail_loop")
    a.emit(0x60)

    code = bytearray(a.resolve())
    # Patch self-modifying absolute addresses for pit record OR routine.
    for placeholder, label in [
        (0x0330, "pit_lda_lo"), (0x0331, "pit_lda_hi"),
        (0x0333, "pit_sta_lo"), (0x0334, "pit_sta_hi"),
    ]:
        target = a.labels[label]
        needle = bytes([placeholder & 0xFF, (placeholder >> 8) & 0xFF])
        idx = code.find(needle)
        if idx < 0:
            raise RuntimeError(f"Could not find placeholder {hex(placeholder)}")
        code[idx:idx+2] = bytes([target & 0xFF, (target >> 8) & 0xFF])
    return bytes(code)

def basic_stub() -> bytes:
    return bytes([0x0C, 0x08, 0x0A, 0x00, 0x9E, 0x32, 0x30, 0x36, 0x31, 0x00, 0x00, 0x00])

def make_payloads(report):
    # Prefer posePayloads when present: orientationId*9 + cursorY*3 + cursorX.
    items = report.get("posePayloads") or report["orientations"]
    payloads = []
    for item in items:
        segs = item["segments"]
        if len(segs) > 255:
            raise RuntimeError("line count too high for one-byte count")
        blob = bytearray([len(segs)])
        for seg in segs:
            for key in ["x1", "y1", "x2", "y2"]:
                v = int(seg[key])
                if not 0 <= v <= 255:
                    raise RuntimeError(f"endpoint out of 8-bit range: {v}")
                blob.append(v)
        payloads.append(bytes(blob))
    return payloads

def project_active_point(x: float, y: float, z: float) -> tuple[int, int]:
    # Same WASD_3x3x10 projection contract as the P03 report/pit.
    PIT_W = 3
    PIT_H = 3
    PIT_VISUAL_DEPTH = 10
    DEPTH_T_BY_Z = [0.00, 0.34, 0.56, 0.71, 0.81, 0.88, 0.93, 0.96, 0.98, 0.99, 1.00]
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
    return round(left + x * width / PIT_W), round(top + y * height / PIT_H)

def active_cell_box(x: int, y: int, z: int) -> tuple[int, int, int, int]:
    corners = [project_active_point(x + dx, y + dy, z + dz) for dx in (0, 1) for dy in (0, 1) for dz in (0, 1)]
    xs = [px for px, py in corners]
    ys = [py for px, py in corners]
    col0 = max(0, min(xs) // 8)
    col1 = min(39, max(xs) // 8)
    row0 = max(0, min(ys) // 8)
    row1 = min(24, max(ys) // 8)
    return row0, row1, col0, col1

def make_active_box_payloads(report):
    items = report.get("posePayloads") or report["orientations"]
    payloads = []
    for item in items:
        cells = item["placedCells"]
        if len(cells) > 255:
            raise RuntimeError("too many active cells for one-byte active box count")
        blob = bytearray([len(cells)])
        for x, y, z in cells:
            row0, row1, col0, col1 = active_cell_box(int(x), int(y), int(z))
            blob.extend([row0, row1, col0, col1])
        payloads.append(bytes(blob))
    return payloads

def make_transition_tables(report):
    transitions = report["transitions"]
    out = {}
    for key in ["A", "Q", "S", "W", "D", "E"]:
        out[key] = bytes([transitions[str(i)][key] for i in range(report["orientationCount"])])
    return out

def make_lookup_tables():
    ylo = bytearray()
    yhi = bytearray()
    for y in range(200):
        addr = BITMAP_ADDR + (y // 8) * 320 + (y % 8)
        ylo.append(addr & 0xFF)
        yhi.append((addr >> 8) & 0xFF)

    xoff_lo = bytearray()
    xoff_hi = bytearray()
    xmask = bytearray()
    xcell = bytearray()
    for x in range(256):
        off = (x // 8) * 8
        xoff_lo.append(off & 0xFF)
        xoff_hi.append((off >> 8) & 0xFF)
        xmask.append(1 << (7 - (x % 8)))
        xcell.append(x // 8)

    screenrow_lo = bytearray()
    screenrow_hi = bytearray()
    for y in range(200):
        addr = SCREEN_ADDR + (y // 8) * 40
        screenrow_lo.append(addr & 0xFF)
        screenrow_hi.append((addr >> 8) & 0xFF)

    bitmapcellrow_lo = bytearray()
    bitmapcellrow_hi = bytearray()
    screencellrow_lo = bytearray()
    screencellrow_hi = bytearray()
    for row in range(25):
        baddr = BITMAP_ADDR + row * 320
        saddr = SCREEN_ADDR + row * 40
        bitmapcellrow_lo.append(baddr & 0xFF)
        bitmapcellrow_hi.append((baddr >> 8) & 0xFF)
        screencellrow_lo.append(saddr & 0xFF)
        screencellrow_hi.append((saddr >> 8) & 0xFF)

    col8_lo = bytearray()
    col8_hi = bytearray()
    for col in range(40):
        off = col * 8
        col8_lo.append(off & 0xFF)
        col8_hi.append((off >> 8) & 0xFF)

    return {
        "yrow_lo": bytes(ylo), "yrow_hi": bytes(yhi),
        "xoff_lo": bytes(xoff_lo), "xoff_hi": bytes(xoff_hi),
        "xmask": bytes(xmask), "xcell": bytes(xcell),
        "screenrow_lo": bytes(screenrow_lo), "screenrow_hi": bytes(screenrow_hi),
        "bitmapcellrow_lo": bytes(bitmapcellrow_lo), "bitmapcellrow_hi": bytes(bitmapcellrow_hi),
        "screencellrow_lo": bytes(screencellrow_lo), "screencellrow_hi": bytes(screencellrow_hi),
        "col8_lo": bytes(col8_lo), "col8_hi": bytes(col8_hi),
    }

def layout_and_build(report, pit_records):
    payloads = make_payloads(report)
    active_box_payloads = make_active_box_payloads(report)
    transitions = make_transition_tables(report)
    lookups = make_lookup_tables()

    # Iterative two-pass layout: code size depends only on absolute addresses, not lengths.
    symbols = {name: 0x2000 for name in [
        "trans_A","trans_Q","trans_S","trans_W","trans_D","trans_E",
        "payload_lo","payload_hi","active_box_lo","active_box_hi","pit_records",
        "yrow_lo","yrow_hi","xoff_lo","xoff_hi","xmask","xcell","screenrow_lo","screenrow_hi",
        "bitmapcellrow_lo","bitmapcellrow_hi","screencellrow_lo","screencellrow_hi","col8_lo","col8_hi"
    ]}
    code0 = build_code(symbols, report["orientationCount"], len(pit_records))
    cursor = LOAD_ADDR + len(basic_stub()) + len(code0)
    pad = (16 - (cursor % 16)) % 16
    cursor += pad

    placed = {}
    for key in ["A", "Q", "S", "W", "D", "E"]:
        placed[f"trans_{key}"] = cursor
        cursor += len(transitions[key])

    placed["payload_lo"] = cursor
    cursor += len(payloads)
    placed["payload_hi"] = cursor
    cursor += len(payloads)

    payload_addrs = []
    for payload in payloads:
        payload_addrs.append(cursor)
        cursor += len(payload)

    active_box_addrs = []
    placed["active_box_lo"] = cursor
    cursor += len(active_box_payloads)
    placed["active_box_hi"] = cursor
    cursor += len(active_box_payloads)
    for active_box_payload in active_box_payloads:
        active_box_addrs.append(cursor)
        cursor += len(active_box_payload)

    placed["pit_records"] = cursor
    cursor += len(pit_records) * 3

    for name, blob in lookups.items():
        placed[name] = cursor
        cursor += len(blob)

    code = build_code(placed, report["orientationCount"], len(pit_records))

    program = bytearray()
    program.extend(basic_stub())
    program.extend(code)
    while (LOAD_ADDR + len(program)) % 16 != 0:
        program.append(0)

    actual = {}
    for key in ["A", "Q", "S", "W", "D", "E"]:
        actual[f"trans_{key}"] = LOAD_ADDR + len(program)
        program.extend(transitions[key])

    actual["payload_lo"] = LOAD_ADDR + len(program)
    program.extend(bytes([addr & 0xFF for addr in payload_addrs]))
    actual["payload_hi"] = LOAD_ADDR + len(program)
    program.extend(bytes([(addr >> 8) & 0xFF for addr in payload_addrs]))

    for payload in payloads:
        program.extend(payload)

    actual["active_box_lo"] = LOAD_ADDR + len(program)
    program.extend(bytes([addr & 0xFF for addr in active_box_addrs]))
    actual["active_box_hi"] = LOAD_ADDR + len(program)
    program.extend(bytes([(addr >> 8) & 0xFF for addr in active_box_addrs]))
    for active_box_payload in active_box_payloads:
        program.extend(active_box_payload)

    actual["pit_records"] = LOAD_ADDR + len(program)
    for addr, mask in sorted(pit_records.items()):
        program.extend([addr & 0xFF, (addr >> 8) & 0xFF, mask & 0xFF])

    for name, blob in lookups.items():
        actual[name] = LOAD_ADDR + len(program)
        program.extend(blob)

    # Check key symbol placements.
    for key, addr in placed.items():
        if key in actual and actual[key] != addr:
            raise RuntimeError(f"layout mismatch for {key}: {actual[key]} != {addr}")

    image_size = END_ADDR - LOAD_ADDR
    if len(program) + 2 > image_size:
        raise RuntimeError(f"program too large: {len(program)+2}")

    image = bytearray([0] * image_size)
    image[0:2] = bytes([LOAD_ADDR & 0xFF, LOAD_ADDR >> 8])
    image[2:2+len(program)] = program

    return bytes(image), {
        "codeBytes": len(code),
        "payloadBytes": sum(len(p) for p in payloads),
        "activeBoxPayloadBytes": sum(len(p) for p in active_box_payloads),
        "transitionBytes": sum(len(v) for v in transitions.values()),
        "pitRecordBytes": len(pit_records) * 3,
        "lookupTableBytes": sum(len(v) for v in lookups.values()),
        "programUsedBytes": len(program) + 2,
        "availablePrgImageBytes": image_size - 2,
    }

def main():
    report = load_report()
    pit_records = pit_dot_records()
    image, sizes = layout_and_build(report, pit_records)

    OUT_PRG.parent.mkdir(parents=True, exist_ok=True)
    OUT_PRG.write_bytes(image)

    meta = {
        "schemaVersion": 1,
        "program": str(OUT_PRG),
        "pieceId": "P03_ELBOW",
        "mode": "P03_ELBOW WASD 3x3x10 pit solid-active preview",
        "shortcutRemoved": True,
        "abovePit": True,
        "pitDimensions": {"widthCells": 3, "heightCells": 3, "depthCells": 10},
        "maxBlockFootprintWidth": 2,
        "axisControls": {"A": "+x", "Q": "-x", "S": "+y", "W": "-y", "D": "+z", "E": "-z"},
        "orientationCount": report["orientationCount"],
        "payloadSource": str(REPORT),
        "endpointPayloadClassification": report["summary"]["classification"],
        "estimatedEndpointPayloadBytes": report["summary"]["estimatedTotalEndpointPayloadBytes"],
        "runtimeLineDrawing": False,
        "activeSolidBoxes": True,
        "activeBoxWireframe": True,
        "activeBoxWireframeStrategy": "black 1-pixel cuts on top/bottom/left/right edges of each coarse 8x8 active box",
        "activeBoxPayloadBytes": sizes.get("activeBoxPayloadBytes"),
        "runtimeTruth": "C64 draws a green dotted WASD 3x3x10 pit, then key-driven P03_ELBOW solid active screen-cell boxes generated from placedCells.",
        "pitStyle": "green dotted WASD 3x3x10 pit, 4 dots per visible pit cell edge",
        "floorDots": False,
        "floorLines": False,
        "colorStrategy": "screen cells default green; active solid boxes fill bitmap cells and set their 8x8 cells white",
        "knownArtifact": "Solid active boxes are coarse 8x8-cell diagnostic fills with black wireframe cuts around each placed cube box; next step is face-accurate fills.",
        "sizes": sizes,
        "prgBytes": len(image),
        "runtimeKeyboard": True,
        "runtimeStatefulRotation": True,
        "previewOnly": True,
    }
    OUT_META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_PRG}")
    print(f"Wrote {OUT_META}")
    print(json.dumps({
        "pieceId": meta["pieceId"],
        "mode": meta["mode"],
        "orientationCount": meta["orientationCount"],
        "axisControls": meta["axisControls"],
        "runtimeLineDrawing": meta["runtimeLineDrawing"],
        "activeSolidBoxes": meta["activeSolidBoxes"],
        "activeBoxPayloadBytes": meta["activeBoxPayloadBytes"],
        "sizes": sizes,
        "prgBytes": meta["prgBytes"],
    }, indent=2))

if __name__ == "__main__":
    main()
