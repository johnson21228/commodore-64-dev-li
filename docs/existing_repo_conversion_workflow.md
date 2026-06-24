# Existing Repo → Workbench LI Conversion Workflow

## Purpose

This workflow governs the case where a user has an existing repository pack and wants to transfer the Workbench structure into it.

The goal is not to clone the template into the repo.

The goal is to add enough Workbench LI to preserve continuity, source authority, cards, verification, history, cleanup, and pack behavior while preserving the repo's existing purpose.

## When to use

Use this when the user says things like:

```text
Can we turn this repo into a Workbench?
Can you transfer the WB structure to this existing repo pack?
Can you add the WB loop to this project?
Can you make this repo follow the template?
```

Primary prompt:

```text
prompts/convert_existing_repo_to_workbench_li.md
```

Related prompt for already-Workbench targets:

```text
prompts/compare_target_workbench_against_template_pack.md
```

## Distinction from two-pack comparison

Use `convert_existing_repo_to_workbench_li.md` when the target repo is not yet a Workbench or is missing the core WB layer.

Use `compare_target_workbench_against_template_pack.md` when the target is already a Workbench and the question is template synchronization.

## Conversion rule

Preserve the repo first.

Add the narrowest governing layer that makes the repo re-enterable by LLMs and humans.

Do not perform product refactors, broad source moves, or style rewrites as part of initial conversion.

## Expected Capture Back shape

A good conversion Capture Back usually includes:

- `LLM_READ_FIRST.md`
- `MAP.md`
- `HOW_LI_RULES.md`
- `SPINE.md`
- core LI files under `li/`
- first continuity card under `cards/`
- repo history / cleanup / verify / pack tooling under `tools/`
- Makefile targets for `verify`, `history`, `clean-li`, and `pack`
- `.gitkeep` files for generated output folders
- an apply script that prints review surfaces and suggested verification

## Human boundary

The assistant may produce the overlay and terminal command.

The human applies it, reviews opened files, runs verification, and commits only after accepting the change.
