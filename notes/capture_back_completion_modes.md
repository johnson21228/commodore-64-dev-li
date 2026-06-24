# Capture Back Note: Completion Modes

## What was learned

Creating the Workbench Consulting repo revealed that Workbench loops need different completion modes.

An existing repo update and a new repo creation do not have the same commit order.

## Lesson

The template should support:

1. existing repo Capture Back
2. new repo creation
3. source-first with generated-artifact closeout

## Why

`make pack` may create timestamped generated artifacts.

If `make pack` runs after the final commit, the repo may become dirty again.

## Captured back into template

This is captured in:

```text
li/repo/completion_modes.md
prompts/choose_workbench_completion_mode.md
```
