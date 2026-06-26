#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labs" / "010_goal_language_to_asm_pacman_bounce"
errors: list[str] = []

if not LAB.exists():
    errors.append("missing authoritative Lab 010 directory")

try:
    subprocess.run(
        [sys.executable, "src/generate_asm.py", "src/goal.lang", "src/program.lang", "src/generated_intent.json", "src/generated.s"],
        cwd=LAB,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
except Exception as exc:
    errors.append(f"Lab 010 generator failed: {exc}")

required_files = [
    "docs/c64/goal_language_to_asm_pacman_bounce_lab.md",
    "prompts/c64_build_goal_language_pacman_bounce_lab.md",
    "captures/CAPTURE_BACK_C64_GOAL_LANGUAGE_TO_ASM_PACMAN_BOUNCE_LAB.md",
    "cards/016_c64_goal_language_to_asm_pacman_bounce_lab_card.md",
    "labs/010_goal_language_to_asm_pacman_bounce/README.md",
    "labs/010_goal_language_to_asm_pacman_bounce/expected.md",
    "labs/010_goal_language_to_asm_pacman_bounce/Makefile",
    "labs/010_goal_language_to_asm_pacman_bounce/src/goal.lang",
    "labs/010_goal_language_to_asm_pacman_bounce/src/program.lang",
    "labs/010_goal_language_to_asm_pacman_bounce/src/generate_asm.py",
    "labs/010_goal_language_to_asm_pacman_bounce/src/generated_intent.json",
    "labs/010_goal_language_to_asm_pacman_bounce/src/generated.s",
]

combined = ""
for rel in required_files:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing {rel}")
        continue
    combined += "\n" + path.read_text(errors="ignore")

for token in [
    "goal.lang", "program.lang", "generated.s", "No main.c", "Pac-Man", "runtime_speed_first",
    "dx", "dy", "crunching mouth", "movement vector", "direction_from_vector", "left/right-only",
    "arcade-optimized", "direction_index", "mouth_dirty", "mouth_pointer_table_01",
]:
    if token not in combined:
        errors.append(f"missing arcade/vector token {token!r}")

asm_path = LAB / "src" / "generated.s"
asm_text = asm_path.read_text(errors="ignore") if asm_path.exists() else ""
for forbidden in ["#include", "clrscr", "cputsxy", "main()", "_main.c"]:
    if forbidden in asm_text:
        errors.append(f"generated.s contains forbidden C/helper token {forbidden!r}")
if "main.c" in asm_text and "No main.c" not in asm_text:
    errors.append("generated.s appears to depend on C source")

for required in [
    "SPRITE_POINTER_0 = $07f8",
    "SPRITE_DATA = $2000",
    "SPRITE_DATA_CLOSED = $2000",
    "SPRITE_DATA_OPEN_E = $2040",
    "SPRITE_DATA_OPEN_NE = $2080",
    "SPRITE_DATA_OPEN_N = $20c0",
    "SPRITE_DATA_OPEN_NW = $2100",
    "SPRITE_DATA_OPEN_W = $2140",
    "SPRITE_DATA_OPEN_SW = $2180",
    "SPRITE_DATA_OPEN_S = $21c0",
    "SPRITE_DATA_OPEN_SE = $2200",
    "DIR_E = $00",
    "DIR_NE = $01",
    "DIR_N = $02",
    "DIR_NW = $03",
    "DIR_W = $04",
    "DIR_SW = $05",
    "DIR_S = $06",
    "DIR_SE = $07",
    "FRAME_CLOSED = $00",
    "FRAME_OPEN_BASE = $01",
    "INITIAL_DIRECTION_INDEX",
    "direction_index:",
    "current_mouth_frame:",
    "mouth_dirty:",
    "mouth_pointer_table_01:",
    "refresh_direction_index_01:",
    "maybe_store_direction_index_01:",
    "apply_mouth_pointer_if_dirty_01:",
    "mouth_pointer_clean_01:",
    "mouth_pointer_dirty_01:",
    "lda mouth_dirty",
    "bne mouth_pointer_dirty_01",
    "cpx current_mouth_frame",
    "lda mouth_pointer_table_01,x",
    "sta SPRITE_POINTER_0",
    "jsr refresh_direction_index_01",
    "jsr apply_mouth_pointer_if_dirty_01",
    "fast_clear_loop_01:",
    "wait_frame_01:",
    "animate_mouth_01:",
    "pacman_sprite_closed_data:",
    "pacman_sprite_open_e_data:",
    "pacman_sprite_open_ne_data:",
    "pacman_sprite_open_n_data:",
    "pacman_sprite_open_nw_data:",
    "pacman_sprite_open_w_data:",
    "pacman_sprite_open_sw_data:",
    "pacman_sprite_open_s_data:",
    "pacman_sprite_open_se_data:",
]:
    if required not in asm_text:
        errors.append(f"generated.s missing assembly token {required!r}")

# Ensure pointer update is no longer an every-frame branch chain to open labels.
for stale in [
    "update_mouth_pointer_01:",
    "mouth_open_from_vector_01:",
    "mouth_dx_positive_01:",
    "mouth_dx_negative_01:",
    "mouth_open_e_01:",
    "mouth_open_ne_01:",
    "mouth_open_n_01:",
    "mouth_open_nw_01:",
    "mouth_open_w_01:",
    "mouth_open_sw_01:",
    "mouth_open_s_01:",
    "mouth_open_se_01:",
    "mouth_faces_left_01:",
    "mouth_faces_right_01:",
    "SPRITE_DATA_OPEN_RIGHT",
    "SPRITE_DATA_OPEN_LEFT",
]:
    if stale in asm_text:
        errors.append(f"generated.s still contains stale non-optimized token {stale!r}")

if asm_text.count("sta SPRITE_POINTER_0") != 1:
    errors.append("optimized runtime should have exactly one sprite pointer write site")
if asm_text.count("jsr refresh_direction_index_01") < 4:
    errors.append("expected refresh_direction_index_01 calls on all four bounce paths")

if (LAB / "src" / "main.c").exists():
    errors.append("Lab 010 must not include src/main.c")
if (ROOT / "labs/010_pac_mouth_motion").exists():
    errors.append("duplicate standalone pac mouth lab must not exist")

try:
    payload = json.loads((LAB / "src" / "generated_intent.json").read_text())
    if payload.get("optimization_posture") != "runtime_speed_first":
        errors.append("generated_intent.json missing runtime_speed_first optimization posture")
    if payload.get("runtime_optimization") != "arcade_optimized_dirty_pointer_cache":
        errors.append("generated_intent.json missing arcade optimized dirty pointer cache marker")
    if payload.get("output_contract") != "assembly_only_no_main_c":
        errors.append("generated_intent.json missing assembly-only output contract")
    if payload.get("app_model") != "yellow_pacman_sprite_linear_bounce_vector_facing_crunching_mouth":
        errors.append("generated_intent.json missing vector-facing Pac-Man app model")
    expected_dirs = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
    if payload.get("supported_mouth_directions") != expected_dirs:
        errors.append("generated_intent.json missing supported vector mouth directions")
    strategy = payload.get("assembly_strategy", {})
    if "mouth_pointer_table_01" not in json.dumps(strategy):
        errors.append("generated_intent.json strategy missing mouth_pointer_table_01")
    program_ops = {item.get("op") for item in payload.get("program", [])}
    for op in ["use_pacman_sprite", "animate_mouth", "face_mouth_with_vector", "move_sprite_velocity", "bounds", "bounce_reflect", "loop_forever"]:
        if op not in program_ops:
            errors.append(f"generated_intent.json missing program op {op}")
except Exception as exc:
    errors.append(f"generated_intent.json is not valid JSON: {exc}")

makefile = (ROOT / "Makefile").read_text(errors="ignore") if (ROOT / "Makefile").exists() else ""
for token in ["lab010", "lab010-run", "tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py", "labs/010_goal_language_to_asm_pacman_bounce"]:
    if token not in makefile:
        errors.append(f"Makefile missing {token}")

if errors:
    print("C64 Goal Language Pac-Man Bounce Lab verification failed:")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("OK: C64 Lab 010 generated Pac-Man game uses arcade-optimized cached vector-mouth pointer updates.")
