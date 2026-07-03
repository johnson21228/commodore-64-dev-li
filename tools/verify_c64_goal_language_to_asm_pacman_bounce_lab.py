#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labs" / "010_goal_language_to_asm_pacman_bounce"
SRC = LAB / "src"

BOARD = SRC / "board.txt"
META = SRC / "projected_board.json"
ASM = SRC / "generated.s"
INTENT = SRC / "generated_intent.json"
GENERATOR = SRC / "generate_asm.py"
PROJECTED_VERIFIER = SRC / "verify_projected_board.py"

ALLOWED = set("#.o PGX")
TRAVERSABLE = set(".o PG")


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def read_board() -> list[str]:
    rows = BOARD.read_text().splitlines()
    if not rows:
        raise AssertionError("board.txt is empty")
    width = len(rows[0])
    for y, row in enumerate(rows):
        if len(row) != width:
            raise AssertionError(f"board row {y} width mismatch")
        bad = sorted({ch for ch in row if ch not in ALLOWED})
        if bad:
            raise AssertionError(f"board row {y} has unsupported chars {bad}")
    return rows


def parse_asm_board_rows(text: str) -> list[str]:
    rows = []
    for _, payload in re.findall(r"board_row_(\d{2}):\n    \.byte ([^\n]+)", text):
        chars = []
        for raw in payload.split(","):
            raw = raw.strip()
            chars.append(chr(int(raw[1:], 16) if raw.startswith("$") else int(raw)))
        rows.append("".join(chars))
    return rows


def parse_byte_table(text: str, label: str) -> list[int]:
    pattern = rf"{re.escape(label)}:\n((?:    \.byte [^\n]+\n?)+)"
    match = re.search(pattern, text)
    if not match:
        raise AssertionError(f"missing byte table {label}")
    values = []
    for line in match.group(1).splitlines():
        payload = line.split(".byte", 1)[1]
        for raw in payload.split(","):
            raw = raw.strip()
            values.append(int(raw[1:], 16) if raw.startswith("$") else int(raw))
    return values


def pacman_start(rows: list[str]) -> tuple[int, int]:
    found = [(x, y) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch == "P"]
    if len(found) != 1:
        raise AssertionError(f"expected exactly one Pac-Man start, found {len(found)}")
    return found[0]


def legal_neighbors(rows: list[str], x: int, y: int) -> list[tuple[int, int]]:
    out = []
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(rows) and 0 <= nx < len(rows[ny]) and rows[ny][nx] in TRAVERSABLE:
            out.append((nx, ny))
    return out


def main() -> int:
    required = [
        BOARD,
        META,
        ASM,
        INTENT,
        GENERATOR,
        PROJECTED_VERIFIER,
        LAB / "BOARD_PROJECTION_LI.md",
        LAB / "assets" / "source_board.png",
        LAB / "c64_asm.cfg",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        return fail("missing required files: " + ", ".join(missing))

    projected = subprocess.run([sys.executable, str(PROJECTED_VERIFIER)], cwd=ROOT, text=True, capture_output=True)
    if projected.returncode != 0:
        print(projected.stdout)
        print(projected.stderr)
        return fail("projected board verifier failed")

    rows = read_board()
    meta = json.loads(META.read_text())
    intent = json.loads(INTENT.read_text())
    asm_text = ASM.read_text()
    generator_text = GENERATOR.read_text()

    sprite_contract_path = LAB / "li" / "sprite_projection_contract.md"
    capture_contract_path = LAB.parents[1] / "captures" / "CAPTURE_BACK_PACMAN_SPRITE_PROJECTION_CONTRACT.md"

    if not sprite_contract_path.exists():
        return fail("Lab 010 must include li/sprite_projection_contract.md")
    if not capture_contract_path.exists():
        return fail("captures/CAPTURE_BACK_PACMAN_SPRITE_PROJECTION_CONTRACT.md must exist")

    sprite_contract = sprite_contract_path.read_text()
    capture_contract = capture_contract_path.read_text()

    required_contract_lines = [
        "Do not treat board projection as proof of sprite centering.",
        "return 17 + (left + x) * 8",
        "return 44 + (top + y) * 8",
        "Sprite projection answers:",
    ]

    for required_line in required_contract_lines:
        if required_line not in sprite_contract:
            return fail(f"sprite projection contract missing: {required_line}")

    if "Lab 010 has two coordinate systems that must not be conflated" not in capture_contract:
        return fail("sprite projection Capture Back must document the coordinate-system boundary")
    if "The board projection can prove that Pac-Man is in a legal maze cell." not in capture_contract:
        return fail("sprite projection Capture Back must document board legality boundary")
    if "It does not, by itself, prove that the visible 24x21 hardware sprite is centered" not in capture_contract:
        return fail("sprite projection Capture Back must document sprite-centering boundary")

    if meta.get("width") != len(rows[0]) or meta.get("height") != len(rows):
        return fail("projected_board.json dimensions do not match board.txt")

    if intent.get("milestone") != "pacman_hardware_sprite_interpolation_retuned_xy_origin":
        return fail("generated_intent.json does not declare pacman_hardware_sprite_interpolation_retuned_xy_origin")

    if not intent.get("authority", {}).get("generatedAssemblyIsArtifact"):
        return fail("generated_intent.json must declare generated assembly as artifact")

    if parse_asm_board_rows(asm_text) != rows:
        return fail("generated.s board_row data does not match board.txt")

    path_x = parse_byte_table(asm_text, "path_x")
    path_y = parse_byte_table(asm_text, "path_y")
    sprite_x_lo = parse_byte_table(asm_text, "path_sprite_x_lo")
    sprite_x_hi = parse_byte_table(asm_text, "path_sprite_x_hi")
    sprite_y = parse_byte_table(asm_text, "path_sprite_y")
    sprite_ptr = parse_byte_table(asm_text, "path_sprite_ptr")

    lengths = {len(path_x), len(path_y), len(sprite_x_lo), len(sprite_x_hi), len(sprite_y), len(sprite_ptr)}
    if len(lengths) != 1:
        return fail("path and sprite interpolation table lengths differ")

    declared_len = intent.get("pacmanPathWalker", {}).get("pathLength")
    if declared_len != len(path_x):
        return fail(f"intent pathLength {declared_len} does not match generated path length {len(path_x)}")

    start = pacman_start(rows)
    if (path_x[0], path_y[0]) != start:
        return fail(f"path starts at {(path_x[0], path_y[0])}, expected Pac-Man start {start}")

    if not legal_neighbors(rows, *start):
        return fail("Pac-Man start has no legal move")

    visited = set()
    reversals = 0
    previous_delta = None

    for index, (x, y) in enumerate(zip(path_x, path_y)):
        if not (0 <= y < len(rows) and 0 <= x < len(rows[y])):
            return fail(f"path step {index} exits board at {(x, y)}")
        if rows[y][x] not in TRAVERSABLE:
            return fail(f"path step {index} enters blocked cell {(x, y)} = {rows[y][x]!r}")
        visited.add((x, y))

        if index > 0:
            px, py = path_x[index - 1], path_y[index - 1]
            dx, dy = x - px, y - py
            if abs(dx) + abs(dy) != 1:
                return fail(f"path step {index} is not orthogonal adjacent: {(px, py)} -> {(x, y)}")
            if previous_delta and (dx, dy) == (-previous_delta[0], -previous_delta[1]):
                reversals += 1
            previous_delta = (dx, dy)

    if len(visited) < 40:
        return fail(f"path visits only {len(visited)} unique cells")

    if reversals < 1:
        return fail("path should include at least one reverse direction")

    pointers = intent.get("spriteProjection", {}).get("spritePointers", {})
    expected_open_ptrs = {0xD0, 0xD1, 0xD2, 0xD3}
    expected_all_ptrs = {0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7}
    if set(pointers.values()) != expected_all_ptrs:
        return fail("intent must declare animated sprite pointers D0-D7")
    if not set(sprite_ptr).issubset(expected_open_ptrs):
        return fail("path sprite pointer table must use only open direction sprite pointers D0-D3")

    if any(value not in {0, 1} for value in sprite_x_hi):
        return fail("sprite x high-bit table must contain only 0/1")

    for snippet in [
        "Milestone C.15: radial Pac-Man sprite geometry with retuned x/y sprite origin",
        "SPRITE_DATA_ADDR = $3400",
        "SPRITE_PTR_E_OPEN = $d0",
        "SPRITE_PTR_W_OPEN = $d1",
        "SPRITE_PTR_N_OPEN = $d2",
        "SPRITE_PTR_S_OPEN = $d3",
        "SPRITE_PTR_E_CLOSED = $d4",
        "SPRITE_PTR_W_CLOSED = $d5",
        "SPRITE_PTR_N_CLOSED = $d6",
        "SPRITE_PTR_S_CLOSED = $d7",
        "init_sprite:",
        "set_sprite_position_from_index:",
        "set_target_for_index:",
        "move_sprite_toward_target:",
        "update_sprite_registers:",
        "update_mouth_animation:",
        "mouth_phase:",
        "copy_sprite_page0:",
        "copy_sprite_page1:",
        "SPRITE_DATA_BYTES = 512",
        "custom_sprites:",
        "path_sprite_x_lo:",
        "path_sprite_x_hi:",
        "path_sprite_y:",
        "path_sprite_ptr:",
        "board_row_00:",
        "board_row_21:",
    ]:
        if snippet not in asm_text:
            return fail(f"generated.s missing expected snippet: {snippet}")

    sprite_projection = intent.get("spriteProjection", {})
    if sprite_projection.get("enabledSprite") != 0:
        return fail("intent must declare sprite 0 for Pac-Man")
    if sprite_projection.get("movement") != "pixel interpolation between board-cell centers":
        return fail("intent must declare pixel interpolation movement")
    if sprite_projection.get("mouthAnimation") != "open and closed sprite frames alternate at a visible crunch pace while moving":
        return fail("intent must declare visible crunch mouth animation")
    if sprite_projection.get("mouthSpeedTuning") != "toggle every 8 frame-pixel updates":
        return fail("intent must declare 8-frame mouth crunch tuning")
    if sprite_projection.get("verticalSpriteArt") != "north/south mouth uses same radial sprite geometry as east/west":
        return fail("intent must declare radial vertical mouth sprite art")
    if sprite_projection.get("spriteFootprint") != "all directions use shared center, shared radius, and shared mouth-wedge rule":
        return fail("intent must declare shared radial sprite footprint")
    if sprite_projection.get("spriteGeometry") != "radial Pac-Man generated from one circle-like pixel model":
        return fail("intent must declare radial Pac-Man sprite geometry")
    if sprite_projection.get("spriteOriginTuning") != "sprite y origin lowered by one pixel and x origin shifted left by three pixels for hallway centering":
        return fail("intent must declare retuned x/y sprite origin centering")
    if sprite_projection.get("spriteCopyFix") != "copies all 512 bytes for eight sprite frames":
        return fail("intent must declare 512-byte sprite frame copy fix")
    if sprite_projection.get("speedTuning") != "two raster frames per interpolated pixel":
        return fail("intent must declare two-frame-per-pixel half-speed tuning")
    if sprite_projection.get("sizeTuning") != "smaller 10-12 pixel centered sprite body within 24x21 hardware sprite cell":
        return fail("intent must declare smaller 10-12 pixel centered sprite tuning")

    walker = intent.get("pacmanPathWalker", {})
    if walker.get("movementAuthority") != "board.txt traversable cells":
        return fail("intent must declare board.txt traversable cells as movement authority")

    if "build_sprites" not in generator_text or "cell_sprite_x" not in generator_text:
        return fail("generate_asm.py must include hardware sprite projection helpers")
    if "radial_pacman_sprite" not in generator_text or "mouth_slope" not in generator_text:
        return fail("generate_asm.py must include radial Pac-Man mouth geometry")

    print("OK: C64 Lab 010 Pac-Man uses retuned x/y-origin radial sprite art over verified board paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
