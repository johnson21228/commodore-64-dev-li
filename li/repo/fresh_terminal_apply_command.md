# Fresh Terminal Apply Command

## Purpose

This LI defines a common Workbench workflow for applying overlays with an LLM reasoning model.

## Rule

A Workbench Apply Command SHOULD normally be run in a new terminal window.

The new terminal window creates a clean, copyable execution trace from the start of the repo operation through verification, packing, commit, and final status.

## Why

A fresh terminal window helps the human and LLM reasoning model stay aligned.

It makes it easy to copy and paste the complete terminal output back into the chat without mixing it with unrelated shell history.

That copied output lets the LLM reason from current evidence instead of guessing.

## Recommended workflow

1. Open a new terminal window.
2. Paste the full Apply Command from the LLM.
3. Let the command run until it stops.
4. Copy the complete terminal output.
5. Paste the output back into the same chat.
6. Continue this loop until verification, packing, commit, and final status are complete.

## Apply Command expectation

An Apply Command SHOULD be written so it can be pasted into a new terminal window and run as a coherent block. It MUST fail closed: if verification or packing fails, the command stops before commit.

It SHOULD:

- start with `set -euo pipefail`
- `cd` into the target repo
- unzip or locate the overlay
- run the apply script
- run verification
- run packing
- show `git status`
- commit only when the user has asked for commit
- show the final pack path
- end with a clean status check when possible

## Completion standard

A Workbench loop is not fully complete until the terminal output shows, or the human confirms:

- overlay applied
- verification passed or failures are understood
- cleanup ran
- history was generated
- pack was generated
- changes were committed when intended
- final `git status` is clean or intentionally explained

## LLM behavior

When giving an Apply Command, the LLM SHOULD explicitly invite the user to run it in a new terminal window and paste the full output back into the chat.

The LLM should then reason from the pasted terminal output and keep helping until the repo reaches a stable state.

## Boundary

The fresh terminal window is a workflow convention, not a source of authority.

The repo remains the continuity authority.
The terminal output is validation evidence.
The chat is the reasoning surface.
