#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labs" / "010_goal_language_to_asm_pacman_bounce"
errors: list[str] = []


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing {rel}")
        return ""
    return path.read_text(errors="ignore")


if not LAB.exists():
    errors.append("missing authoritative Lab 010 directory")
if (ROOT / "labs/010_pac_mouth_motion").exists():
    errors.append("duplicate standalone Lab 010 still exists: labs/010_pac_mouth_motion")
if (LAB / "src/main.c").exists():
    errors.append("Lab 010 must not include src/main.c")

files = {
    "goal": read("labs/010_goal_language_to_asm_pacman_bounce/src/goal.lang"),
    "program": read("labs/010_goal_language_to_asm_pacman_bounce/src/program.lang"),
    "generator": read("labs/010_goal_language_to_asm_pacman_bounce/src/generate_asm.py"),
    "asm": read("labs/010_goal_language_to_asm_pacman_bounce/src/generated.s"),
    "readme": read("labs/010_goal_language_to_asm_pacman_bounce/README.md"),
    "expected": read("labs/010_goal_language_to_asm_pacman_bounce/expected.md"),
    "docs": read("docs/c64/goal_language_to_asm_pacman_bounce_lab.md"),
    "capture": read("captures/CAPTURE_BACK_C64_GOAL_LANGUAGE_TO_ASM_PACMAN_BOUNCE_LAB.md"),
    "card": read("cards/016_c64_goal_language_to_asm_pacman_bounce_lab_card.md"),
    "prompt": read("prompts/c64_build_goal_language_pacman_bounce_lab.md"),
    "makefile": read("Makefile"),
}
combined = "\n".join(files.values())

for token in [
    "goal.lang", "program.lang", "generated_intent.json", "generated.s", "No main.c", "dx_vel", "dy_vel", "direction_from_vector", "face mouth with dx dy vector", "left/right-only", "vector-facing", "SPRITE_DATA_POINTER_CLOSED", "mouth_vector_north_01", "mouth_vector_south_01", "mouth_vector_horizontal_01",
]:
    if token not in combined:
        errors.append(f"missing merged Pac-Man vector-mouth token {token!r}")

for direction in ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]:
    if direction not in combined:
        errors.append(f"missing mouth direction {direction}")
    if f"SPRITE_DATA_POINTER_OPEN_{direction}" not in files["asm"]:
        errors.append(f"generated.s missing pointer for open direction {direction}")
    if f"pacman_sprite_open_{direction.lower()}_data" not in files["asm"]:
        errors.append(f"generated.s missing sprite data label for open direction {direction}")

if "verify_c64_pac_mouth_lab.py" in files["makefile"]:
    errors.append("Makefile still points at stale standalone Pac-mouth verifier")
if "labs/010_pac_mouth_motion" in files["makefile"]:
    errors.append("Makefile still points lab010 at duplicate standalone Pac-mouth lab")
for token in ["tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py", "tools/verify_c64_goal_language_to_asm_net_proxy_lab.py", "labs/010_goal_language_to_asm_pacman_bounce", "labs/011_goal_language_to_asm_net_proxy"]:
    if token not in files["makefile"]:
        errors.append(f"Makefile missing {token}")

for stale in ["tools/verify_c64_pac_mouth_lab.py", "docs/c64/pac_mouth_motion_app.md", "captures/CAPTURE_BACK_C64_PAC_MOUTH_MOTION.md", "cards/016_c64_pac_mouth_motion_card.md", "prompts/c64_run_lab_010_pac_mouth_motion.md"]:
    if (ROOT / stale).exists():
        errors.append(f"stale duplicate artifact remains: {stale}")

try:
    payload = json.loads((LAB / "src/generated_intent.json").read_text())
    if payload.get("optimization_posture") != "runtime_speed_first":
        errors.append("generated_intent.json missing runtime_speed_first optimization posture")
    if payload.get("output_contract") != "assembly_only_no_main_c":
        errors.append("generated_intent.json missing assembly-only output contract")
    if payload.get("mouth_orientation") != "direction_from_vector(dx_vel, dy_vel)":
        errors.append("generated_intent.json missing vector mouth orientation")
    expected_dirs = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
    if payload.get("supported_mouth_directions") != expected_dirs:
        errors.append("generated_intent.json missing all eight mouth directions")
    program_ops = {item.get("op") for item in payload.get("program", [])}
    if "face_mouth_with_vector" not in program_ops:
        errors.append("generated_intent.json missing face_mouth_with_vector program op")
except Exception as exc:
    errors.append(f"generated_intent.json is not valid JSON: {exc}")

asm_text = files["asm"]
for forbidden in ["#include", "clrscr", "cputsxy", "main()", "_main.c"]:
    if forbidden in asm_text:
        errors.append(f"generated.s contains forbidden C/helper token {forbidden!r}")
if "main.c" in asm_text and "No main.c" not in asm_text:
    errors.append("generated.s appears to depend on C source")
if asm_text.count("fast_clear_loop_01:") != 1:
    errors.append("generated.s must contain exactly one fast_clear_loop_01 label")
if "sta $06e8,x" in asm_text or "sta $dae8,x" in asm_text:
    errors.append("generated.s should use exact 1000-byte clear, not overlapping 256-page clear")

try:
    subprocess.run([sys.executable, "src/generate_asm.py", "src/goal.lang", "src/program.lang", "src/generated_intent.json", "src/generated.s"], cwd=LAB, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
except Exception as exc:
    errors.append(f"Lab 010 generator failed: {exc}")

if errors:
    print("C64 Goal Language Pac-Man Bounce Lab verification failed:")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("OK: C64 Lab 010 goal-language Pac-Man bounce owns vector-facing mouth behavior from dx/dy.")
