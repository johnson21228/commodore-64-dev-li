# Card 033 — Capture prompt inventory and next-level prompt steering

## Status

Proposed / ready for Capture Back.

## Claim

The template Workbench now has enough prompts that the prompt folder needs a visible index and steering language.

The user should be able to ask, in ordinary chat language:

> What prompt should I use next?

and be guided to the right Workbench prompt for the next level of work.

## Decision

Add a prominent `prompts/README.md` that inventories the current prompt set by use case and includes plain chat language for steering the user to the right prompt.

Also strengthen `prompts/request_workbench_cb_history.md` so the first request is for the latest:

```text
outputs/history/repo_history_for_llm_*.md
```

not raw git history and not the full pack unless needed.

## Why this matters

A growing prompt library can become confusing.

Workbench prompts should not feel like a drawer full of files. They should feel like a guided operating surface.

The README should help a user move from ordinary language to the right prompt:

- “I want to start a new WB.”
- “I am re-entering a WB.”
- “I want to Capture Back this lesson.”
- “I want to compare this WB to the current template.”
- “I want to generate the Start-Today Workbench explanation.”
- “I want to clean up before packing.”
- “I want a new team member to understand this WB.”

## Review standard

The prompt README should:

- organize prompts by job-to-be-done;
- highlight the primary prompt for each job;
- include copyable chat language;
- point power users to the latest repo history file for WB history;
- avoid deleting or renaming prompts in this Capture Back;
- set up future consolidation without breaking current workflows.

## Related files

- `prompts/README.md`
- `prompts/request_workbench_cb_history.md`
- `notes/prompt_inventory_cleanup_lesson.md`
- `CAPTURE_BACK_PROMPT_INVENTORY_CLEANUP.md`
