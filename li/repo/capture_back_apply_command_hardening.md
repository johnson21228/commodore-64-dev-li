# Capture Back Apply Command Hardening

Capture Back overlays must be easy to apply from a fresh terminal and must fail closed when the downloaded zip does not match the generated instructions.

## Problem this prevents

A Capture Back overlay can be conceptually correct but mechanically flawed if the zip root folder name differs from the folder name used in the terminal command.

Example failure pattern:

```text
zip extracts to:      take60_latest_wb_support_overlay/
command expects:      take60_latest_workbench_support_overlay/
result:              cp fails, apply script is never copied, nothing applies
```

A second failure pattern occurs when the generated terminal command calls repo targets before the overlay creates or patches those targets.

Example:

```text
make verify
```

may be invalid before the overlay has added a `verify` target to an existing repo.

## Required rule

Every Capture Back overlay MUST be self-consistent:

- the zip root folder must exactly match the folder used in the apply command
- the apply script must exist at the copied repo root before it is executed
- the apply command must not call Makefile targets before the overlay creates or confirms them
- existing target repos may need `python3 tools/check_template_integrity.py` before `make verify`
- generated commands must fail closed if the expected folder or apply script is missing

## Preferred apply command shape

Use a stable overlay name and folder variable:

```bash
set -euo pipefail

REPO="/path/to/target/repo"
ZIP="$HOME/Downloads/example_overlay.zip"
WORKDIR="/tmp/example_overlay_apply"
ROOT="example_overlay"
SCRIPT="apply_example_overlay.py"

cd "$REPO"
rm -rf "$WORKDIR"
unzip -o "$ZIP" -d "$WORKDIR"

test -d "$WORKDIR/$ROOT" || { echo "Missing overlay root: $WORKDIR/$ROOT"; exit 1; }
test -f "$WORKDIR/$ROOT/$SCRIPT" || { echo "Missing apply script: $SCRIPT"; exit 1; }

cp -R "$WORKDIR/$ROOT"/* .
test -f "$SCRIPT" || { echo "Apply script was not copied to repo root"; exit 1; }

python3 "$SCRIPT"
python3 tools/check_template_integrity.py
make pack
git status
```

## Verification posture

For a mature template repo, `make verify` may be used after the overlay applies.

For an existing non-template repo, the safer first verification is:

```bash
python3 tools/check_template_integrity.py
make pack
git status
```

After the overlay patches or confirms a `verify` target, future loops may use:

```bash
make verify
make pack
git status
```

## Human meaning

This is a Capture Back quality rule. The continuity act can be correct while the delivery mechanism is flawed. The repo should remember both the concept and the mechanical guardrail so future overlays do not make the same mistake.
