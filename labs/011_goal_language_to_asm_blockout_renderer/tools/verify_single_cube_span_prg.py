#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
prg_path = ROOT / "dist" / "single_cube_span_fill.prg"
meta_path = ROOT / "dist" / "single_cube_span_fill_metadata.json"
spans_path = ROOT / "dist" / "single_cube_polygon_spans.json"

if not prg_path.exists():
    raise SystemExit("Missing dist/single_cube_span_fill.prg")
if not meta_path.exists():
    raise SystemExit("Missing dist/single_cube_span_fill_metadata.json")
if not spans_path.exists():
    raise SystemExit("Missing dist/single_cube_polygon_spans.json")

prg = prg_path.read_bytes()
if len(prg) < 2 + 8000:
    raise SystemExit("single_cube_span_fill.prg is too small to contain a bitmap payload")

load_addr = prg[0] | (prg[1] << 8)
if load_addr != 0x0801:
    raise SystemExit(f"Unexpected PRG load address: ${load_addr:04x}")

if b"2061" not in prg[:32]:
    raise SystemExit("BASIC SYS2061 stub not found near PRG start")

meta = json.loads(meta_path.read_text(encoding="utf-8"))
spans = json.loads(spans_path.read_text(encoding="utf-8"))

if meta.get("source_spans") != "dist/single_cube_polygon_spans.json":
    raise SystemExit("Span-fill PRG metadata does not point to generated spans")
if meta.get("source_pit_segments") != "dist/pit_line_segments.json":
    raise SystemExit("Span-fill PRG metadata does not point to pit line segments")
if meta.get("cube_context") != "off_side_cube_in_perspective_pit":
    raise SystemExit("Span-fill PRG does not declare off-side cube pit context")
if meta.get("total_spans") != spans.get("total_spans"):
    raise SystemExit("PRG metadata span count does not match span JSON")
if meta.get("pit_line_segments", 0) < 10:
    raise SystemExit("PRG metadata does not include meaningful pit segment count")
if meta.get("bitmap_bytes") != 8000:
    raise SystemExit("Expected 8000 bitmap bytes")
if meta.get("mode") != "C64 standard hi-res bitmap span-fill proof with pit context":
    raise SystemExit("Unexpected span-fill PRG mode metadata")

print("OK: off-side cube C64 bitmap/span-fill PRG with pit context verified.")
