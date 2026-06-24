# Capture Back macOS Terminal Protocol

## Rule

For the current macOS Workbench workflow, Capture Back is a human-operated protocol that moves accepted chat learning into local repo memory through a downloaded overlay, Terminal apply commands, verification, review, and deliberate commit.

## Required protocol

When using a generated Capture Back overlay on macOS:

1. Download the overlay zip from chat to `~/Downloads`.
2. Do not rename the zip unless the terminal command is also changed.
3. Open a fresh Terminal window when possible.
4. `cd` into the correct Workbench repo root.
5. Unzip the overlay into the repo.
6. Run the overlay apply script.
7. Run verification.
8. Run pack generation.
9. Inspect `git status --short`.
10. Open the primary review artifacts.
11. Paste Terminal stdout back into chat.
12. Let chat diagnose errors or confirm success from actual repo evidence.
13. Commit only after human review and approval.
14. Use generated repo history for future re-entry.

## Downloads folder convention

The standard command assumes the overlay is in:

```bash
~/Downloads/
```

Example:

```bash
unzip -o ~/Downloads/<capture-back-overlay>.zip -d .
```

This convention makes the chat-generated command stable and easy to reuse.

If the file is not in Downloads, the command will fail. Either move the file to Downloads or update the path.

## Repo-root requirement

The command must run from the Workbench repo root.

The repo root usually contains:

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

Running the command from the wrong directory can place overlay files in the wrong location.

## Terminal stdout as evidence

Raw Terminal output is part of the review surface.

After applying an overlay, paste the full output back into chat. This allows the assistant to inspect:

- unzip results;
- apply script output;
- verification results;
- pack results;
- cleanup messages;
- `git status --short`;
- open-file errors;
- shell quoting or continuation prompt mistakes.

Do not rely on memory or paraphrase when an error occurs.

## Commit boundary

A successful apply is not the same as approval.

The apply script should not commit.

Human review comes first. Commit only after the user accepts the change.

## History and re-entry

`make pack` should regenerate the repo history report, usually under:

```text
outputs/history/repo_history_for_llm_*.md
```

Future chats should use the latest pack or latest history report before summarizing current Workbench state or proposing the next Capture Back.

## One-line principle

Download to Downloads. Apply from repo root. Paste stdout back to chat. Review opened files. Commit only after approval.
