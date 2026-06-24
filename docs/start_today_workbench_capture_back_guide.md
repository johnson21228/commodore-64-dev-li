# Start-Today Workbench Capture Back Guide

## Purpose

This guide explains the current best-practice Start-Today Workbench pattern.

A Workbench does not require a dedicated application to begin working.

It can operate today through one chat window, two roles, a local repo, macOS Terminal, and Capture Back.

## Core message

Workbench works today.

The first usable Workbench can operate through:

- one ChatGPT conversation;
- two roles inside that conversation;
- a local Workbench repo;
- generated Capture Back overlays;
- macOS Terminal apply commands;
- verification and pack;
- opened review files;
- pasted Terminal stdout;
- deliberate human commit;
- generated repo history for future re-entry.

## One chat window, two roles

The same chat can alternate between two roles.

### Workbench role

The Workbench role governs the work.

It:

- decides what should become durable;
- asks for structure;
- holds continuity;
- reviews proposed Capture Back;
- approves, rejects, or revises;
- commits only after review.

### II role / Intelligence Interface role

The II role reasons and produces.

It:

- reasons through the request;
- drafts outputs;
- proposes files and changes;
- generates Capture Back overlays;
- creates apply commands;
- diagnoses Terminal output;
- helps summarize WB history.

## Local repo memory

The Workbench repo is the durable memory layer.

It preserves:

- cards;
- docs;
- LI rules;
- prompts;
- notes;
- source context;
- generated assets;
- history reports;
- Capture Back manifests.

## Capture Back overlay

A Capture Back overlay moves accepted learning from chat into the repo.

It should include:

- files to add or update;
- an apply script;
- a Capture Back manifest;
- review summary;
- open-file list;
- verification guidance;
- suggested commit command.

## macOS Terminal workflow

Standard apply pattern:

```bash
cd /Users/stevejohnson/Developer/<workbench-repo>

unzip -o ~/Downloads/<capture-back-overlay>.zip -d .

python3 tools/<apply_script>.py

make verify
make pack

git status --short

open <primary_doc>
open <primary_li_rule>
open <primary_manifest_or_artifact>
```

## Why Downloads matters

The command assumes the overlay zip is downloaded to the Mac Downloads folder:

```text
~/Downloads
```

Do not rename the overlay unless the command changes.

## Paste stdout back to chat

Terminal output is evidence.

The user should paste the full output back into chat so the assistant can inspect:

- unzip success;
- apply-script output;
- verification;
- pack;
- cleanup;
- `git status --short`;
- open-file errors;
- quoting or continuation-prompt mistakes.

## Human review gate

Successful apply is not approval.

The user reviews opened files first.

Then the user commits deliberately:

```bash
git add <changed-files>

git commit -m "<clear commit message>"

git status --short
```

## WB history and re-entry

`make pack` regenerates repo history:

```text
outputs/history/repo_history_for_llm_*.md
```

Future chats should use the latest repo pack or latest history report before summarizing current state or proposing the next Capture Back.

## Re-entry prompt

```text
I am re-entering this Workbench. Please read the latest repo pack or latest outputs/history/repo_history_for_llm_*.md before summarizing current state. Generate a WB Capture Back history summary by card, decision, files added, LI changes, prompts, notes, generated assets, and open implications.
```

## Footer principle

Apply below. Review above. Commit only after human approval.
