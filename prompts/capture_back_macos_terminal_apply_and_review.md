# Prompt — Capture Back macOS Terminal Apply and Review

Use this prompt when asking chat to produce or review a macOS Capture Back apply workflow.

## Prompt

I want to Capture Back this accepted change into the Workbench repo using the macOS terminal workflow.

Please provide:

1. a downloadable overlay zip;
2. an apply command block that assumes the zip is in `~/Downloads`;
3. commands that run from the repo root;
4. `unzip -o`;
5. the overlay apply script command;
6. `make verify`;
7. `make pack`;
8. `git status --short`;
9. `open` commands for the primary review artifacts;
10. a commit command only after review.

Also include a short explanation of what files are added, what I should inspect first, and what terminal output I should paste back if there is an error.

Do not make the apply script commit automatically.
