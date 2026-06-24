# Choose Workbench Completion Mode

You are preparing a Workbench Apply Command.

Before writing the command, identify the completion mode.

## Mode 1: Existing repo Capture Back

Use when updating an existing Workbench repo.

Command shape:

```bash
set -euo pipefail

cd /path/to/repo

# unzip/copy overlay
# run apply script

make verify
make pack

git status
git add -A
git commit -m "<message>"

git status
```

Do not run `make pack` after the final commit.

## Mode 2: New repo creation

Use when creating a new repo from a seed zip.

Command shape:

```bash
set -euo pipefail

cd /parent/path

rm -rf <new-repo>
unzip -o ~/Downloads/<repo-seed>.zip -d /parent/path

cd /parent/path/<new-repo>

git init
git add -A
git commit -m "Create <repo>"

make verify
make pack

git status
git add -A
git commit -m "Finalize generated pack and history"

git status
```

Do not run `make pack` after the final generated-artifact commit.

## Mode 3: Source-first with generated-artifact closeout

Use when the human wants source changes and generated artifacts in separate commits.

Command shape:

```bash
set -euo pipefail

cd /path/to/repo

# apply overlay

make verify

git add -A
git commit -m "<source change>"

make pack

git add -A
git commit -m "Refresh generated pack and history"

git status
```

Do not run `make pack` after the final generated-artifact commit.

## Required explanation

Tell the user which mode you selected and why.

Explain that the command avoids running `make pack` after the final commit because `make pack` may create timestamped generated artifacts and dirty the working tree again.
