# C64 Workbench Thread State and Local Apply Notes

## Current thread summary

This Workbench was created from the Workbench LI template for Commodore 64 development.

The current durable focus is:

```text
C64 MEMORY PAL
```

This begins as a small text-first C64 program and can grow into an ELIZA-style chatbot.

## Why the chatbot idea is valid

A chatbot is a good C64 learning project because it forces the Workbench to handle authentic machine constraints:

- keyboard input;
- PETSCII/screen output;
- small memory budget;
- string handling;
- simple state;
- testable behavior in an emulator.

The first version should not be a modern LLM. It should be a native C64 rule-based text companion.

## Honest architecture ladder

### Stage 1: Native C64 rule bot

The program runs entirely as a C64 program.

Expected behavior:

- title screen;
- prompt;
- user name capture;
- small keyword matcher;
- canned responses;
- HELP and BYE commands.

### Stage 2: Better native C64 personality

The bot gains more text patterns, a better input loop, and a stronger persona.

### Stage 3: C64 terminal bridge

The C64 may later become a terminal to a host-side service. In that model the C64 owns the retro UI, while a modern Mac or server owns heavier reasoning.

### Stage 4: LLM-assisted experience

A modern LLM may help generate or respond through the host-side bridge, but the Workbench should explicitly say that the LLM is not running natively on the C64.

## Local repo state lesson

When applying a generated pack or overlay, first confirm the actual repo root.

The repo root should be:

```text
/Users/stevejohnson/Developer/commodore-64-dev-li
```

The folder can exist even when the original `.pack.zip` is no longer in Downloads. In that case, do not keep trying to unzip the missing base pack. Work from the existing folder.

## Fresh Terminal re-entry

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li

pwd
ls -la

make verify
make pack

git status --short
```

## Overlay apply rule

Before applying a CB overlay, confirm:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li

test -f Makefile
test -f SPINE.md
test -f MAP.md

make verify
```

Then apply the overlay.

## Next implementation target

Create `C64 MEMORY PAL v0`.

Minimum deliverable:

- source file;
- build instructions;
- emulator run instructions;
- simple transcript example;
- capture of what worked and what did not.
