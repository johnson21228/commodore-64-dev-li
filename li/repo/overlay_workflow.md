# Overlay Workflow

## Purpose

This LI defines how chat reasoning becomes durable repo change.

## Pattern

```text
LLM reasoning → downloadable overlay → local terminal execution → verification → commit → pack
```

## Overlay contents

An overlay SHOULD include:

- files to add or replace
- a narrow apply script when useful
- instructions
- no unrelated refactors
- no hidden destructive actions

## Terminal command

The model SHOULD provide a copyable terminal command that fails closed and:

1. starts with `set -euo pipefail`
2. changes into the target repo
2. unzips the overlay
3. runs the apply script
4. runs verification/tests
5. runs `make pack`
6. shows `git status`
7. commits only after verification and packing succeed, and only when appropriate and explicitly requested

## Rule

The overlay is the bridge from reasoning to repo.

The repo, not the chat, becomes the durable record.

## Fresh terminal window convention

A Workbench Apply Command SHOULD normally be run in a new terminal window.

This gives the human and LLM reasoning model a clean, copyable terminal trace from overlay application through verification, packing, commit, and final status.

See:

```text
li/repo/fresh_terminal_apply_command.md
```
