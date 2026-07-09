#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
prg = ROOT / "dist" / "moving_cube_byte_span_animation.prg"
meta = ROOT / "dist" / "moving_cube_byte_span_animation_metadata.json"

if not prg.exists():
    raise SystemExit("Missing dist/moving_cube_byte_span_animation.prg")
if not meta.exists():
    raise SystemExit("Missing dist/moving_cube_byte_span_animation_metadata.json")

data = json.loads(meta.read_text())
if data.get("mode") != "C64 moving cube byte-span animation proof":
    raise SystemExit(f"Unexpected mode: {data.get('mode')}")
if data.get("source") != "dist/moving_cube_same_depth_byte_spans.json":
    raise SystemExit("Animation PRG does not consume byte-span source")
if data.get("frame_count", 0) < 4:
    raise SystemExit("Expected at least 4 moving-cube animation frames")
if data.get("generated_code_bytes", 0) <= 0:
    raise SystemExit("Generated code byte count missing")
if data.get("union_clear_offsets", 0) <= 0:
    raise SystemExit("Expected non-empty clear-offset union")

raw = prg.read_bytes()
load = raw[0] | (raw[1] << 8)
if load != 0x0801:
    raise SystemExit(f"Unexpected PRG load address: ${load:04x}")
if b"2061" not in raw[:32]:
    raise SystemExit("BASIC SYS2061 stub not found")

print("OK: moving cube byte-span animation PRG verified.")
