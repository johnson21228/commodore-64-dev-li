# Capture Back Review Surface Rule

## Rule

Every Capture Back overlay should create an immediate human review surface.

The overlay may add, modify, or package files, but it must not leave the reviewer guessing what happened. The apply workflow should surface the important results immediately.

## Required behavior

A Capture Back overlay should include one or more of the following:

1. **Apply script**
   - Applies bounded navigation/reference updates.
   - Prints a concise review summary.
   - Lists the key files added or changed.
   - Names the primary review artifacts.

2. **Terminal command block**
   - Applies the overlay.
   - Runs verification.
   - Runs pack generation.
   - Opens the key review files.

3. **Capture Back manifest**
   - Explains the intent, files, review checklist, and commit suggestion.

## Preferred apply-script output

After an overlay applies, the script should print something like:

```text
Capture Back applied: <short title>

Added / updated:
- <file>: <why it matters>
- <file>: <why it matters>

Review next:
- <primary doc>
- <primary artifact>
- <primary LI rule>

Suggested verification:
- make verify
- make pack

Commit if accepted:
- git add ...
- git commit -m "<message>"
```

## Preferred command block pattern

The assistant should provide an apply command block that ends by opening key artifacts:

```bash
cd /path/to/repo

unzip -o ~/Downloads/<overlay>.zip -d .

python3 tools/<apply_script>.py

make verify
make pack

git status --short

open <primary_doc>
open <primary_rule>
open <primary_generated_artifact>
```

## Review hierarchy

Open only the most important review files by default. Too many opened files can create noise.

Recommended order:

1. primary human-readable doc;
2. governing LI rule;
3. generated artifact, if any;
4. source prompt or template, if it is important to inspect;
5. Capture Back manifest.

## Human custody

The script may apply safe reference patches and print summary information, but it should not commit changes.

Committing remains a human approval step.

## Anti-patterns

Avoid:

- silent overlays with no review summary;
- commands that only unzip and verify but do not open review artifacts;
- opening every changed file;
- hiding generated assets in folders without a README or doc reference;
- treating a successful script run as approval.

## One-line principle

Apply below. Review above. Commit only after human approval.
