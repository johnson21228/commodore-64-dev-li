# Prompt — Apply Overlay Terminal Workflow

## Capture Back apply workflow

When giving a user an overlay apply command, make the command reviewable.

Do not stop at unzip.

A good command should:

1. apply the overlay;
2. run the apply script;
3. verify the repo;
4. pack the repo;
5. show status;
6. open the files that make the change understandable.

## Example

```bash
cd /Users/stevejohnson/Developer/<repo>

unzip -o ~/Downloads/<overlay>.zip -d .

python3 tools/<apply_script>.py

make verify
make pack

git status --short

open docs/<primary_doc>.md
open li/<primary_rule>.md
open CAPTURE_BACK_<NAME>.md
```

## Why

Workbench is a human-in-the-loop system.

The apply step changes the repo. The open step creates the human review surface. The commit step remains a human decision.
