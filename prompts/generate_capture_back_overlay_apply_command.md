# Prompt — Generate Capture Back Overlay Apply Command

Use this prompt when producing a terminal command block for a Capture Back overlay.

## Instruction

Generate an apply command block that:

1. changes into the repo root;
2. unzips the overlay into the repo;
3. runs the overlay apply script, if present;
4. runs `make verify`;
5. runs `make pack`;
6. shows `git status --short`;
7. opens the primary review artifacts.

## Required structure

```bash
cd /path/to/repo

unzip -o ~/Downloads/<overlay>.zip -d .

python3 tools/<apply_script>.py

make verify
make pack

git status --short

open <primary_doc>
open <primary_li_rule>
open <primary_artifact_or_manifest>
```

## Open-file rule

Open the files the human most needs to review.

Prefer:

- primary explanatory doc;
- governing LI rule;
- generated artifact if any;
- Capture Back manifest;
- source prompt/template only if central.

Do not open every changed file.

## Response rule

After the user runs the command and pastes terminal output, evaluate:

- whether the apply succeeded;
- whether verification passed;
- whether pack generation completed;
- whether git status matches the expected Capture Back;
- what should be committed if accepted.
