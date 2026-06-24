# Card 003: Capture C64 Workbench Thread State

## Intent

Capture the full conversation state after creating the Commodore 64 Workbench, discussing local application, brainstorming the first application, and troubleshooting the existing Developer folder.

## Captured facts

- Workbench repo name: `commodore-64-dev-li`.
- Expected local path: `/Users/stevejohnson/Developer/commodore-64-dev-li`.
- The base pack may not remain in `~/Downloads` after creation.
- If the folder already exists, work from the existing folder and verify before applying overlays.
- The first application direction is `C64 MEMORY PAL`.
- The first chatbot should be native, rule-based, and ELIZA-style.
- A later C64-as-terminal bridge may talk to a host-side modern LLM.
- The Workbench must not claim that a modern LLM runs natively on the C64.

## Files added

```text
captures/CAPTURE_BACK_C64_WORKBENCH_THREAD_STATE.md
docs/c64/thread_state_and_local_apply_notes.md
prompts/c64_rejoin_thread_and_continue.md
cards/003_capture_c64_thread_state_card.md
```

## Validation

```bash
make verify
make pack
```

## Next card

Create a `C64 MEMORY PAL v0` implementation card.
