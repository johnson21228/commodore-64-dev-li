# Apply Command Fresh Terminal Prompt

You are producing an Apply Command for a Workbench LI repo.

Write the command so the user can open a new terminal window, paste the whole block, run it, and copy the complete output back into chat.

## Requirements

The command must start with `set -euo pipefail` and should:

1. `cd` into the target repo.
2. unzip the overlay from `~/Downloads`.
3. run the apply script.
4. run verification.
5. run packing.
6. show `git status`.
7. commit only if the user explicitly asked to commit.
8. repack after commit when useful.
9. finish with `git status`.

## User-facing instruction

Before the command, say:

```text
Open a new terminal window, paste this whole block, then copy the complete terminal output back into this chat.
```

## Reason

A fresh terminal window creates a clean execution trace for the LLM reasoning model to inspect until the repo is stable. The command should stop on failure so broken states are not packed and committed.
