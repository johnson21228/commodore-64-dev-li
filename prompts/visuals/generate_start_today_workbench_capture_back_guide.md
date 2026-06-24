# Prompt — Generate Start-Today Workbench / Stage 0 Capture Back Guide

Use this prompt to generate the current best-practice "Start-Today Workbench" explanation.

Important framing:

This is not customer-facing stage-path pitch language.

This is internal / educational Workbench adoption language. It explains how a user can operate Workbench today using one ChatGPT conversation, a local Workbench repo, and macOS Terminal.

Use "Start-Today Workbench" as the primary phrase.

You may reference "Stage 0" only as a secondary clarification:

> Stage 0 means the Workbench can already operate today without a dedicated app: one chat window, two roles, local repo memory, and terminal-based Capture Back.

## Goal

Generate a practical guide and infographic that explain the current best practice for operating a Workbench before a native product surface exists.

The guide should include:

1. short explanatory copy;
2. a high-quality infographic;
3. the macOS terminal workflow;
4. the Capture Back review surface;
5. the download-to-Downloads convention;
6. the paste-stdout-back-to-chat loop;
7. the commit-after-review boundary;
8. the WB Capture Back history / re-entry pattern.

## Core message

Workbench works today.

The first usable Workbench does not require a new application. It can operate through:

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

## Required headline

Use:

```text
Start-Today Workbench
```

Recommended subtitle:

```text
One chat window. Two roles. Local repo memory. Terminal-based Capture Back.
```

Optional supporting line:

```text
This is the practical Stage 0 Workbench: useful before any dedicated app, MCP endpoint, or native product surface exists.
```

## Copy requirements

Explain these concepts clearly:

### 1. One chat window, two roles

The same chat can alternate between:

**Workbench role**
- governs the work;
- decides what should become durable;
- asks for structure;
- reviews proposed Capture Back;
- approves, rejects, or revises;
- commits only after review.

**II role / Intelligence Interface role**
- reasons through the request;
- drafts outputs;
- proposes files and changes;
- generates Capture Back overlays;
- creates apply commands;
- diagnoses terminal output;
- helps summarize WB history.

### 2. Local repo memory

The Workbench repo is the durable memory layer.

It preserves cards, docs, LI rules, prompts, notes, source context, generated assets, history reports, and Capture Back manifests.

### 3. Capture Back overlay

A Capture Back overlay is the package that moves accepted learning from chat into the repo.

It should include files to add or update, an apply script, a Capture Back manifest, a review summary, an open-file list, verification guidance, and a suggested commit command.

### 4. macOS terminal workflow

Explain the standard apply pattern:

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

Explain why `~/Downloads` matters:

The command assumes the overlay zip is downloaded to the Mac Downloads folder. Do not rename it unless the command changes.

### 5. Paste stdout back to chat

Terminal output is evidence.

The user should paste the full output back into chat so the assistant can inspect unzip success, apply-script output, verification, pack, cleanup, `git status --short`, open-file errors, and quoting or continuation-prompt mistakes.

### 6. Human review gate

Successful apply is not approval.

The user reviews opened files first.

Then the user commits deliberately:

```bash
git add <changed-files>

git commit -m "<clear commit message>"

git status --short
```

### 7. WB history and re-entry

`make pack` regenerates repo history:

```text
outputs/history/repo_history_for_llm_*.md
```

Future chats should use the latest repo pack or latest history report before summarizing current state or proposing the next Capture Back.

Include this reusable prompt:

```text
I am re-entering this Workbench. Please read the latest repo pack or latest outputs/history/repo_history_for_llm_*.md before summarizing current state. Generate a WB Capture Back history summary by card, decision, files added, LI changes, prompts, notes, generated assets, and open implications.
```

## Infographic requirements

Generate a high-quality infographic titled:

```text
Start-Today Workbench
```

Subtitle:

```text
One chat window. Two roles. Local repo memory. Terminal-based Capture Back.
```

The infographic should visually show:

1. ChatGPT Review Surface;
2. Download Overlay;
3. Apply from Repo Root;
4. Review Surface;
5. Paste stdout back to chat;
6. Human Commit Gate;
7. Workbench Memory and Re-entry.

## Footer principle

Use this footer:

```text
Apply below. Review above. Commit only after human approval.
```

## Anti-drift rules

Do not make the visual look like a generic AI automation dashboard.

Do not imply the assistant commits automatically.

Do not hide the human review gate.

Do not make Stage 0 sound primitive or obsolete.

Do not use Stage 0 language for customer-facing solution pitches.

Make clear:

```text
Start-Today Workbench is already a real Workbench. It is the practical first surface before dedicated software.
```

## Deliverables

Return:

1. polished explanatory copy;
2. the infographic;
3. a short review checklist;
4. a suggested Capture Back file list if this output should be saved into a Workbench repo.
