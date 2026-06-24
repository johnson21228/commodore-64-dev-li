# Repository History Pattern

## Purpose

Repository history artifacts help an LLM briefly interpret how a repo has evolved without requiring a full pack every time.

## Pattern

Repository history artifacts are generated locally on demand.

They live under:

```text
outputs/history/repo_history_for_llm_*.md
```

They are generated evidence, not authority.

## Rules

- History artifacts are not hand-authored authority.
- They should be ignored by git unless the repo intentionally tracks a specific one.
- `make pack` SHOULD generate a fresh history artifact.
- Cleanup SHOULD remove stale history artifacts and preserve only the latest useful one.
- Prompts should ask the user to upload the latest history artifact before asking for a full pack when a brief interpretation is enough.

## Why

This keeps LLM review token-lean while preserving enough continuity to understand recent change.
