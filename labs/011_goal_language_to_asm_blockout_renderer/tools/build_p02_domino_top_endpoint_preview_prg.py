#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT = LAB / "dist" / "pieces" / "P02_DOMINO.endpoint_payload_report.json"
OUT_PRG = LAB / "dist" / "p02_domino_top_endpoint_preview.prg"
OUT_META = LAB / "dist" / "p02_domino_top_endpoint_preview_metadata.json"

LOAD_ADDR = 0x0801
SYS_ADDR = 0x080D
SCREEN_ADDR = 0x4400
BITMAP_ADDR = 0x6000
VIC_BANK = 1

PIT_WIDTH = 5
PIT_HEIGHT = 5
PIT_DEPTH = 10

VIEWPORT = {
    "near": {"left": 30, "top": 2, "right": 226, "bottom": 198},
    "far": {"left": 92, "top": 64, "right": 164, "bottom": 136},
    "depthT": {
        0: 0.00,
        1: 0.34,
        2: 0.56,
        3: 0.71,
        4: 0.81,
        5: 0.88,
        6: 0.93,
        7: 0.96,
        8: 0.98,
        9: 0.99,
        10: 1.00,
    },
}

VISIBLE_RINGS = [0, 1, 2, 3, 4, 5, 6, 8, 10]

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def project_vertex(v: tuple[int, int, int]) -> tuple[int, int]:
    x, y, z = v
    z = max(0, min(10, z))
    t = VIEWPORT["depthT"][z]
    near = VIEWPORT["near"]
    far = VIEWPORT["far"]
    left = lerp(near["left"], far["left"], t)
    top = lerp(near["top"], far["top"], t)
    right = lerp(near["right"], far["right"], t)
    bottom = lerp(near["bottom"], far["bottom"], t)
    return (
        int(round(left + (x / PIT_WIDTH) * (right - left))),
        int(round(top + (y / PIT_HEIGHT) * (bottom - top))),
    )

def bresenham(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:
    x0, y0 = a
    x1, y1 = b
    points = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        if 0 <= x0 < 320 and 0 <= y0 < 200:
            points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return points

def bitmap_offset(x: int, y: int) -> int:
    return (y // 8) * 320 + (x // 8) * 8 + (y % 8)

def draw_line(bitmap: bytearray, touched_cells: set[int], a: tuple[int, int], b: tuple[int, int]) -> None:
    for x, y in bresenham(a, b):
        off = bitmap_offset(x, y)
        bitmap[off] |= 1 << (7 - (x % 8))
        touched_cells.add((y // 8) * 40 + (x // 8))

def add_pit_segments() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    segments: list[tuple[tuple[int, int], tuple[int, int]]] = []

    def p(x: int, y: int, z: int) -> tuple[int, int]:
        return project_vertex((x, y, z))

    for z in VISIBLE_RINGS:
        corners = [p(0,0,z), p(5,0,z), p(5,5,z), p(0,5,z)]
        for i in range(4):
            segments.append((corners[i], corners[(i + 1) % 4]))

    for corner in [(0,0), (5,0), (5,5), (0,5)]:
        segments.append((p(corner[0], corner[1], 0), p(corner[0], corner[1], 10)))

    for k in range(1, 5):
        segments.append((p(k, 0, 0), p(k, 0, 10)))
        segments.append((p(k, 5, 0), p(k, 5, 10)))
        segments.append((p(0, k, 0), p(0, k, 10)))
        segments.append((p(5, k, 0), p(5, k, 10)))

    return segments

def basic_stub() -> bytes:
    # 10 SYS 2061
    return bytes([
        0x0c, 0x08,
        0x0a, 0x00,
        0x9e,
        0x32, 0x30, 0x36, 0x31,
        0x00,
        0x00, 0x00,
    ])

def machine_code() -> bytes:
    # starts at $080d
    code = []
    def lda_imm(v): code.extend([0xA9, v & 0xff])
    def sta_abs(addr): code.extend([0x8D, addr & 0xff, (addr >> 8) & 0xff])
    def lda_abs(addr): code.extend([0xAD, addr & 0xff, (addr >> 8) & 0xff])
    def and_imm(v): code.extend([0x29, v & 0xff])
    def ora_imm(v): code.extend([0x09, v & 0xff])
    def jmp_abs(addr): code.extend([0x4C, addr & 0xff, (addr >> 8) & 0xff])

    # VIC bank 1 ($4000-$7fff): CIA2 bank bits = %10.
    lda_abs(0xDD00)
    and_imm(0xFC)
    ora_imm(0x02)
    sta_abs(0xDD00)

    lda_imm(0x00); sta_abs(0xD020)  # border black
    lda_imm(0x00); sta_abs(0xD021)  # background black
    lda_imm(0x3B); sta_abs(0xD011)  # bitmap mode + display
    lda_imm(0x08); sta_abs(0xD016)  # standard hi-res
    lda_imm(0x18); sta_abs(0xD018)  # screen $4400, bitmap $6000 inside VIC bank 1

    loop_addr = SYS_ADDR + len(code)
    jmp_abs(loop_addr)
    return bytes(code)

def select_pose(report: dict) -> dict:
    target = {
        "rotationId": "x_axis",
        "x": 1,
        "y": 2,
        "z": 0,
    }
    for pose in report["poses"]:
        if all(pose.get(k) == v for k, v in target.items()):
            return pose
    raise ValueError(f"Could not find target pose: {target}")

def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    pose = select_pose(report)

    bitmap = bytearray(8000)
    screen = bytearray([0x50] * 1000)  # green foreground, black background.

    pit_cells: set[int] = set()
    for a, b in add_pit_segments():
        draw_line(bitmap, pit_cells, a, b)

    block_cells: set[int] = set()
    for x1, y1, x2, y2 in pose["projectedSegments"] if "projectedSegments" in pose else []:
        draw_line(bitmap, block_cells, (x1, y1), (x2, y2))

    # Older report stores counts, not segment lists. Reconstruct selected pose from local endpoint generator.
    if not block_cells:
        for x1, y1, x2, y2 in reconstruct_pose_segments(pose):
            draw_line(bitmap, block_cells, (x1, y1), (x2, y2))

    for cell in block_cells:
        if 0 <= cell < 1000:
            screen[cell] = 0x10  # white foreground, black background.

    image_size = 0x8000 - LOAD_ADDR
    image = bytearray([0x00] * image_size)
    image[0:2] = bytes([LOAD_ADDR & 0xff, LOAD_ADDR >> 8])

    def put(addr: int, data: bytes | bytearray) -> None:
        start = addr - LOAD_ADDR + 2
        image[start:start + len(data)] = data

    put(0x0801, basic_stub())
    put(SYS_ADDR, machine_code())
    put(SCREEN_ADDR, screen)
    put(BITMAP_ADDR, bitmap)

    OUT_PRG.parent.mkdir(parents=True, exist_ok=True)
    OUT_PRG.write_bytes(bytes(image))

    meta = {
        "schemaVersion": 1,
        "program": str(OUT_PRG),
        "mode": "P02_DOMINO top-level endpoint preview",
        "sourceReport": str(REPORT),
        "selectedPose": {
            "pieceId": pose["pieceId"],
            "rotationId": pose["rotationId"],
            "x": pose["x"],
            "y": pose["y"],
            "z": pose["z"],
            "occupiedCells": pose["occupiedCells"],
            "projectedLineSegmentCount": pose["projectedLineSegmentCount"],
        },
        "colors": {
            "pitForeground": "green",
            "activeBlockForeground": "white",
            "background": "black",
            "note": "C64 hi-res bitmap color is cell-based; active-block cells use white foreground."
        },
        "memoryLayout": {
            "loadAddress": hex(LOAD_ADDR),
            "sysAddress": hex(SYS_ADDR),
            "vicBank": VIC_BANK,
            "screenAddress": hex(SCREEN_ADDR),
            "bitmapAddress": hex(BITMAP_ADDR),
        },
        "pitLineSegments": len(add_pit_segments()),
        "pitTouchedCells": len(pit_cells),
        "blockTouchedCells": len(block_cells),
        "prgBytes": len(image),
        "runtimeLineDrawing": False,
        "previewOnly": True,
    }
    OUT_META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_PRG}")
    print(f"Wrote {OUT_META}")
    print(json.dumps(meta["selectedPose"], indent=2))

def reconstruct_pose_segments(pose: dict) -> list[tuple[int, int, int, int]]:
    # Reconstruct the domino's exposed edges from occupied cells to keep the PRG builder
    # independent from storing the full segment array inside the report.
    world = [tuple(cell) for cell in pose["occupiedCells"]]
    occupied = set(world)
    face_defs = [
        ((-1, 0, 0), [(0,0,0),(0,1,0),(0,1,1),(0,0,1)]),
        ((1, 0, 0), [(1,0,0),(1,0,1),(1,1,1),(1,1,0)]),
        ((0, -1, 0), [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
        ((0, 1, 0), [(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
        ((0, 0, -1), [(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
        ((0, 0, 1), [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),
    ]
    edges = set()
    for x, y, z in world:
        for (dx, dy, dz), corners in face_defs:
            if (x + dx, y + dy, z + dz) in occupied:
                continue
            verts = [(x + cx, y + cy, z + cz) for cx, cy, cz in corners]
            for i in range(4):
                a = verts[i]
                b = verts[(i + 1) % 4]
                edges.add(tuple(sorted([a, b])))
    segments = []
    for a, b in sorted(edges):
        x1, y1 = project_vertex(a)
        x2, y2 = project_vertex(b)
        if (x1, y1) != (x2, y2):
            segments.append((x1, y1, x2, y2))
    return sorted(set(segments))

if __name__ == "__main__":
    main()
