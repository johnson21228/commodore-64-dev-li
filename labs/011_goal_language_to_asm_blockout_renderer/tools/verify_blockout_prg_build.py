#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRG = ROOT / "dist" / "blockout_renderer.prg"
CELLS = ROOT / "dist" / "blockout_renderer_screen_cells.json"

if not PRG.exists():
    raise SystemExit("Missing dist/blockout_renderer.prg")

data = PRG.read_bytes()
if len(data) < 128:
    raise SystemExit(f"PRG unexpectedly small: {len(data)} bytes")

if data[:2] != bytes([0x01, 0x08]):
    raise SystemExit("PRG does not load at $0801")

# BASIC stub must contain SYS2061.
if bytes([0x9E, 0x32, 0x30, 0x36, 0x31]) not in data[:20]:
    raise SystemExit("PRG missing BASIC SYS2061 stub")

if not CELLS.exists():
    raise SystemExit("Missing dist/blockout_renderer_screen_cells.json")

cells = json.loads(CELLS.read_text(encoding="utf-8"))
if cells.get("source") != "dist/pit_line_segments.json":
    raise SystemExit("Screen cell map does not declare pit_line_segments as source")

if cells.get("cell_count", 0) < 40:
    raise SystemExit("Too few rendered cells to show governed board")

print("OK: first runnable Blockout renderer PRG verified.")
