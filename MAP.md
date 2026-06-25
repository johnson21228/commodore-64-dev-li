# Commodore 64 Development Workbench LI Map

This map orients humans and LLM reasoning models inside the Commodore 64 Development Workbench.

## Repository purpose

This repository is a Workbench LI repo for Commodore 64 development. It keeps the general Workbench template governance and adds domain LI for C64 software work.

## Required read-first files

Before changing this repo, read:

```text
LLM_READ_FIRST.md
HOW_LI_RULES.md
SPINE.md
li/workflow/workbench_build_loop.md
li/workflow/visible_workflow_outcome_contract.md
```

For C64 work, also read:

```text
li/domain/c64_development_principles.md
li/domain/cross_development_model.md
li/domain/emulator_first_hardware_later.md
li/domain/c64_constraints.md
li/domain/toolchain_source_authority.md
source/c64/toolchain_source_map.md
```

## C64 source authority

```text
source/c64/toolchain_source_map.md
```

This file names the initial external toolchain references and explains how to treat them. It is not a substitute for checking current official docs before installing or changing tools.

## C64 docs

```text
docs/c64/first_session_c64_hello_world.md
docs/c64/toolchain_options.md
docs/c64/workbench_loop_for_c64_development.md
docs/c64/application_brainstorm_chatbot.md
```


## C64 Learning Lab

The primary project direction is now:

```text
C64 Learning Lab
```

Learning Lab read-first files:

```text
li/domain/c64_learning_lab_principles.md
li/domain/lab_artifact_contract.md
docs/c64/learning_lab_project_setup.md
docs/c64/lab_sequence.md
docs/c64/emulator_review_workflow.md
docs/c64/c64_machine_concepts.md
docs/c64/hello_world_app.md
source/c64/community_sources.md
```

First lab skeletons:

```text
labs/001_hello_screen/
labs/002_screen_memory/
labs/003_color_memory/
```

Learning Lab prompts:

```text
prompts/c64_define_learning_lab_li.md
prompts/c64_build_next_learning_lab.md
prompts/c64_capture_learning_lab_evidence.md
prompts/c64_research_project_idea_corpus.md
```

Learning Lab verification lives at:

```text
tools/verify_c64_learning_lab.py
```

## C64 prompts

```text
prompts/c64_interview_me_to_define_first_project.md
prompts/c64_create_first_hello_world.md
prompts/c64_design_sprite_or_charset_experiment.md
prompts/c64_capture_back_dev_session.md
prompts/c64_review_emulator_evidence.md
prompts/c64_brainstorm_first_application.md
```

## C64 examples

```text
examples/hello-cc65/
examples/kickasm-smoke/
```

Examples are starter material. They are not authoritative until built and validated in the user's environment.

## Template governance

Core governing LI remains under:

```text
li/core/
li/workflow/
li/repo/
li/source/
```

Important template tools remain:

```text
tools/check_template_integrity.py
tools/verify_li_governance.py
tools/export_repo_history_for_llm.py
tools/clean_li_repo_artifacts.py
```

C64 domain verification lives at:

```text
tools/verify_c64_workbench.py
```

## Makefile targets

```text
make verify
make verify-li
make verify-c64
make history
make clean-li
make pack
make read-first
```

## Generated artifact boundary

Generated artifacts are evidence only. Build outputs, emulator screenshots, `.prg` files, disk images, and logs should be placed under `work/` or `artifacts/` only when intentionally curated. They do not govern the repo.

## C64 Learning Lab 002: Screen Memory

- `docs/c64/screen_memory_app.md` — Lab 002 runnable screen-memory app notes.
- `prompts/c64_run_screen_memory_lab.md` — prompt for building/running Lab 002 and capturing emulator evidence.
- `cards/006_c64_screen_memory_app_card.md` — continuity card for the Lab 002 app.
- `captures/CAPTURE_BACK_C64_SCREEN_MEMORY_APP.md` — Capture Back for the Lab 002 screen-memory code example.
- `labs/002_screen_memory/` — runnable direct screen-memory code example.

## C64 Learning Lab 003: Color Memory

- `docs/c64/color_memory_app.md` — Lab 003 runnable color-memory app notes.
- `prompts/c64_run_color_memory_lab.md` — prompt for building/running Lab 003 and capturing emulator evidence.
- `cards/007_c64_color_memory_app_card.md` — continuity card for the Lab 003 app.
- `captures/CAPTURE_BACK_C64_COLOR_MEMORY_APP.md` — Capture Back for the Lab 003 color-memory code example.
- `labs/003_color_memory/` — runnable direct screen/color memory code example.
