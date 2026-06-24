# Start-Today Workbench Protocol

## Rule

Start-Today Workbench is a real Workbench operating mode.

It is not a lesser demo and should not be framed as merely primitive or obsolete.

It is the practical first surface for Workbench before dedicated software exists.

## Definition

Start-Today Workbench operates through:

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

## Role split

### Workbench role

The Workbench role governs the work.

It:

- decides what becomes durable;
- requests structure;
- holds continuity;
- reviews proposed Capture Back;
- approves, rejects, or revises;
- commits only after human review.

### II / Intelligence Interface role

The II role reasons and produces.

It:

- drafts outputs;
- proposes files and changes;
- generates Capture Back overlays;
- creates apply commands;
- diagnoses Terminal output;
- helps summarize Workbench history.

## Capture Back boundary

Capture Back moves accepted learning from chat into local Workbench repo memory.

It should include:

- files to add or update;
- an apply script;
- a Capture Back manifest;
- review summary;
- open-file list;
- verification guidance;
- suggested commit command.

## macOS workflow

The current practical workflow uses:

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

## Evidence loop

Terminal stdout should be pasted back into chat.

This gives the assistant actual repo evidence for:

- unzip results;
- apply script output;
- verification;
- pack;
- cleanup;
- `git status --short`;
- open-file errors;
- shell quoting or continuation prompt mistakes.

## Human approval

A successful apply is not approval.

The user reviews opened files first and then commits deliberately.

## History and re-entry

`make pack` regenerates repo history under:

```text
outputs/history/repo_history_for_llm_*.md
```

Future chats should read the latest pack or latest history before summarizing state or proposing the next Capture Back.

## One-line principle

Start-Today Workbench is the first practical Workbench surface: one chat window, two roles, local repo memory, terminal Capture Back, review surface, human commit, and history-based re-entry.
