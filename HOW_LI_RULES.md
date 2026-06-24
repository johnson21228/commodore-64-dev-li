# How LI Rules This Workbench

Language Infrastructure is the repo's governing layer.

LI does not replace human judgment. It preserves the structure needed for humans and LLM reasoning models to reason coherently across time.

## LI role

LI defines:

- purpose
- authority
- workflow
- boundaries
- vocabulary
- acceptance rules
- generated artifact status
- handoff expectations

## Human role

The human/domain owner supplies intent, judgment, acceptance, and responsibility.

## LLM role

The LLM reasoning model helps interpret, draft, critique, summarize, and propose changes.

The LLM should not treat its own current chat context as durable authority. Durable residue belongs in the repo.

## Repo role

The repo is the continuity-bearing artifact.

Useful reasoning should move from chat into repo files, tests, cards, prompts, tools, commits, packs, or documented decisions.

## Generated artifact role

Generated artifacts are evidence only.

A generated pack, diagram, history file, summary, or output may help a reviewer understand the repo. It does not override governing LI.

## Operating loop

The Workbench grows through this repeated loop:

```text
latest pack → LLM reasoning → overlay → local execution → verify/test → commit → updated pack → repeat
```

## Rule of repair

If an output is wrong, repair the governing layer before regenerating the output.

Do not patch generated evidence and pretend the system is governed.
