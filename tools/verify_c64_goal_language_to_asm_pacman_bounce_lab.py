#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labs" / "010_goal_language_to_asm_pacman_bounce"
SRC = LAB / "src"
BOARD = SRC / "board.txt"
META = SRC / "projected_board.json"
ASM = SRC / "generated.s"
INTENT = SRC / "generated_intent.json"
GENERATOR = SRC / "generate_asm.py"


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def read_board() -> list[str]:
    return BOARD.read_text().splitlines()


def is_traversable(rows: list[str], x: int, y: int) -> bool:
    return rows[y][x] in {".", "o", " ", "P", "G"}


def expected_legal_masks(rows: list[str]) -> list[list[int]]:
    masks: list[list[int]] = []
    for y, row in enumerate(rows):
        mask_row: list[int] = []
        for x, ch in enumerate(row):
            mask = 0
            if ch in {".", "o", " ", "P", "G"}:
                if y > 0 and is_traversable(rows, x, y - 1):
                    mask |= 0x01
                if y + 1 < len(rows) and is_traversable(rows, x, y + 1):
                    mask |= 0x02
                if x > 0 and is_traversable(rows, x - 1, y):
                    mask |= 0x04
                if x + 1 < len(row) and is_traversable(rows, x + 1, y):
                    mask |= 0x08
            mask_row.append(mask)
        masks.append(mask_row)
    return masks


def parse_byte_row(asm_text: str, label: str) -> list[int]:
    match = re.search(rf"^{re.escape(label)}:\n\s+\.byte\s+([^\n]+)", asm_text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing byte row {label}")
    values: list[int] = []
    for raw in match.group(1).split(","):
        token = raw.strip()
        if token.startswith("$"):
            values.append(int(token[1:], 16))
        else:
            values.append(int(token, 10))
    return values


def main() -> int:
    required_paths = [BOARD, META, ASM, INTENT, GENERATOR]
    for path in required_paths:
        if not path.exists():
            return fail(f"missing required file: {path}")

    rows = read_board()
    meta = json.loads(META.read_text())
    intent = json.loads(INTENT.read_text())
    asm_text = ASM.read_text()
    generator_text = GENERATOR.read_text()

    sprite_contract_path = LAB / "li" / "sprite_projection_contract.md"
    capture_contract_path = ROOT / "captures" / "CAPTURE_BACK_PACMAN_SPRITE_PROJECTION_CONTRACT.md"
    movement_contract_path = LAB / "li" / "pacman_movement_contract.md"
    movement_capture_path = ROOT / "captures" / "CAPTURE_BACK_PACMAN_MOVEMENT_CONTRACT.md"
    increment_ledger_path = LAB / "li" / "pacman_increment_ledger.md"
    assembly_efficiency_contract_path = LAB / "li" / "assembly_efficiency_contract.md"

    if not sprite_contract_path.exists():
        return fail("Lab 010 must include li/sprite_projection_contract.md")
    if not capture_contract_path.exists():
        return fail("captures/CAPTURE_BACK_PACMAN_SPRITE_PROJECTION_CONTRACT.md must exist")

    sprite_contract = sprite_contract_path.read_text()
    capture_contract = capture_contract_path.read_text()
    movement_contract = movement_contract_path.read_text()
    movement_capture = movement_capture_path.read_text()
    increment_ledger = increment_ledger_path.read_text()
    assembly_efficiency_contract = assembly_efficiency_contract_path.read_text()

    for required_line in [
        "Do not treat board projection as proof of sprite centering.",
        "return 17 + (left + x) * 8",
        "return 44 + (top + y) * 8",
        "Sprite projection answers:",
    ]:
        if required_line not in sprite_contract:
            return fail(f"sprite projection contract missing: {required_line}")

    if "Lab 010 has two coordinate systems that must not be conflated" not in capture_contract:
        return fail("sprite projection Capture Back must document the coordinate-system boundary")

    for required_line in [
        "Pac-Man-style continuous motion with buffered turn requests.",
        "Pac-Man must not auto-select a new direction merely because he reached the end of a hallway.",
        "The runtime should preserve the most recent requested direction and apply it when that direction becomes legal.",
        "D.8 implements a C64 W/A/S/D keyboard fallback.",
    ]:
        if required_line not in movement_contract:
            return fail(f"movement contract missing: {required_line}")

    for required_line in [
        "Pac-Man should not auto-turn at hallway ends.",
        "The right fix is reliable buffered input.",
        "no automatic turn selection",
    ]:
        if required_line not in movement_capture:
            return fail(f"movement Capture Back missing: {required_line}")

    for required_line in [
        "D.6 — Auto-turn experiment",
        "Superseded.",
        "D.7 — Buffered requested turns",
        "D.8 — W/A/S/D keyboard fallback",
        "Auto-turning is not the target behavior.",
    ]:
        if required_line not in increment_ledger:
            return fail(f"increment ledger missing: {required_line}")

    for required_line in [
        "The learning surface is language and LI.",
        "generated assembly should be compact",
        "table-driven board renderer",
        "Unrolled per-cell board writes are superseded",
    ]:
        if required_line not in assembly_efficiency_contract:
            return fail(f"assembly efficiency contract missing: {required_line}")

    if meta.get("width") != len(rows[0]) or meta.get("height") != len(rows):
        return fail("projected_board.json dimensions do not match board.txt")

    if intent.get("milestone") != "pacman_buffered_turn_keyboard_fallback_control":
        return fail("generated_intent.json does not declare pacman_buffered_turn_keyboard_fallback_control")

    joystick = intent.get("joystickControl", {})
    if joystick.get("enabled") is not True:
        return fail("intent must declare joystick control enabled")
    if joystick.get("port") != "$dc00":
        return fail("intent must declare joystick port $dc00")
    if joystick.get("activeLow") is not True:
        return fail("intent must declare active-low joystick control")
    if joystick.get("movementPolicy") != "Pac-Man starts moving immediately, continues in the current legal direction, and applies buffered joystick or keyboard requested turns when legal at cell centers":
        return fail("intent must declare buffered joystick/keyboard requested-turn movement policy")
    if joystick.get("wallPolicy") != "blocked requested turns are ignored; if current momentum is blocked and no buffered legal turn exists, Pac-Man stops":
        return fail("intent must declare blocked requested turns stop only when current momentum is blocked")
    if joystick.get("keyboardFallback") != "W/A/S/D keys update the same requested direction buffer as joystick input":
        return fail("intent must declare W/A/S/D keyboard fallback into requested direction buffer")

    assembly_efficiency = intent.get("assemblyEfficiency", {})
    if assembly_efficiency.get("renderer") != "table-driven board renderer":
        return fail("intent must declare table-driven board renderer")
    if assembly_efficiency.get("unrolledBoardWrites") is not False:
        return fail("intent must declare unrolled board writes disabled")
    if assembly_efficiency.get("auditBoardTextInAssembly") is not False:
        return fail("intent must declare board text audit removed from assembly")

    sprite_projection = intent.get("spriteProjection", {})
    if sprite_projection.get("spriteOriginTuning") != "sprite y origin lowered by one pixel and x origin shifted left by three pixels for hallway centering":
        return fail("intent must preserve C.15 sprite origin tuning")
    if sprite_projection.get("movement") != "pixel interpolation between board-cell centers":
        return fail("intent must preserve pixel interpolation movement")
    if sprite_projection.get("verticalSpriteArt") != "north/south mouth uses same radial sprite geometry as east/west":
        return fail("intent must preserve radial vertical mouth sprite art")

    for snippet in [
        "Milestone D.8: buffered-turn Pac-Man with W/A/S/D keyboard fallback",
        "START_DIR_PTR =",
        "START_TARGET_CELL_X =",
        "START_TARGET_CELL_Y =",
        "START_TARGET_SPRITE_X_LO =",
        "START_TARGET_SPRITE_Y =",
        "continue_current_direction:",
        "requested_dir_ptr:",
        "read_input_buffer:",
        "read_keyboard_fallback:",
        "keyboard_buffer_up:",
        "keyboard_buffer_left:",
        "keyboard_buffer_down:",
        "keyboard_buffer_right:",
        "KEYBOARD_ROW_PORT = $dc00",
        "KEYBOARD_COL_PORT = $dc01",
        "keyboard_row_state:",
        "buffer_left:",
        "buffer_right:",
        "buffer_up:",
        "buffer_down:",
        "choose_next_target_from_buffer:",
        "try_requested_left:",
        "try_requested_right:",
        "try_requested_up:",
        "try_requested_down:",
        "try_current_left:",
        "try_current_right:",
        "try_current_up:",
        "try_current_down:",
        "stop_at_cell_center:",
        ".segment \"LOADADDR\"",
        "PRG file load address",
        ".word $0801",
        ".segment \"EXEHDR\"",
        "10 SYS 2061",
        "$9e, $32, $30, $36, $31",
        "BOARD_PTR = $f7",
        "COLOR_PTR = $f9",
        "render_board_row_loop:",
        "render_board_col_loop:",
        "board_render_rows:",
        "board_render_row_lo:",
        "board_render_row_hi:",
        "color_addr_row_lo:",
        "color_addr_row_hi:",
        "JOY_PORT_2 = $dc00",
        "JOY_UP = $01",
        "JOY_DOWN = $02",
        "JOY_LEFT = $04",
        "JOY_RIGHT = $08",
        "load_legal_mask:",
        "legal_move_rows:",
        "legal_row_lo:",
        "legal_row_hi:",
        "sprite_x_lo_by_cell:",
        "sprite_x_hi_by_cell:",
        "sprite_y_by_cell:",
        "set_target_sprite_from_cell:",
        "move_sprite_toward_target:",
        "copy_sprite_page0:",
        "copy_sprite_page1:",
        "SPRITE_DATA_BYTES = 512",
    ]:
        if snippet not in asm_text:
            return fail(f"generated.s missing expected snippet: {snippet}")

    if "path_x:" in asm_text or "path_sprite_x_lo:" in asm_text:
        return fail("joystick milestone should not use generated random path tables")

    if "auto_turn_from_blocked_momentum:" in asm_text:
        return fail("movement LI now forbids auto-turning; implement buffered requested turns instead")

    if "; board[" in asm_text:
        return fail("unrolled board writes are superseded; use compact table-driven renderer")
    if "board_row_00:" in asm_text:
        return fail("audit board_row_* data should not be embedded in generated assembly")

    masks = expected_legal_masks(rows)
    for y, expected_row in enumerate(masks):
        actual = parse_byte_row(asm_text, f"legal_row_{y:02d}")
        if actual != expected_row:
            return fail(f"legal move mask row {y:02d} does not match board.txt")

    if "legal_move_masks" not in generator_text:
        return fail("generate_asm.py must generate joystick legal move masks from board.txt")
    if "JOY_PORT_2 = $dc00" not in asm_text:
        return fail("generated assembly must read joystick port 2")
    if "radial_pacman_sprite" not in generator_text:
        return fail("generate_asm.py must preserve radial Pac-Man sprite generation")

    full_rule_paths = {
        "li/pacman_rule_source_inventory.md": LAB / "li" / "pacman_rule_source_inventory.md",
        "li/pacman_full_game_rule_contract.md": LAB / "li" / "pacman_full_game_rule_contract.md",
        "li/pacman_implementation_lane.md": LAB / "li" / "pacman_implementation_lane.md",
        "captures/CAPTURE_BACK_PACMAN_FULL_RULE_SPEC_DIRECTION.md": ROOT / "captures" / "CAPTURE_BACK_PACMAN_FULL_RULE_SPEC_DIRECTION.md",
    }
    for label, path in full_rule_paths.items():
        if not path.exists():
            return fail(f"missing Pac-Man full-rule LI file: {label}")

    source_inventory = full_rule_paths["li/pacman_rule_source_inventory.md"].read_text()
    full_rule_contract = full_rule_paths["li/pacman_full_game_rule_contract.md"].read_text()
    implementation_lane = full_rule_paths["li/pacman_implementation_lane.md"].read_text()
    full_rule_capture = full_rule_paths["captures/CAPTURE_BACK_PACMAN_FULL_RULE_SPEC_DIRECTION.md"].read_text()

    for required_line in [
        "The Pac-Man Dossier",
        "small dot: 10 points",
        "energizer: 50 points",
        "frightened ghosts in one energizer chain: 200, 400, 800, 1600",
        "Lab 010 uses its own projected board.",
    ]:
        if required_line not in source_inventory:
            return fail(f"rule source inventory missing: {required_line}")

    for required_line in [
        "Dot and scoring rules",
        "Round completion",
        "Energizers and frightened mode",
        "Ghost common movement",
        "Scatter and chase modes",
        "Individual ghost targeting",
        "Collision and lives",
        "Fruit",
        "Level progression",
    ]:
        if required_line not in full_rule_contract:
            return fail(f"full-game rule contract missing: {required_line}")

    for required_line in [
        "Next slice: F.2 scoring",
        "consuming a small dot adds 10",
        "consuming an energizer adds 50",
        "consumed cells do not score twice",
        "score is visible on screen",
    ]:
        if required_line not in implementation_lane:
            return fail(f"implementation lane missing: {required_line}")

    for required_line in [
        "F.2 should be scoring.",
        "Scoring is the right next feature",
        "Do not implement the full game at once.",
    ]:
        if required_line not in full_rule_capture:
            return fail(f"full-rule Capture Back missing: {required_line}")

    print("OK: C64 Lab 010 uses buffered turns, compact rendering, and full-rule LI direction.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
