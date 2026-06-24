# Capture Back Review Surface

## Purpose

This document describes the preferred Capture Back apply experience.

The goal is not only to mutate the repo. The goal is to make the change immediately reviewable.

Workbench should preserve the distinction:

> The repo is changed below. The human reviews above.

## Why this exists

Earlier overlays often worked technically but required the user to hunt through the repo to understand what changed.

The improved pattern makes the overlay self-surfacing:

- the apply script prints what was added;
- the terminal command opens the primary files;
- the user sees the governing rule, the document, and any generated artifact immediately;
- the user can decide whether to commit.

## Standard overlay experience

A strong Capture Back should include:

1. A bounded overlay zip.
2. An apply script under `tools/`.
3. A Capture Back manifest at the repo root.
4. A card describing the decision.
5. Any LI, docs, prompts, source templates, notes, or assets needed.
6. A terminal command block that:
   - unzips the overlay;
   - runs the apply script;
   - runs verification;
   - packs the repo;
   - shows git status;
   - opens the review artifacts.

## Standard apply summary

The apply script should print a summary like:

```text
Capture Back applied: Review Surface Rule

Added:
- li/repo/capture_back_review_surface_rule.md
- docs/capture_back_review_surface.md
- prompts/generate_capture_back_overlay_apply_command.md
- source/templates/capture_back_apply_script_template.py

Review next:
- docs/capture_back_review_surface.md
- li/repo/capture_back_review_surface_rule.md
- CAPTURE_BACK_REVIEW_SURFACE_RULE.md
```

## What should open automatically

Prefer opening:

- one governing LI rule;
- one explanatory doc;
- one generated artifact, if the overlay includes an artifact;
- one source prompt/template only if it is central to future reuse.

Do not open every file. The summary can list the rest.

## Commit remains separate

The apply script should not run `git commit`.

The user should review first, then commit explicitly.

Suggested commit line should be included in the assistant response or the manifest.
