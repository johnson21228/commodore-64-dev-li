# Create a Continuity Card for a WB Loop

You are helping capture a completed or in-progress Workbench Loop as a continuity/work card.

Do not summarize every file mechanically. Capture the governed unit of work.

## Ask for

- the user's intent
- the relevant git status, diff, or commit output
- what decision was made
- what evidence validated the decision
- what remains next

## Produce

```markdown
# Card: [short title]

## Intent

[What the human was trying to accomplish.]

## Context

[Why this mattered. Include repo authority, product meaning, or workflow meaning.]

## Decision

[The judgment made by the human.]

## Execution

[Commands, files, commits, or overlays used.]

## Evidence

[Terminal output, tests, pack results, commit hash, or other proof.]

## Outcome

[What changed in the repo or workbench.]

## Next handoff

[What future human or LLM should do next.]
```

## Rule

If the git diff records the change but not the reasoning, the card should preserve the reasoning.
