#!/usr/bin/env python3
from pathlib import Path

REQUIRED = [
    "li/domain/c64_learning_lab_principles.md",
    "li/domain/lab_artifact_contract.md",
    "docs/c64/learning_lab_project_setup.md",
    "docs/c64/lab_sequence.md",
    "docs/c64/emulator_review_workflow.md",
    "docs/c64/c64_machine_concepts.md",
    "docs/c64/hello_world_app.md",
    "prompts/c64_run_hello_world_lab.md",
    "cards/005_c64_hello_world_app_card.md",
    "captures/CAPTURE_BACK_C64_HELLO_WORLD_APP.md",
    "docs/c64/screen_memory_app.md",
    "prompts/c64_run_screen_memory_lab.md",
    "cards/006_c64_screen_memory_app_card.md",
    "captures/CAPTURE_BACK_C64_SCREEN_MEMORY_APP.md",
    "docs/c64/color_memory_app.md",
    "prompts/c64_run_color_memory_lab.md",
    "cards/007_c64_color_memory_app_card.md",
    "captures/CAPTURE_BACK_C64_COLOR_MEMORY_APP.md",
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
    "docs/c64/hello_world_app.md": ["make lab001", "HELLO, WORLD!", "generated `.prg` artifacts are evidence"],
    "labs/001_hello_screen/src/main.c": ["HELLO, WORLD!", "cputsxy", "cgetc"],
    "labs/001_hello_screen/README.md": ["make lab001", "x64sc", "HELLO, WORLD!"],
    "captures/CAPTURE_BACK_C64_HELLO_WORLD_APP.md": ["Hello World", "edit source -> build .prg -> run in VICE"],
    "docs/c64/screen_memory_app.md": ["$0400", "SCREEN[0]", "make lab002", "generated code can touch the C64 machine model directly"],
    "labs/002_screen_memory/src/main.c": ["0x0400", "SCREEN[0]", "ROW 10 COL 5 IS OFFSET 405", "while (1)"],
    "labs/002_screen_memory/README.md": ["make lab002", "x64sc", "SCREEN[0]", "$0400"],
    "captures/CAPTURE_BACK_C64_SCREEN_MEMORY_APP.md": ["Lab 002: Screen Memory", "C64 screen RAM starts at $0400", "make lab002-run"],
    "docs/c64/color_memory_app.md": ["$D800", "COLOR[0]", "make lab003", "Writing to $0400 changes what character is displayed"],
    "labs/003_color_memory/src/main.c": ["0xD800", "COLOR[0]", "SCREEN[0]", "CLOSE EMULATOR TO END", "while (1)"],
    "labs/003_color_memory/README.md": ["make lab003", "x64sc", "COLOR[0]", "$D800"],
    "captures/CAPTURE_BACK_C64_COLOR_MEMORY_APP.md": ["Lab 003", "C64 color RAM starts at $D800", "make lab003-run"],
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

    if "lab001:" not in makefile or "lab001-run:" not in makefile:
        print("Makefile must include lab001 and lab001-run shortcuts for the Hello World app")
        return 1

    if "lab002:" not in makefile or "lab002-run:" not in makefile:
        print("Makefile must include lab002 and lab002-run shortcuts for the Screen Memory app")
        return 1

    if "lab003:" not in makefile or "lab003-run:" not in makefile:
        print("Makefile must include lab003 and lab003-run shortcuts for the Color Memory app")
        return 1

    print("OK: C64 Learning Lab LI, Hello World app, Screen Memory app, and Color Memory app are present.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
