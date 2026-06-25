from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = [
    "li/domain/c64_development_principles.md",
    "li/domain/cross_development_model.md",
    "li/domain/emulator_first_hardware_later.md",
    "li/domain/c64_constraints.md",
    "li/domain/toolchain_source_authority.md",
    "docs/c64/application_brainstorm_chatbot.md",
    "docs/c64/thread_state_and_local_apply_notes.md",
    "docs/c64/learning_lab_project_setup.md",
    "docs/c64/first_curriculum_batch.md",
    "docs/visuals/c64_workbench_stage0_learning_loop.md",
    "docs/visuals/c64_workbench_stage0_learning_loop.png",
    "assets/visuals/c64_workbench_stage0_learning_loop/c64_workbench_stage0_learning_loop.png",
    "prompts/visuals/generate_c64_workbench_stage0_learning_loop_infographic.md",
    "cards/013_c64_workbench_stage0_learning_loop_ig_card.md",
    "captures/CAPTURE_BACK_C64_WORKBENCH_STAGE0_LEARNING_LOOP_IG.md",
    "docs/visuals/c64_workbench_stage0_learning_loop_for_hernan.md",
    "docs/visuals/c64_workbench_stage0_learning_loop_for_hernan.jpeg",
    "assets/visuals/c64_workbench_stage0_learning_loop/c64_workbench_stage0_learning_loop_for_hernan.jpeg",
    "source/visuals/c64_workbench_stage0_learning_loop_for_hernan_copy.md",
    "prompts/visuals/write_c64_workbench_stage0_learning_loop_hernan_copy.md",
    "cards/014_c64_workbench_stage0_learning_loop_hernan_copy_card.md",
    "captures/CAPTURE_BACK_C64_WORKBENCH_STAGE0_LEARNING_LOOP_HERNAN_COPY.md",
    "captures/CAPTURE_BACK_C64_WORKBENCH_THREAD_STATE.md",
    "captures/CAPTURE_BACK_C64_FIRST_CURRICULUM_BATCH.md",
]
errors=[]
for rel in REQUIRED_PATHS:
    if not (ROOT/rel).exists():
        errors.append(f"missing {rel}")
text=(ROOT/"docs/c64/first_curriculum_batch.md").read_text(errors='ignore') if (ROOT/"docs/c64/first_curriculum_batch.md").exists() else ''
for token in ["Lab 004", "Lab 005", "Lab 006", "Lab 007", "Lab 008", "Memory Pal"]:
    if token not in text:
        errors.append(f"first curriculum batch missing {token!r}")

ig = (ROOT / "docs/visuals/c64_workbench_stage0_learning_loop.md").read_text(errors="ignore") if (ROOT / "docs/visuals/c64_workbench_stage0_learning_loop.md").exists() else ""
for token in ["Stage 0", "VICE", "cc65", "Capture Back", "Hernan"]:
    if token not in ig:
        errors.append(f"C64 Stage 0 infographic doc missing {token!r}")

hernan = (ROOT / "docs/visuals/c64_workbench_stage0_learning_loop_for_hernan.md").read_text(errors="ignore") if (ROOT / "docs/visuals/c64_workbench_stage0_learning_loop_for_hernan.md").exists() else ""
for token in ["repeatable loop", "make verify", "cc65", ".prg", "VICE", "Capture Back", "re-enterable learning system"]:
    if token not in hernan:
        errors.append(f"C64 Hernan shareable copy missing {token!r}")

if errors:
    print('Missing or incomplete C64 Workbench files:')
    for e in errors: print('-', e)
    sys.exit(1)
print('OK: Commodore 64 Workbench domain, chatbot, thread-state, Learning Lab, and first curriculum layers are present.')
