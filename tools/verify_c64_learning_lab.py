from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "li/domain/c64_learning_lab_principles.md": ["C64 Learning Lab", "runnable"],
    "li/domain/lab_artifact_contract.md": ["README.md", "expected.md"],
    "docs/c64/learning_lab_project_setup.md": ["Learning Lab", "emulator"],
    "docs/c64/lab_sequence.md": ["Lab 001", "Lab 008", "Lab 009"],
    "docs/c64/first_curriculum_batch.md": ["Lab 004", "Lab 008"],
    "captures/CAPTURE_BACK_C64_HELLO_WORLD_APP.md": ["Hello World"],
    "captures/CAPTURE_BACK_C64_SCREEN_MEMORY_APP.md": ["Screen Memory"],
    "captures/CAPTURE_BACK_C64_COLOR_MEMORY_APP.md": ["Color Memory"],
    "captures/CAPTURE_BACK_C64_FIRST_CURRICULUM_BATCH.md": ["PETSCII", "Memory Pal"],
    "cards/005_c64_hello_world_app_card.md": ["Hello World"],
    "cards/006_c64_screen_memory_app_card.md": ["Screen Memory"],
    "cards/007_c64_color_memory_app_card.md": ["Color Memory"],
    "docs/c64/petscii_ui_app.md": ["PETSCII"],
    "docs/c64/keyboard_input_app.md": ["Keyboard"],
    "docs/c64/sprite_basics_app.md": ["sprite"],
    "docs/c64/sid_tone_app.md": ["SID"],
    "docs/c64/memory_pal_app.md": ["Memory Pal"],
}

LABS = [
    ("001_hello_screen", "hello_screen"),
    ("002_screen_memory", "screen_memory"),
    ("003_color_memory", "color_memory"),
    ("004_petscii_ui", "petscii_ui"),
    ("005_keyboard_input", "keyboard_input"),
    ("006_sprite_basics", "sprite_basics"),
    ("007_sid_tone", "sid_tone"),
    ("008_memory_pal", "memory_pal"),
]

errors = []
for rel, needles in REQUIRED.items():
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing {rel}")
        continue
    text = path.read_text(errors="ignore")
    for needle in needles:
        if needle not in text:
            errors.append(f"{rel} missing token {needle!r}")

for folder, target in LABS:
    for rel in ["README.md", "expected.md", "Makefile", "src/main.c"]:
        path = ROOT / "labs" / folder / rel
        if not path.exists():
            errors.append(f"missing labs/{folder}/{rel}")
    mk = ROOT / "labs" / folder / "Makefile"
    if mk.exists() and target not in mk.read_text(errors="ignore"):
        errors.append(f"labs/{folder}/Makefile missing target name {target}")

makefile = (ROOT / "Makefile").read_text(errors="ignore") if (ROOT / "Makefile").exists() else ""
for n in range(1, 10):
    token = f"lab{n:03d}"
    if token not in makefile or f"{token}-run" not in makefile:
        errors.append(f"Makefile missing {token}/{token}-run shortcut")

if "labs/*/dist/*" not in makefile or "labs/*/src/*.o" not in makefile:
    errors.append("Makefile pack exclusions must omit generated lab dist files and object files")

if errors:
    print("C64 Learning Lab verification failed:")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("OK: C64 Learning Lab first curriculum labs 001-008 are present.")
