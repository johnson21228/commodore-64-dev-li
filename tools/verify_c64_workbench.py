#!/usr/bin/env python3
from pathlib import Path

REQUIRED = [
    "li/domain/c64_development_principles.md",
    "li/domain/cross_development_model.md",
    "li/domain/emulator_first_hardware_later.md",
    "li/domain/c64_constraints.md",
    "li/domain/toolchain_source_authority.md",
    "li/domain/c64_learning_lab_principles.md",
    "li/domain/lab_artifact_contract.md",
    "source/c64/toolchain_source_map.md",
    "source/c64/community_sources.md",
    "docs/c64/first_session_c64_hello_world.md",
    "docs/c64/toolchain_options.md",
    "docs/c64/workbench_loop_for_c64_development.md",
    "docs/c64/application_brainstorm_chatbot.md",
    "docs/c64/thread_state_and_local_apply_notes.md",
    "docs/c64/learning_lab_project_setup.md",
    "prompts/c64_interview_me_to_define_first_project.md",
    "prompts/c64_create_first_hello_world.md",
    "prompts/c64_design_sprite_or_charset_experiment.md",
    "prompts/c64_capture_back_dev_session.md",
    "prompts/c64_review_emulator_evidence.md",
    "prompts/c64_brainstorm_first_application.md",
    "prompts/c64_rejoin_thread_and_continue.md",
    "cards/001_start_commodore_64_development_workbench_card.md",
    "cards/002_brainstorm_c64_first_application_chatbot_card.md",
    "cards/003_capture_c64_thread_state_card.md",
    "cards/004_define_c64_learning_lab_card.md",
    "captures/CAPTURE_BACK_C64_APPLICATION_BRAINSTORM_CHATBOT.md",
    "captures/CAPTURE_BACK_C64_WORKBENCH_THREAD_STATE.md",
    "captures/CAPTURE_BACK_C64_LEARNING_LAB_PROJECT_SETUP.md",
    "examples/hello-cc65/hello.c",
    "examples/hello-cc65/Makefile",
    "tools/verify_c64_learning_lab.py",
]

TOKENS = {
    "SPINE.md": ["Commodore 64", "cross-development", "C64 MEMORY PAL", "must not claim that a C64 is running an LLM natively", "C64 Learning Lab"],
    "MAP.md": ["li/domain/c64_development_principles.md", "tools/verify_c64_workbench.py", "tools/verify_c64_learning_lab.py"],
    "README.md": ["Commodore 64 Development Workbench", "make verify", "C64 Learning Lab"],
    "source/c64/toolchain_source_map.md": ["cc65", "VICE", "Kick Assembler", "C64 Studio"],
    "li/domain/emulator_first_hardware_later.md": ["Do not move directly from generated code to real-hardware claims"],
    "docs/c64/application_brainstorm_chatbot.md": ["C64 MEMORY PAL", "ELIZA-style", "C64 as chatbot terminal"],
    "prompts/c64_brainstorm_first_application.md": ["native rule-based C64 chatbot", "modern host chatbot"],
    "docs/c64/learning_lab_project_setup.md": ["C64 Learning Lab", "Bracket Builder analogy", "Take60 analogy"],
}


def main() -> int:
    missing = [path for path in REQUIRED if not Path(path).exists()]
    if missing:
        print("Missing C64 Workbench files:")
        for path in missing:
            print(f"- {path}")
        return 1

    for path, tokens in TOKENS.items():
        text = Path(path).read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                print(f"{path} missing required C64 token: {token}")
                return 1

    makefile = Path("Makefile").read_text(encoding="utf-8")
    required = [
        "verify-c64",
        "verify-learning-lab",
        "tools/verify_c64_workbench.py",
        "tools/verify_c64_learning_lab.py",
    ]
    for token in required:
        if token not in makefile:
            print(f"Makefile missing required C64 verification token: {token}")
            return 1

    print("OK: Commodore 64 Workbench domain, chatbot, thread-state, and Learning Lab layers are present.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
