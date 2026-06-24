# Fail-Closed Apply Command

## Purpose

This LI defines the required safety behavior for Workbench Apply Commands.

## Rule

A Workbench Apply Command MUST fail closed.

If apply, verification, tests, cleanup, packing, or any required step fails, the command must stop before commit.

## Required shell behavior

Apply Commands SHOULD start with:

```bash
set -euo pipefail
```

At minimum, they MUST use:

```bash
set -e
```

## Why

The Workbench loop is only trustworthy if broken changes are not accidentally packed and committed.

The intended loop is:

```text
apply overlay
→ verify
→ if verification fails, stop
→ repair before commit
→ commit only after verification passes
→ repack
```

The loop must not be:

```text
apply overlay
→ verification fails
→ pack anyway
→ commit anyway
→ repair later
```

## Commit rule

Do not run `git add`, `git commit`, or final `make pack` after a failed verification step.

A commit should mean the repo reached an accepted, verified state.

## LLM behavior

When producing an Apply Command, the LLM should:

1. tell the user to open a fresh terminal window
2. include `set -euo pipefail`
3. run apply
4. run `make verify`
5. run `make pack`
6. show `git status`
7. commit only after verification and packing succeed
8. repack after commit
9. show final `git status`

It must also respect generated artifact commit order and choose the appropriate Workbench completion mode. If `make pack` creates tracked artifacts, do not run `make pack` after the final commit unless the command also commits those generated artifacts and stops.

If the user pastes a failure, the LLM should diagnose the failure and produce a corrected overlay or repair command before continuing.

## Human behavior

If the command stops, the human should paste the full terminal output back into chat.

The stop is not a failure of the Workbench. It is the Workbench protecting itself.

## Authority

Fail-closed behavior is part of repo governance.

No workflow convenience should override it.

See also:

```text
li/repo/generated_artifact_commit_order.md
li/repo/completion_modes.md
```
