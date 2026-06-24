# Rejoin an Unfinished Workbench Loop

I am returning to an unfinished Workbench Loop.

Help me re-enter the loop safely, recover focus, and finish without mixing unrelated changes.

## Goal

Re-anchor the current repo state, identify the active loop, separate intended changes from unrelated residue, and give me a narrow path to close the loop.

Preserve the Workbench promise:

- durable continuity
- human custody
- small verified steps
- no accidental mixing of product/runtime changes with Workbench-support changes
- no `git add -A` unless the working tree contains only intended loop changes

## Required input from me

I will paste:

```bash
pwd
git branch --show-current
git status
git diff --stat
```

If relevant, I will also paste recent terminal output from the overlay/apply/pack step.

## Ask or determine

1. What repo am I in?
2. What branch am I on?
3. What loop was I trying to finish?
4. What was the intended Capture Back?
5. What files or changes belong to this loop?
6. What files or changes do not belong to this loop?
7. What verification should run before staging?
8. What should be staged narrowly?
9. What commit message should close the loop?
10. What final pack/status command confirms completion?

## Output

Give me:

1. A short re-entry diagnosis.
2. A classification of changes into buckets:

```text
A. Intended loop changes
B. Unrelated product/runtime changes
C. Generated artifacts
D. Overlay/apply cruft
E. Unknown / inspect before staging
```

3. The safest verification command.
4. A narrow `git add` command for only the intended loop.
5. The commit command.
6. The final pack/status commands.
7. A warning about anything that should not be mixed into the commit.

## Rules

Do not tell me to use `git add -A` unless the working tree is clean except for the intended loop.

Do not overwrite product-specific meaning with generic template material.

Do not assume `make verify` exists unless the repo already has it or the overlay has successfully added it.

Prefer specific verifier commands first, such as:

```bash
python3 tools/check_template_integrity.py
```

Then use:

```bash
make pack
git status
```

## Current loop context

[Describe the loop here in one sentence.]

Example:

```text
I am finishing the loop to bring latest generic Workbench support from the template into Take60, without mixing existing Take60 runtime/app-code edits.
```
