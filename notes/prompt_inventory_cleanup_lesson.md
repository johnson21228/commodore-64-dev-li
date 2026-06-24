# Prompt Inventory Cleanup Lesson

## Lesson

The template now has enough prompts that the prompt folder needs a visible operating index.

The right first cleanup is not deletion. It is steering.

## Captured insight

Users should be able to ask ordinary chat-language questions and be routed to the right prompt:

- I want to start a new Workbench.
- I am re-entering this Workbench.
- What has been captured back?
- This should be captured back.
- Compare this target WB to the current template.
- Generate the Start-Today Workbench guide.
- Help me clean up and pack.
- Help a new team member understand this WB.

## Power-user history behavior

For Workbench history, the assistant should ask for the latest:

```text
outputs/history/repo_history_for_llm_*.md
```

first.

The full pack is useful when source inspection is needed, but the history file is the fastest, most direct source for WB Capture Back history.

## Product implication

The prompt folder is becoming a command surface. Its README should help the user take the current conversation to the next level.

## One-line formulation

The prompt library should steer the user from ordinary chat language to the right Workbench protocol.
