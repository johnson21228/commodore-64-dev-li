# Workbench Build Loop LI

## Purpose

This LI defines the repeated workflow used to build, preserve, and improve Workbench continuity.

A Workbench is a git repository of Language Infrastructure. The repository is the durable authority surface. The LLM reasoning model is a temporary reasoning partner. The pack is the portable compacted form of the Workbench used to begin the next reasoning session.

## Governing principle

Workbench continuity is built through a repeated human-in-the-loop cycle:

```text
repo LI → pack zip → LLM reasoning session → Capture Back → local apply → verification → commit → new pack → next session
```

The loop exists so useful reasoning does not remain trapped in chat. It must leave durable residue in the repository as LI, prompts, tools, tests, cards, outputs, or documented decisions.

## Required loop

Every Workbench build cycle SHOULD follow this sequence.

### 1. Start from the current pack

The user adds the latest Workbench pack zip to a chat with an LLM reasoning model.

The pack is the compacted form of the current repo LI. It gives the model context without requiring the entire local repo.

The user prompts the model with the Workbench goal.

Example:

```text
Here is the current Workbench pack. My goal is to improve the starter template so every new Workbench begins with the governed build loop.
```

### 2. Reason with the model

The user and model interact until the desired change is clear enough to make durable.

The model may interpret, critique, propose, or draft, but the human remains the authority for intent and judgment.

### 3. Capture Back

When the reasoning has ripened, the user asks the model to help capture useful reasoning, decisions, context, evidence, and continuity back into the repo.

Capture Back SHOULD result in a narrow, reviewable repo change. The delivery may use a downloadable overlay, an apply script, direct file edits, or another safe local mechanism.

A Capture Back change SHOULD include:

- files to add or replace
- narrow changes only
- an apply script when useful
- terminal commands for applying, verifying, packing, committing, and reporting status

The model SHOULD also provide a copyable terminal command block designed to run from the local machine.

### 4. Execute locally

The user downloads the Capture Back change to the Downloads folder when a downloadable artifact is used.

The user runs the terminal command.

The terminal command SHOULD fail closed and:

- start with `set -euo pipefail`
- unpack or place the change into the target repo when needed
- apply the change
- run verification and tests
- run `make pack`
- show `git status`
- commit the changes when appropriate
- show the final pack path

The user copies terminal output back into the chat until the command sequence completes cleanly. If verification fails, the command should stop before commit and the user should paste the failure output back into chat.

### 5. Repeat with the updated pack

The newly generated pack becomes the starting context for the next LLM reasoning session.

This creates an intentional continuity loop:

```text
current pack → reasoning → Capture Back → repo change → verified commit → updated pack
```

## Required properties

A compliant Workbench loop MUST preserve these properties:

1. Human intent remains primary.
2. The repo is the continuity authority.
3. The LLM is a reasoning partner, not the system of record.
4. Generated artifacts are evidence, not authority.
5. Changes are applied locally and verified before claims are made.
6. The pack is regenerated after meaningful changes.
7. The next chat starts from the latest pack, not stale context.

## Non-goals

This loop does not require the LLM to have direct repo access.

This loop does not require GitHub Issues to be the unit of work.

This loop does not treat chat as durable memory.

This loop does not allow generated output to outrank governing LI.

## Relationship to optional continuity notes

A continuity note may be created when extra human-readable handoff context is useful.

A note is optional. The Workbench loop does not require a card or note.

The primary durable record remains the repo: LI, source files, verification output, commits, history artifacts, and packs.

## Relationship to overlays

Overlay remains a useful implementation word for a downloadable patch bundle or technical delivery mechanism.

Do not use Overlay as the conceptual name of the Workbench Loop step. The conceptual step is Capture Back.

## Starter requirement

Every Workbench starter/template SHOULD include this file or an equivalent governing LI file before it is considered complete.

## Fresh terminal apply convention

When the user asks for an Apply Command, the LLM SHOULD tell the user to open a new terminal window, paste the whole command block, and copy the complete output back into the chat.

This keeps the reasoning loop focused until the repo is verified, packed, committed when intended, and stable.

See:

```text
li/repo/fresh_terminal_apply_command.md
```

## High-level loop relationship

For first-impression communication and simple infographics, use:

```text
li/workflow/high_level_workbench_loop.md
```

The high-level loop is:

```text
Pack → Reason → Capture Back → Verify → Commit + Repack → Repeat
```

This file remains the more detailed operational workflow.

## Current-state anti-drift rule

```text
No Capture Back without current state.
```

Steps 3, 4, and 5 must force current-state grounding:

- Capture Back must inspect the current target Workbench state before patching.
- Verify must prove the change fits the current state and does not drift.
- Commit + Repack must make the verified state the next reasoning baseline.

Short form:

```text
Reason from the current Workbench.
Capture Back into the current Workbench.
Verify before the Workbench remembers.
```
