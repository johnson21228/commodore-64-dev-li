# Card 004: Define C64 Learning Lab

## Intent

Promote the C64 Workbench from a general development repo into a Learning Lab: a sequence of small, runnable experiments that teach Commodore 64 machine concepts.

## Decision

The C64 Workbench now treats `C64 Learning Lab` as the primary project direction.

## Added LI

```text
li/domain/c64_learning_lab_principles.md
li/domain/lab_artifact_contract.md
docs/c64/learning_lab_project_setup.md
docs/c64/lab_sequence.md
docs/c64/emulator_review_workflow.md
docs/c64/c64_machine_concepts.md
source/c64/community_sources.md
```

## Added lab skeletons

```text
labs/001_hello_screen/
labs/002_screen_memory/
labs/003_color_memory/
```

## Verification

`tools/verify_c64_learning_lab.py` checks that the Learning Lab LI, first milestone files, and lab skeletons exist.

## Boundary

Do not claim that the lab examples have run locally until emulator evidence is captured.
