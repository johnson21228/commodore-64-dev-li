#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

lab = Path("labs/011_goal_language_to_asm_blockout_renderer")
li = Path("li/labs")

contract_path = lab / "source" / "blockout_runtime_pipeline_contract.json"
capture_path = lab / "captures" / "CAPTURE_BACK_ACTIVE_PIECE_PIPELINE_AND_LOCKED_OCCUPANCY.md"
li_path = li / "011_goal_language_to_asm_blockout_renderer_active_piece_pipeline.md"

errors = []

for path in [contract_path, capture_path, li_path]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    if contract.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")

    lifecycle = contract.get("activePieceLifecycle", {})
    if lifecycle.get("pieceExistsOnlyWhileActive") is not True:
        errors.append("active piece must exist only while active")

    if lifecycle.get("visualRole") != "dynamic_white_wireframe_overlay":
        errors.append("active piece visual role must be dynamic white wireframe overlay")

    locked = contract.get("lockedOccupancyModel", {})
    if locked.get("authoritativeTruth") != "cell_occupancy_grid":
        errors.append("locked occupancy authority must be cell_occupancy_grid")

    if locked.get("notModeledAs") != "locked_piece_objects":
        errors.append("locked occupancy must not be modeled as locked piece objects")

    piece_io = contract.get("piecePayloadFileIO", {})
    if piece_io.get("designTarget") != "one_compact_payload_file_per_piece_family":
        errors.append("piece payload design target must be one file per piece family")

    if piece_io.get("activeMemoryBoundary") != "only_current_piece_payload_loaded_or_copied_into_ACTIVE_PIECE_TABLE":
        errors.append("active memory boundary must load/copy only the current piece payload")

    non_goals = set(contract.get("runtimeNonGoals", []))
    for item in [
        "3d_rotation_matrix_math",
        "projection_math",
        "line_rasterization_for_active_piece",
        "bitmap_mask_discovery",
        "all_shapes_resident_payload_storage",
    ]:
        if item not in non_goals:
            errors.append(f"missing runtime non-goal: {item}")

    sprite = contract.get("spritePolicy", {})
    if sprite.get("spritesArePrimaryPieceRenderer") is not False:
        errors.append("sprites must not be primary piece renderer")

    if sprite.get("primaryActivePieceRenderer") != "bitmap_dirty_overlay_records":
        errors.append("primary active renderer must be bitmap dirty overlay records")

    text_checks = [
        (capture_path, "Locked blocks are not locked pieces."),
        (capture_path, "Precompute per-piece payloads offline."),
        (li_path, "A piece does not become a locked piece."),
        (li_path, "The active falling piece remains bitmap-rendered from generated dirty records."),
    ]

    for path, needle in text_checks:
        if needle not in path.read_text(encoding="utf-8"):
            errors.append(f"{path} missing expected text: {needle}")

if errors:
    print("ERROR: Lab 011 runtime pipeline contract verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: Lab 011 active-piece payload and locked-occupancy pipeline contract verified.")
