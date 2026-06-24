# Generated Artifact Commit Order

## Purpose

This LI captures a Workbench loop lesson learned while creating a new repo from the starter template.

Some Workbench repos track generated artifacts such as:

- `dist/*.pack.zip`
- `outputs/history/repo_history_for_llm_*.md`

When `make pack` runs, it may create a new timestamped history artifact and rebuild the pack. If `make pack` is run after the final commit, the working tree may become dirty again.

## Problem

A naive Apply Command can do this:

```text
apply overlay
→ verify
→ pack
→ commit
→ pack again
→ working tree becomes dirty again
```

The final `make pack` may generate a new history artifact and update the pack after the commit.

That creates friction:

```text
the repo is verified
the repo is packed
the repo is committed
but final git status is not clean
```

## Rule

A Workbench Apply Command must respect generated artifact commit order.

If generated artifacts are tracked, the command must choose one of these patterns.

## Pattern A: Commit after pack, then stop

Use this when the generated pack/history should be included in the same commit as the source changes.

```text
apply overlay
→ verify
→ pack
→ git add -A
→ git commit
→ git status
```

Do not run `make pack` again after the commit.

## Pattern B: Two-commit generated artifact closeout

Use this when a source commit should happen before the final generated pack/history.

```text
apply overlay
→ verify
→ git add -A
→ git commit source changes
→ make pack
→ git add -A
→ git commit generated pack/history
→ git status
```

Do not run `make pack` again after the generated-artifact commit.

## Anti-pattern

Do not create an Apply Command that ends with:

```text
git commit
→ make pack
→ git status dirty
```

unless the command also commits the generated artifacts and stops.

## Fail-closed requirement

If verification fails, stop before commit.

If pack generation fails, stop before commit.

If the final status is dirty, either commit the generated artifact closeout or explicitly report why the dirty state is intentional.

## Completion modes

This file is extended by:

```text
li/repo/completion_modes.md
```

## Preferred default

For most Workbench LI changes, prefer Pattern A:

```text
apply overlay
→ make verify
→ make pack
→ git add -A
→ git commit
→ git status
```

This keeps the command simple and avoids a post-commit `make pack` that dirties the tree.

## Capture Back lesson

This rule exists because a real Workbench loop revealed the problem.

The Workbench Consulting repo creation generated a clean repo, then `make pack` after commit created a newer history artifact and updated the pack, requiring an extra commit.

That friction should now be prevented by the starter template.
