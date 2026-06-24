# Workbench Completion Modes

## Purpose

This LI defines how a Workbench loop reaches a clean, trustworthy stopping point.

A Workbench loop is complete only when:

```text
verification passed
pack is current
intended changes are committed
git status is clean
no final command regenerates tracked artifacts after the last commit
```

## Why completion modes are needed

Some Workbench repos track generated artifacts:

```text
dist/*.pack.zip
outputs/history/repo_history_for_llm_*.md
```

Running `make pack` creates a new timestamped history artifact and rebuilds the pack.

Therefore, running `make pack` after the final commit can make the working tree dirty again.

## Mode 1: Existing repo Capture Back

Use this when applying an overlay to an existing Workbench repo.

Recommended order:

```text
apply overlay
→ make verify
→ make pack
→ git add -A
→ git commit
→ git status
```

Do not run `make pack` again after the final commit.

The pack and latest history artifact are included in the commit.

## Mode 2: New repo creation

Use this when creating a new Workbench repo from a zipped seed or generated repo.

Recommended order:

```text
unzip new repo
→ git init
→ git add -A
→ git commit initial repo
→ make verify
→ make pack
→ git add -A
→ git commit generated pack/history
→ git status
```

Do not run `make pack` again after the generated-artifact closeout commit.

## Mode 3: Source-first with generated-artifact closeout

Use this when the human wants a clean source-change commit before generated artifacts.

Recommended order:

```text
apply overlay
→ make verify
→ git add -A
→ git commit source changes
→ make pack
→ git add -A
→ git commit generated pack/history
→ git status
```

Do not run `make pack` again after the generated-artifact closeout commit.

## LLM rule

Before producing an Apply Command, the LLM should identify which completion mode applies:

```text
existing repo Capture Back
new repo creation
source-first with generated-artifact closeout
```

If unclear, default to existing repo Capture Back for an already-initialized repo.
