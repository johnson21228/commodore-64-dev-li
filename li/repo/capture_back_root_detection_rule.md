# Capture Back Root Detection Rule

Capture Back apply commands must not depend on a manually guessed extracted folder name.

A prior failure showed this class of bug:

```text
zip extracted root: wb_loop_reentry_protocol_overlay
command expected: workbench_loop_reentry_protocol_overlay
```

The conceptual Capture Back was correct, but the apply command failed because the shell command hardcoded the wrong root.

## Rule

When generating a Capture Back overlay apply command:

1. Unzip into a clean temporary working directory.
2. Detect the single extracted root directory.
3. Verify the expected apply script exists inside that detected root.
4. Copy from the detected root into the repo.
5. Verify the apply script exists at the repo root.
6. Run the apply script.
7. Run the narrow verifier.
8. Pack.
9. Show `git status`.

## Required command posture

Use root detection:

```bash
EXTRACTED_ROOT="$(find "$WORKDIR" -mindepth 1 -maxdepth 1 -type d | head -1)"
test -n "$EXTRACTED_ROOT" || { echo "No extracted overlay root found"; exit 1; }
test -f "$EXTRACTED_ROOT/$SCRIPT" || { echo "Missing apply script: $SCRIPT"; exit 1; }
cp -R "$EXTRACTED_ROOT"/* .
```

Do not require the human to manually keep the zip root name and command root name synchronized.

Capture Back must be mechanically boring.
