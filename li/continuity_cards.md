# Continuity Cards

A continuity card is the Workbench LI unit of work.

It binds:

- human intent
- governing authority/context
- LLM reasoning
- execution/change
- validation evidence
- outcome
- future handoff

GitHub Issues may be used as a container, but the deeper unit is the continuity card.

## Card trigger: when git diff is not enough

Create a continuity/work card when a WB loop contains judgment that would be hard to reconstruct from `git diff` alone.

Strong triggers include:

- authority changes
- cleanup that could look accidental
- deletion or migration of important context
- repo structure changes
- generated artifact decisions
- validation or evidence that matters later
- follow-on work that should not be lost
- handoff to a future human or LLM

A git commit records what changed. A card records why the change was governed, what evidence was used, and what should happen next.
