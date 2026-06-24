# Apply Command Fail-Closed Prompt

You are producing an Apply Command for a Workbench LI repo.

The command must fail closed.

## Required instruction to user

Before the command, say:

```text
Open a new terminal window, paste this whole block, and copy the complete output back into this chat. The command is designed to stop if verification fails, so we do not accidentally commit a broken repo state.
```

## Required command behavior

The command MUST start with:

```bash
set -euo pipefail
```

The command should then:

1. `cd` into the target repo.
2. unzip the overlay into a temporary apply directory.
3. copy the overlay contents into the repo.
4. run the apply script.
5. run `make verify`.
6. run `make pack`.
7. show `git status`.
8. run `git add -A`.
9. run `git commit -m "..."`
10. show final `git status`.

Do not run `make pack` after the final commit unless the command also commits the generated pack/history and stops.

## Failure behavior

If any step fails, the shell should stop.

Do not continue to pack or commit after failure.

Do not create a command that dirties the working tree after the final commit by running `make pack` again.

Ask the user to paste the terminal output back into chat so the issue can be diagnosed.
