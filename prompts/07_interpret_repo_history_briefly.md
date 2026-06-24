# Interpret Repository History Briefly

You are reviewing a repository history artifact created for LLM reasoning.

Your task is to provide a brief interpretation only.

Do not provide a full technical audit unless the user asks for it.

## Input expected

Ask the user to upload the latest repository history artifact only.

Do not ask for the full repo pack unless the history artifact is missing or insufficient.

Expected file pattern:

```text
outputs/history/repo_history_for_llm_*.md
```

## What to explain

1. What the main sequence of changes appears to be.
2. What changed last.
3. What the repository seems to be becoming.
4. What the most important overall shift was.
5. Whether the repo history looks coherent.
6. Whether there are obvious cleanup or sharing concerns.

Keep the response short, candid, and interpretive.
