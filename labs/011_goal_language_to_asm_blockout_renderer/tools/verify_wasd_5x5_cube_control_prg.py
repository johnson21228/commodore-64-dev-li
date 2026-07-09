#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
prg = ROOT / "dist" / "wasd_5x5_cube_control.prg"
meta = ROOT / "dist" / "wasd_5x5_cube_control_metadata.json"

if not prg.exists():
    raise SystemExit("Missing dist/wasd_5x5_cube_control.prg")
if not meta.exists():
    raise SystemExit("Missing dist/wasd_5x5_cube_control_metadata.json")

data = json.loads(meta.read_text())
if data.get("mode") != "C64 pit-only compact-payload projection tuning proof":
    raise SystemExit(f"Unexpected mode: {data.get('mode')}")
if data.get("active_piece_render") != "disabled_pit_tuning":
    raise SystemExit("Active piece should be disabled")
if data.get("payload_strategy") != "compact_nonzero_bitmap_byte_records":
    raise SystemExit("Expected compact pit payload strategy")
mem = data.get("memory_layout", {})
if mem.get("vic_bank") != 1 or mem.get("screen_addr") != "$4400" or mem.get("bitmap_addr") != "$6000":
    raise SystemExit(f"Unexpected compact memory layout: {mem}")

pit = data.get("pit", {})
if pit.get("width") != 5 or pit.get("height") != 5 or pit.get("visual_depth") != 10:
    raise SystemExit(f"Unexpected pit: {pit}")

vp = data.get("projection_viewport", {})
if vp.get("far_square_pixels") != 72 or vp.get("near_square_pixels") != 196:
    raise SystemExit(f"Unexpected near/far square projection: {vp}")
if vp.get("visible_ring_zs") != [0, 1, 2, 3, 4, 5, 6, 8, 10]:
    raise SystemExit(f"Unexpected selected visible rings: {vp}")
if vp.get("wall_grid_guides") != "all_5x5_boundary_divisions":
    raise SystemExit(f"Missing all wall grid guides: {vp}")
if vp.get("top_plane_clutter") != "none":
    raise SystemExit(f"Top-plane clutter should be absent: {vp}")

if data.get("pit_record_count", 0) <= 0:
    raise SystemExit("No pit byte records generated")
if data.get("pit_record_payload_bytes", 999999) >= 10000:
    raise SystemExit(f"Compact payload did not beat old 10K source payload: {data.get('pit_record_payload_bytes')}")

raw = prg.read_bytes()
load = raw[0] | (raw[1] << 8)
if load != 0x0801:
    raise SystemExit(f"Unexpected load address: ${load:04x}")
if b"2061" not in raw[:32]:
    raise SystemExit("BASIC SYS2061 stub not found")

print("OK: pit-only compact-payload PRG verified.")
