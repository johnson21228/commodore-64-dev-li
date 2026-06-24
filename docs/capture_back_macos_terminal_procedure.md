# Capture Back on macOS: Terminal Review Procedure

## Purpose

This document explains the practical Capture Back workflow for a Workbench repo when using ChatGPT and macOS Terminal.

Capture Back is the step where accepted learning, decisions, artifacts, rules, prompts, notes, or generated assets are written back into the local Workbench repo.

The goal is not blind automation.

The goal is:

> Apply below. Review above. Commit only after human approval.

The assistant may generate a Capture Back overlay. The human downloads it, applies it locally, reviews the result, verifies the repo, and commits only after acceptance.

## The basic loop

1. Discuss work in chat.
2. Decide what should be preserved.
3. Ask chat to generate a Capture Back overlay.
4. Download the overlay zip to the Mac Downloads folder.
5. Run the apply commands from Terminal.
6. Paste Terminal output back into chat.
7. Let chat inspect success or errors.
8. Review opened files.
9. Commit only if accepted.
10. Ask chat for WB CB history when re-entering later.

## Why the Downloads folder matters

The standard apply commands assume the overlay zip is in:

```bash
~/Downloads/
```

For example:

```bash
unzip -o ~/Downloads/workbench-li-template-review-surface-cb-overlay.zip -d .
```

This works because macOS expands `~` to the current user's home folder, and most browser/chat downloads go to the Downloads folder by default.

If the file is not in Downloads, the unzip command will fail.

The download pattern is therefore part of the protocol:

1. Click the overlay download link from chat.
2. Let the file download to `~/Downloads`.
3. Do not rename it unless the command is also updated.
4. Run the exact terminal command from the repo root.

## Start from the repo root

Before applying a Capture Back overlay, change into the correct local repo.

Example:

```bash
cd /Users/stevejohnson/Developer/workbench-li-template
```

or:

```bash
cd /Users/stevejohnson/Developer/workbench-product-builder-li
```

The repo root is the folder that contains files like:

```text
README.md
MAP.md
Makefile
cards/
docs/
li/
prompts/
tools/
```

If you apply an overlay from the wrong folder, files may be written to the wrong place.

## Standard apply command pattern

A good Capture Back command block usually looks like this:

```bash
cd /Users/stevejohnson/Developer/<repo-name>

unzip -o ~/Downloads/<capture-back-overlay>.zip -d .

python3 tools/<apply-script>.py

make verify
make pack

git status --short

open <primary-doc>
open <primary-li-rule>
open <primary-manifest-or-artifact>
```

Each step has a purpose.

## What each step does

### 1. `cd`

Moves Terminal into the correct repo.

### 2. `unzip`

Expands the overlay into the repo.

```bash
unzip -o ~/Downloads/<overlay>.zip -d .
```

The `-o` flag allows files in the overlay to overwrite earlier versions if needed.

The `-d .` means extract into the current directory.

### 3. `python3 tools/<apply-script>.py`

Runs the overlay apply script.

The apply script may:

- patch `MAP.md`;
- patch `README.md`;
- patch `WORKBENCH_REFERENCE.md`, if present;
- print a review summary;
- list added or updated files;
- identify what to inspect next.

The apply script should not commit.

### 4. `make verify`

Runs repo checks.

This should confirm that the Workbench structure is still valid.

### 5. `make pack`

Creates a fresh pack zip and usually regenerates repo history.

This matters because later chat sessions can use the pack or history report to understand the current repo.

### 6. `git status --short`

Shows what changed.

This is the human review boundary. The output should match the expected Capture Back.

### 7. `open`

Opens the key review files on macOS.

Examples:

```bash
open docs/capture_back_review_surface.md
open li/repo/capture_back_review_surface_rule.md
open CAPTURE_BACK_REVIEW_SURFACE_RULE.md
```

For Python files, macOS may not know which app to use. If `open` fails, use:

```bash
open -a TextEdit source/templates/capture_back_apply_script_template.py
```

## Paste Terminal output back into chat

After running the apply block, paste the full Terminal output back into chat.

Chat can then help determine:

- Did the unzip succeed?
- Did the apply script run?
- Did verification pass?
- Did packing complete?
- Did `git status --short` show the expected files?
- Did any `open` command fail harmlessly?
- Is the commit command correct?
- Should anything be repaired before commit?

This is important because Terminal output is the evidence trail.

Do not summarize it manually if there was an error. Paste the raw output.

## If an error occurs

Do not guess.

Paste the Terminal output back into chat and ask:

```text
What happened, and what should I run next?
```

Common errors include:

- overlay zip not in Downloads;
- command run from the wrong repo folder;
- Markdown fences accidentally pasted into Terminal;
- Terminal stuck at `bquote>` because a fenced block or quote marker was pasted;
- missing apply script;
- verification failure;
- generated file opened with the wrong app.

If Terminal is stuck at a continuation prompt such as:

```text
bquote>
```

press:

```text
Control-C
```

Then run a clean command without Markdown fences.

## Commit only after review

A successful apply is not the same as approval.

Review the opened files first.

Then commit deliberately.

Typical commit command:

```bash
git add <changed-files>

git commit -m "<clear commit message>"

git status --short
```

The final `git status --short` should be clean or should show only known uncommitted work.

## How to ask chat for WB CB history

When re-entering a Workbench later, ask chat to use the latest repo context before making claims.

Good prompts:

```text
I am re-entering this Workbench. Please read the latest repo pack or latest outputs/history/repo_history_for_llm_*.md before summarizing current state.
```

```text
Generate a WB CB history summary from the latest repo history. Focus on cards, Capture Back manifests, LI changes, docs, prompts, generated assets, and open decisions.
```

```text
What has been captured back in this Workbench so far? Please summarize the CB history by card number, decision, files added, and current implications.
```

```text
Before proposing the next Capture Back, inspect the latest repo history and tell me what the current Workbench already knows.
```

## What the history report is for

The repo history report is generated by:

```bash
make pack
```

or directly by:

```bash
python3 tools/export_repo_history_for_llm.py
```

It writes a file like:

```text
outputs/history/repo_history_for_llm_YYYYMMDD-HHMMSS_<hash>.md
```

That file helps chat re-enter the repo without relying on stale conversation memory.

It is especially useful when:

- a new chat begins;
- several overlays have been applied;
- repo state may have changed;
- the user wants a CB history;
- the assistant needs to avoid guessing.

## The intended human rhythm

The rhythm should feel like this:

```text
Chat proposes.
Human downloads.
Terminal applies.
Repo verifies.
Files open.
Human reviews.
Terminal output returns to chat.
Chat diagnoses.
Human commits.
History preserves.
Next chat re-enters smarter.
```

That is the current macOS Capture Back protocol.

The future product may automate more of this. For now, the terminal workflow is a clear, inspectable, human-owned bridge between chat reasoning and local repo memory.
