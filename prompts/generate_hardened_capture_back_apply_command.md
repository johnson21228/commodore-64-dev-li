# Generate a Hardened Capture Back Overlay Apply Command

Generate terminal commands for applying a Capture Back overlay.

The command must not assume the extracted root folder name.

## Required variables

Use:

```bash
REPO="/path/to/target/repo"
ZIP="$HOME/Downloads/<overlay>.zip"
WORKDIR="/tmp/<overlay>_apply"
SCRIPT="apply_<overlay>.py"
```

Do not require a `ROOT=...` variable.

## Required command pattern

```bash
set -euo pipefail

REPO="/path/to/target/repo"
ZIP="$HOME/Downloads/<overlay>.zip"
WORKDIR="/tmp/<overlay>_apply"
SCRIPT="apply_<overlay>.py"

cd "$REPO"
rm -rf "$WORKDIR"
unzip -o "$ZIP" -d "$WORKDIR"

EXTRACTED_ROOT="$(find "$WORKDIR" -mindepth 1 -maxdepth 1 -type d | head -1)"
test -n "$EXTRACTED_ROOT" || { echo "No extracted overlay root found"; exit 1; }
test -f "$EXTRACTED_ROOT/$SCRIPT" || { echo "Missing apply script: $SCRIPT"; exit 1; }

cp -R "$EXTRACTED_ROOT"/* .
test -f "$SCRIPT" || { echo "Apply script was not copied to repo root"; exit 1; }

python3 "$SCRIPT"

if test -f tools/check_template_integrity.py; then
  python3 tools/check_template_integrity.py
fi

make pack
git status
```

## Rules

- Do not hardcode the extracted overlay root folder name.
- Do not call `make verify` unless the target repo is known to have that target before apply, or the apply script has already created it and the command is being run after apply.
- Prefer the narrow verifier first.
- Use `make pack` and `git status` after apply.
- Warn the user not to use `git add -A` if unrelated changes are already present.
