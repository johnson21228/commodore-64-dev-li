#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
BASE_BUILDER = LAB / "tools" / "build_p02_domino_top_endpoint_preview_prg.py"
OUT_PRG = LAB / "dist" / "p02_domino_white_dashed_pit_preview.prg"
OUT_META = LAB / "dist" / "p02_domino_white_dashed_pit_preview_metadata.json"

LOAD_ADDR = 0x0801
SYS_ADDR = 0x080D
SCREEN_ADDR = 0x4400
BITMAP_ADDR = 0x6000
VIC_BANK = 1

def load_base():
    spec = importlib.util.spec_from_file_location("p02_top_endpoint_base", BASE_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base builder: {BASE_BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def plot(bitmap: bytearray, touched_cells: set[int], x: int, y: int) -> None:
    if not (0 <= x < 320 and 0 <= y < 200):
        return
    off = (y // 8) * 320 + (x // 8) * 8 + (y % 8)
    bitmap[off] |= 1 << (7 - (x % 8))
    touched_cells.add((y // 8) * 40 + (x // 8))

def draw_dashed_line(base, bitmap: bytearray, touched_cells: set[int], a: tuple[int, int], b: tuple[int, int]) -> None:
    points = base.bresenham(a, b)
    # Subtle pit language: short on / longer off. The active block remains solid.
    # This keeps all lines white while preserving visual hierarchy.
    dash_on = 2
    dash_period = 7
    for i, (x, y) in enumerate(points):
        if (i % dash_period) < dash_on:
            plot(bitmap, touched_cells, x, y)

def draw_solid_line(base, bitmap: bytearray, touched_cells: set[int], a: tuple[int, int], b: tuple[int, int]) -> None:
    for x, y in base.bresenham(a, b):
        plot(bitmap, touched_cells, x, y)

def main() -> None:
    base = load_base()
    report = json.loads(base.REPORT.read_text(encoding="utf-8"))
    pose = base.select_pose(report)

    bitmap = bytearray(8000)
    screen = bytearray([0x10] * 1000)  # white foreground, black background everywhere.

    pit_cells: set[int] = set()
    for a, b in base.add_pit_segments():
        draw_dashed_line(base, bitmap, pit_cells, a, b)

    block_cells: set[int] = set()
    for x1, y1, x2, y2 in base.reconstruct_pose_segments(pose):
        draw_solid_line(base, bitmap, block_cells, (x1, y1), (x2, y2))

    image_size = 0x8000 - LOAD_ADDR
    image = bytearray([0x00] * image_size)
    image[0:2] = bytes([LOAD_ADDR & 0xff, LOAD_ADDR >> 8])

    def put(addr: int, data: bytes | bytearray) -> None:
        start = addr - LOAD_ADDR + 2
        image[start:start + len(data)] = data

    put(0x0801, base.basic_stub())
    put(SYS_ADDR, base.machine_code())
    put(SCREEN_ADDR, screen)
    put(BITMAP_ADDR, bitmap)

    OUT_PRG.parent.mkdir(parents=True, exist_ok=True)
    OUT_PRG.write_bytes(bytes(image))

    meta = {
        "schemaVersion": 1,
        "program": str(OUT_PRG),
        "mode": "P02_DOMINO white active block with subtle dashed white pit preview",
        "sourceReport": str(base.REPORT),
        "selectedPose": {
            "pieceId": pose["pieceId"],
            "rotationId": pose["rotationId"],
            "x": pose["x"],
            "y": pose["y"],
            "z": pose["z"],
            "occupiedCells": pose["occupiedCells"],
            "projectedLineSegmentCount": pose["projectedLineSegmentCount"],
        },
        "lineLanguage": {
            "pit": "white subtle dashed lines, dash_on=2, dash_period=7",
            "activeBlock": "solid white outline",
            "reason": "Avoid C64 hi-res 8x8 color-cell conflict by using one foreground color and differentiating by line style."
        },
        "colors": {
            "foreground": "white",
            "background": "black",
            "pitColor": "white",
            "activeBlockColor": "white"
        },
        "memoryLayout": {
            "loadAddress": hex(LOAD_ADDR),
            "sysAddress": hex(SYS_ADDR),
            "vicBank": VIC_BANK,
            "screenAddress": hex(SCREEN_ADDR),
            "bitmapAddress": hex(BITMAP_ADDR),
        },
        "pitLineSegments": len(base.add_pit_segments()),
        "pitTouchedCells": len(pit_cells),
        "blockTouchedCells": len(block_cells),
        "prgBytes": len(image),
        "runtimeLineDrawing": False,
        "previewOnly": True,
    }
    OUT_META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_PRG}")
    print(f"Wrote {OUT_META}")
    print(json.dumps({
        "selectedPose": meta["selectedPose"],
        "lineLanguage": meta["lineLanguage"],
        "pitTouchedCells": meta["pitTouchedCells"],
        "blockTouchedCells": meta["blockTouchedCells"],
        "prgBytes": meta["prgBytes"],
    }, indent=2))

if __name__ == "__main__":
    main()
