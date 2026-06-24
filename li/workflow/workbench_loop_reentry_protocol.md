# Workbench Loop Re-entry Protocol

A Workbench Loop is sometimes interrupted. Re-entry is a first-class workflow, not an exception.

The purpose of re-entry is to recover focus, preserve human custody, and finish the active loop without mixing unrelated changes.

## Promise

When returning to an unfinished loop, the Workbench should help the human answer:

1. What repo am I in?
2. What branch am I on?
3. What loop was I trying to finish?
4. What was the intended Capture Back?
5. What files belong to this loop?
6. What files do not belong to this loop?
7. What verifier should run before staging?
8. What should be staged narrowly?
9. What commit message closes the loop?
10. What final pack/status command confirms completion?

## Buckets

Classify the working tree before staging:

```text
A. Intended loop changes
B. Unrelated product/runtime changes
C. Generated artifacts
D. Overlay/apply cruft
E. Unknown / inspect before staging
```

## Rules

- Do not use `git add -A` unless the working tree contains only intended loop changes.
- Prefer narrow staging lists.
- Do not mix generic Workbench-support changes with product/runtime changes.
- Do not assume `make verify` exists unless the repo already has it or the overlay has successfully added it.
- Prefer the most specific verifier first.
- Preserve product-specific meaning when applying generic template support.
- Close the loop with a commit, then repack and inspect status.

## Re-entry command posture

A safe re-entry usually begins with:

```bash
pwd
git branch --show-current
git status
git diff --stat
```

If an overlay was involved, include recent terminal output from unzip/apply/verify/pack.

## Completion posture

A re-entered loop is not finished until:

```bash
make pack
git status
```

has been run, and any remaining changes have been classified as either separate work or expected local generated output.
