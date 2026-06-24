# Workbench Prompt Index

## Purpose

This folder contains reusable prompts for operating, growing, reviewing, and capturing back a Workbench.

The prompt library is not just a list of files. It is a steering surface.

When you are unsure what to do next, ask:

```text
What Workbench prompt should I use next?
```

or:

```text
Given where this conversation is, which prompt in this repo should guide the next move?
```

The assistant should then route you to the right prompt.

---

# Quick steering language

Use these ordinary chat requests to move your Workbench conversation to the next level.

## Start a new Workbench

Use this when you have an idea, project, workflow, team, product, or domain that needs continuity.

```text
I want to start a new Workbench. Interview me and help define the repo.
```

Primary prompts:

- `01_interview_me_to_define_this_workbench.md`
- `00_create_a_workbench_li_repo.md`

Follow-on prompts:

- `02_generate_initial_repo_structure.md`
- `03_create_spine_and_readme.md`
- `04_create_first_continuity_cards.md`
- `05_create_first_source_context_map.md`
- `06_create_first_overlay_plan.md`

---

## Re-enter an existing Workbench

Use this when you are returning to an active Workbench and do not want the assistant to guess from stale chat memory.

```text
I am re-entering this Workbench. Ask me for the latest repo history file and summarize the current WB state.
```

Primary prompt:

- `request_workbench_cb_history.md`

Supporting prompts:

- `07_interpret_repo_history_briefly.md`
- `rejoin_unfinished_workbench_loop.md`

Power-user source file:

```text
outputs/history/repo_history_for_llm_*.md
```

If the latest history file does not exist, run:

```bash
make pack
```

Then upload the newest file from:

```text
outputs/history/
```

---

## Understand Workbench Capture Back history

Use this when you want to know what has been captured into the repo.

```text
Please summarize this Workbench's Capture Back history from the latest repo_history_for_llm_*.md file.
```

Primary prompt:

- `request_workbench_cb_history.md`

The assistant should focus on:

- cards;
- Capture Back manifests;
- LI rules;
- docs;
- prompts;
- notes;
- generated assets;
- open decisions;
- what should govern the next step.

---

## Capture Back an accepted lesson

Use this when a conversation produced something that should become durable repo memory.

```text
This should be captured back. Create a review-surfaced CB overlay.
```

Primary prompt:

- `capture_back_macos_terminal_apply_and_review.md`

Supporting prompts:

- `generate_capture_back_overlay_apply_command.md`
- `generate_hardened_capture_back_apply_command.md`
- `apply_overlay_terminal_workflow.md`
- `apply_command_fail_closed.md`
- `apply_command_fresh_terminal.md`
- `apply_command_generated_artifact_order.md`
- `capture_back_current_state_anti_drift_rule.md`

Expected current macOS apply rhythm:

```text
Download to Downloads.
Apply from repo root.
Paste stdout back to chat.
Review opened files.
Commit only after approval.
```

---

## Apply a Capture Back overlay on macOS

Use this when you already have an overlay zip and want the exact terminal workflow.

```text
Give me the macOS apply-and-review command block for this Capture Back overlay.
```

Primary prompt:

- `capture_back_macos_terminal_apply_and_review.md`

The command should usually include:

```bash
cd /Users/stevejohnson/Developer/<workbench-repo>

unzip -o ~/Downloads/<overlay>.zip -d .

python3 tools/<apply_script>.py

make verify
make pack

git status --short

open <primary_doc>
open <primary_li_rule>
open <primary_manifest_or_artifact>
```

---

## Compare a target Workbench to the current template

Use this when you have two packs:

1. current template WB pack;
2. target WB pack.

```text
Compare this target Workbench pack against the current template pack. Tell me what should move from template to target, and what the target might teach the template.
```

Primary prompt:

- `compare_target_workbench_against_template_pack.md`

This prompt should not generate an overlay immediately. It should first produce a comparison report and recommended plan.

---

## Generate a Start-Today Workbench explanation

Use this when you want the best current explanation of how Workbench operates today without a dedicated app.

```text
Generate the Start-Today Workbench guide with copy and an infographic.
```

Primary prompt:

- `visuals/generate_start_today_workbench_capture_back_guide.md`

Core framing:

```text
One chat window. Two roles. Local repo memory. Terminal-based Capture Back.
```

Important boundary:

Start-Today Workbench is not a lesser demo. It is the first practical Workbench surface.

---

## Generate Workbench visuals

Use this when you need a visual explanation.

```text
Generate an infographic that explains this Workbench pattern.
```

Visual prompts:

- `generate_simple_workbench_loop_infographic.md`
- `generate_workbench_build_loop_infographic.md`
- `generate_newcomer_workbench_loop_infographic.md`
- `generate_newcomer_multi_pack_workbench_loop_infographic.md`
- `visuals/generate_start_today_workbench_capture_back_guide.md`

Prefer the Start-Today prompt when explaining the current macOS Capture Back workflow.

---

## Clean up and pack a Workbench

Use this before sharing or uploading a Workbench pack.

```text
Help me review untracked files, clean up generated artifacts, verify, and pack this Workbench.
```

Primary prompts:

- `08_review_untracked_and_cleanup.md`
- `09_pack_and_share_this_workbench.md`

Useful command:

```bash
make verify
make pack
git status --short
```

---

## Evaluate a Workbench cleanly

Use this when you want a fresh read of a Workbench without relying on prior conversation.

```text
Evaluate this Workbench as if you are seeing it for the first time.
```

Primary prompt:

- `10_clean_room_evaluate_this_workbench.md`

---

## Convert an existing repo into a Workbench

Use this when you already have a repo and want to add Workbench LI structure.

```text
Help me convert this existing repo into a Workbench LI repo.
```

Primary prompt:

- `convert_existing_repo_to_workbench_li.md`

---

## Onboard a new team member

Use this when another person needs to understand the Workbench.

```text
Simulate onboarding a new team member to this Workbench.
```

Primary prompt:

- `simulate_new_team_member_onboarding.md`

Supporting prompt:

- `write_first_read_reaction_note.md`

---

## Decide how far to go in a Capture Back

Use this when you are not sure whether to stop at a proposal, generate an overlay, or provide manual edits.

```text
Help me choose the right Workbench completion mode for this change.
```

Primary prompt:

- `choose_workbench_completion_mode.md`

---

# Current guidance

## Do not remove prompts casually

Some prompts overlap because they encode hard-won workflow lessons:

- fail closed;
- use a fresh terminal;
- keep generated artifacts ordered;
- ask for current state before patching;
- open review artifacts;
- paste stdout back to chat;
- commit only after review.

Prefer an index first, then consolidation later.

## Ask for current state before making repo claims

When the active repo may have changed, the assistant should ask for current repo context.

For WB history, ask for:

```text
outputs/history/repo_history_for_llm_*.md
```

For full source inspection, ask for the latest repo pack.

## Best general next-level prompt

When unsure, use:

```text
Given this conversation and the current Workbench state, which prompt in this repo should guide the next move? Ask me for the latest repo_history_for_llm_*.md if you need current state before answering.
```
