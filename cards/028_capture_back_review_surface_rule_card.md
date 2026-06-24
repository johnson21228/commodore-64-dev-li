# Card 028 — Capture Back Review Surface Rule

## Status

Proposed / ready for Capture Back.

## Claim

Capture Back should not feel like a blind file mutation. Every generated overlay should make the human review surface obvious immediately after apply.

## Decision

Add a repo/template rule: Capture Back overlays should include an apply script and/or terminal command block that:

1. applies the bounded change;
2. updates navigation references when appropriate;
3. prints a concise review summary;
4. names the files added or changed;
5. identifies the primary review artifacts;
6. opens the most important review files for the human;
7. preserves verification and pack commands after apply.

## Why this matters

Workbench is a governed workflow. The repo changes below, but the human reviews above.

A Capture Back that silently writes files makes the user hunt for what changed. A good Capture Back turns the accepted proposal into a visible review sequence:

- what was added;
- why it was added;
- what to inspect;
- what to verify;
- what to commit.

## Review standard

A Capture Back overlay is not complete unless a future user can answer:

- What changed?
- Why did it change?
- What files should I inspect first?
- Which artifacts are generated evidence?
- What command verifies the repo?
- What command packs the repo?
- What should I commit if accepted?

## Related files

- `li/repo/capture_back_review_surface_rule.md`
- `docs/capture_back_review_surface.md`
- `prompts/generate_capture_back_overlay_apply_command.md`
- `prompts/apply_overlay_terminal_workflow.md`
- `source/templates/capture_back_apply_script_template.py`
- `notes/capture_back_review_surface_lesson.md`
