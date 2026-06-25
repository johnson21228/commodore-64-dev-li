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
if errors:
    print('Missing or incomplete C64 Workbench files:')
    for e in errors: print('-', e)
    sys.exit(1)
print('OK: Commodore 64 Workbench domain, chatbot, thread-state, Learning Lab, and first curriculum layers are present.')
