#!/usr/bin/env python3
from pathlib import Path

REQUIRED = [
    "li/domain/c64_learning_lab_principles.md",
    "li/domain/lab_artifact_contract.md",
    "docs/c64/learning_lab_project_setup.md",
    "docs/c64/lab_sequence.md",
    "docs/c64/emulator_review_workflow.md",
    "docs/c64/c64_machine_concepts.md",
    "source/c64/community_sources.md",
    "prompts/c64_define_learning_lab_li.md",
    "prompts/c64_build_next_learning_lab.md",
    "prompts/c64_capture_learning_lab_evidence.md",
    "prompts/c64_research_project_idea_corpus.md",
    "cards/004_define_c64_learning_lab_card.md",
    "captures/CAPTURE_BACK_C64_LEARNING_LAB_PROJECT_SETUP.md",
    "labs/001_hello_screen/README.md",
    "labs/001_hello_screen/expected.md",
    "labs/001_hello_screen/Makefile",
    "labs/001_hello_screen/src/main.c",
    "labs/002_screen_memory/README.md",
    "labs/002_screen_memory/expected.md",
    "labs/002_screen_memory/Makefile",
    "labs/002_screen_memory/src/main.c",
    "labs/003_color_memory/README.md",
    "labs/003_color_memory/expected.md",
    "labs/003_color_memory/Makefile",
    "labs/003_color_memory/src/main.c",
]

TOKENS = {
    "SPINE.md": ["C64 Learning Lab", "concept truth -> tiny runnable program -> emulator evidence"],
    "MAP.md": ["li/domain/c64_learning_lab_principles.md", "tools/verify_c64_learning_lab.py", "labs/001_hello_screen/"],
    "README.md": ["C64 Learning Lab", "make verify-learning-lab"],
    "li/domain/c64_learning_lab_principles.md": ["concept truth -> tiny program -> emulator run -> observed evidence -> Capture Back"],
    "li/domain/lab_artifact_contract.md": ["README.md", "expected.md", "src/", "Makefile"],
    "docs/c64/learning_lab_project_setup.md": ["Bracket Builder analogy", "Take60 analogy", "Grazing / Registry analogy"],
    "docs/c64/lab_sequence.md": ["Lab 001: Hello Screen", "Lab 009: Online Gateway"],
    "captures/CAPTURE_BACK_C64_LEARNING_LAB_PROJECT_SETUP.md": ["C64 Learning Lab", "Memory Pal", "Online Gateway"],
}


def main() -> int:
    missing = [path for path in REQUIRED if not Path(path).exists()]
    if missing:
        print("Missing C64 Learning Lab files:")
        for path in missing:
            print(f"- {path}")
        return 1

    for path, tokens in TOKENS.items():
        text = Path(path).read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                print(f"{path} missing required Learning Lab token: {token}")
                return 1

    makefile = Path("Makefile").read_text(encoding="utf-8")
    if "verify-learning-lab" not in makefile or "tools/verify_c64_learning_lab.py" not in makefile:
        print("Makefile must include verify-learning-lab and run tools/verify_c64_learning_lab.py")
        return 1

    print("OK: C64 Learning Lab LI and first lab skeletons are present.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
