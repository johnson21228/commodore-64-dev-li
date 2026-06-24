# Capture-back lesson: WB loop card pattern

A Workbench Loop should use a card pattern when the work is more than a file edit.

The Take60 legacy app-specific LI removal showed why. The git commit recorded the mechanical change: many files deleted. But the important meaning was not obvious from the diff alone.

The real unit of work included:

- intent
- authority clarification
- risk of accidental interpretation
- human judgment
- terminal evidence
- commit evidence
- follow-on work
- future handoff

A continuity/work card captures this custody layer.

## Rule of thumb

If a future reader or LLM could misunderstand a git diff without the surrounding judgment, create a card.

## What the card preserves

- why the work was done
- what authority changed
- what risk was considered
- what evidence validated the action
- what remains to do
- what should be handed off to the next WB loop

Git records the change. The card records the governed work.
