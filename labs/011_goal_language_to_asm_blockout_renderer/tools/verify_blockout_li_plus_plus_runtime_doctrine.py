#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

lab = Path("labs/011_goal_language_to_asm_blockout_renderer")
li = Path("li/labs")
contract_path = lab / "source" / "blockout_li_plus_plus_runtime_doctrine.json"
capture_path = lab / "captures" / "CAPTURE_BACK_LI_PLUS_PLUS_LEAN_RUNTIME_DOCTRINE.md"
li_path = li / "011_goal_language_to_asm_blockout_renderer_li_plus_plus_runtime_doctrine.md"

errors = []
for path in [contract_path, capture_path, li_path]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    if contract.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    doctrine = contract.get("doctrine", {})
    if doctrine.get("runtimeRole") != "lean_deterministic_executor":
        errors.append("runtimeRole must be lean_deterministic_executor")
    if doctrine.get("payloadRole") != "contract_between_generator_and_runtime":
        errors.append("payloadRole must make payload the generator/runtime contract")
    forbidden = set(contract.get("runtimeForbiddenResponsibilities", []))
    for item in [
        "3d_rotation_matrix_math",
        "projection_math",
        "active_piece_line_rasterization",
        "bitmap_mask_discovery",
        "all_shapes_resident_pose_table_storage",
        "semantic_shape_interpretation",
    ]:
        if item not in forbidden:
            errors.append(f"missing forbidden runtime responsibility: {item}")
    memory = contract.get("residentMemoryDoctrine", {})
    if memory.get("rule") != "resident_memory_must_earn_its_rent":
        errors.append("resident memory rule must be resident_memory_must_earn_its_rent")
    prefer = set(memory.get("prefer", []))
    for item in [
        "one_active_payload_slot",
        "small_indices_and_pointers",
        "cell_occupancy_over_locked_piece_objects",
        "generated_records_over_runtime_derivation",
        "file_io_as_memory_strategy",
    ]:
        if item not in prefer:
            errors.append(f"missing memory preference: {item}")
    consequences = set(contract.get("testableConsequences", []))
    for item in [
        "reject_all_starter_piece_payloads_resident_by_default",
        "reject_runtime_projection_for_active_pieces",
        "reject_locked_blocks_as_locked_piece_objects",
        "reject_sprites_as_primary_active_piece_renderer",
        "reject_removal_of_one_current_payload_memory_boundary",
        "reject_bypass_of_source_verifier_payload_discipline",
    ]:
        if item not in consequences:
            errors.append(f"missing testable consequence: {item}")
    checks = [
        (capture_path, "The intelligence lives upstream."),
        (capture_path, "The payload is the contract."),
        (capture_path, "The C64 does not reason about Blockout."),
        (li_path, "A byte in resident memory must earn its rent."),
        (li_path, "Meaning belongs upstream:"),
    ]
    for path, needle in checks:
        if needle not in path.read_text(encoding="utf-8"):
            errors.append(f"{path} missing expected text: {needle}")

if errors:
    print("ERROR: Lab 011 LI++ lean runtime doctrine verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: Lab 011 LI++ lean runtime doctrine verified.")
