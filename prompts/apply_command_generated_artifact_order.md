# Apply Command Generated Artifact Order Prompt

You are producing a fail-closed Apply Command for a Workbench LI repo.

First choose the Workbench completion mode from `prompts/choose_workbench_completion_mode.md`.

Generated artifacts may be tracked, including:

```text
dist/*.pack.zip
outputs/history/repo_history_for_llm_*.md
```

## Required behavior

The command must avoid creating a dirty working tree after the final commit.

## Default pattern

Prefer this pattern:

```bash
set -euo pipefail

cd /path/to/repo

unzip -o ~/Downloads/<overlay>.zip -d /tmp/<overlay>_apply
cp -R /tmp/<overlay>_apply/<overlay-folder>/* .

python3 apply_<overlay>.py

make verify
make pack

git status
git add -A
git commit -m "<message>"

git status
```

Do not run `make pack` again after this commit.

## Alternative pattern

If the user explicitly wants a source commit followed by generated artifacts:

```bash
set -euo pipefail

cd /path/to/repo

# apply overlay...

make verify

git status
git add -A
git commit -m "<source change message>"

make pack

git status
git add -A
git commit -m "<generated artifact message>"

git status
```

Do not run `make pack` again after the generated-artifact commit.

## Explanation to include

Tell the user:

```text
This command intentionally does not run `make pack` after the final commit, because `make pack` creates timestamped generated artifacts and can dirty the working tree again.
```

## Failure behavior

The command must stop on failure using:

```bash
set -euo pipefail
```

If verification fails, do not continue to pack or commit.

If pack generation fails, do not commit.

Ask the user to paste the full terminal output back into chat.
