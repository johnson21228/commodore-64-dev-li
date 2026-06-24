# Source Context Map

## Purpose

This LI defines how a Workbench should map the material it relies on.

A Workbench should not treat every file as equally authoritative.

## Source categories

Use these categories when mapping material:

- authoritative
- current
- provisional
- historical
- illustrative
- generated
- external
- rejected
- unknown

## Minimum fields

A source-context map SHOULD record:

- source name
- location
- authority level
- why it matters
- how fresh it is
- what it governs
- known limitations
- related optional continuity notes

## Rule

When the LLM reasons from source material, it should identify the source category and avoid promoting provisional or generated material into authority.
