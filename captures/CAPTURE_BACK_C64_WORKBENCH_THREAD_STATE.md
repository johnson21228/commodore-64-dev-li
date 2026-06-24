# Capture Back: C64 Workbench Thread State

## Trigger

The user asked to Capture Back everything discussed after creating the Commodore 64 Development Workbench from the Workbench LI template.

## What was created

A new Workbench LI repo was generated for Commodore 64 development using the Workbench template.

Working repo name:

```text
commodore-64-dev-li
```

Primary purpose:

```text
Preserve continuity for Commodore 64 development: toolchain setup, cross-development workflow, emulator validation, hardware claims, application brainstorms, and future build sessions.
```

## Template-derived baseline

The Workbench keeps the template governance surface:

```text
LLM_READ_FIRST.md
SPINE.md
MAP.md
README.md
HOW_LI_RULES.md
Makefile
tools/check_template_integrity.py
tools/verify_li_governance.py
tools/export_repo_history_for_llm.py
tools/clean_li_repo_artifacts.py
```

The expected local loop remains:

```bash
make verify
make pack
git status --short
```

## C64-specific additions

The C64 domain layer covers:

- cross-development on a modern Mac;
- C64 constraints and source authority;
- emulator-first / hardware-later validation;
- toolchain options such as cc65, VICE, Kick Assembler, and C64 Studio;
- starter C64 examples;
- prompts for first project definition, hello world, sprite/charset experiments, emulator review, and Capture Back.

Important files:

```text
li/domain/c64_development_principles.md
li/domain/cross_development_model.md
li/domain/emulator_first_hardware_later.md
li/domain/c64_constraints.md
li/domain/toolchain_source_authority.md
source/c64/toolchain_source_map.md
docs/c64/first_session_c64_hello_world.md
docs/c64/toolchain_options.md
docs/c64/workbench_loop_for_c64_development.md
examples/hello-cc65/
examples/kickasm-smoke/
tools/verify_c64_workbench.py
```

## First application brainstorm

The first product/application direction captured during the conversation is:

```text
C64 MEMORY PAL
```

This is a C64 Hello Console that can grow into an ELIZA-style rule-based chatbot.

The Workbench distinction is important:

1. **Native C64 chatbot**: feasible as a rule-based, ELIZA-style text program.
2. **C64 as chatbot terminal**: feasible later, with the C64 acting as the front-end and a modern host or LLM doing richer reasoning.
3. **Hybrid staged path**: recommended. Start native and honest, then bridge outward only after the C64 build/run loop is proven.

The Workbench must not claim that a C64 is running a modern LLM natively.

## Local apply troubleshooting captured

A first apply command failed because it attempted to enter:

```text
/Users/stevejohnson/Developer/commodore-64-dev-li
```

before the shell had confirmed the repo location.

The follow-up terminal session showed that the folder did exist under:

```text
/Users/stevejohnson/Developer/commodore-64-dev-li
```

but the base pack file was not present in Downloads:

```text
~/Downloads/commodore-64-dev-li.pack.zip
```

The right operational lesson is:

- do not assume the pack zip is still in Downloads;
- if the repo folder exists, work with the existing folder first;
- verify with `pwd`, `ls -la`, `make verify`, and `make pack`;
- only apply an overlay after confirming the repo root.

## Safe re-entry command

Use this to resume from a fresh Terminal:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li

pwd
ls -la

make verify
make pack

git status --short
```

Then check whether the chatbot brainstorm already landed:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li

ls docs/c64 | grep application_brainstorm_chatbot
ls prompts | grep c64_brainstorm_first_application
ls cards | grep 002_brainstorm
ls captures | grep C64_APPLICATION_BRAINSTORM_CHATBOT
```

## Next likely CB

The next useful Capture Back should create a `C64 MEMORY PAL v0` implementation card.

Target outcome:

- one native C64 source path;
- one reproducible build command;
- one `.prg` artifact under `artifacts/` or `work/` after build;
- one emulator observation captured back;
- no hardware claim unless real hardware is actually tested.
