# Card 002: Brainstorm First C64 Application and Chatbot Direction

## Intent

Capture a first product/application brainstorm for the Commodore 64 Development Workbench, including whether a chatbot is a plausible first application.

## Decision

A chatbot is plausible, but the Workbench must distinguish three variants:

1. Native C64 chatbot: feasible as an ELIZA-style rule-based text program.
2. C64 chatbot terminal: feasible with the C64 as a front-end and a modern host running the model or richer logic.
3. Hybrid staged chatbot: recommended long-term path, starting native and later bridging outward.

## Recommended first app

Start with:

```text
C64 Hello Console + ELIZA-style chatbot seed
```

Working title:

```text
C64 MEMORY PAL
```

## Why this is the right first app

- It validates the C64 build/run loop quickly.
- It uses a text UI, which is simpler than sprites or SID work.
- It can grow into a real product personality.
- It exposes authentic C64 constraints: memory, strings, PETSCII, keyboard input, screen layout.
- It avoids overclaiming: the first bot is rule-based, not an LLM.

## Files added

```text
docs/c64/application_brainstorm_chatbot.md
prompts/c64_brainstorm_first_application.md
captures/CAPTURE_BACK_C64_APPLICATION_BRAINSTORM_CHATBOT.md
cards/002_brainstorm_c64_first_application_chatbot_card.md
```

## Validation

The C64 domain verifier should require the brainstorm doc and prompt so this direction remains discoverable.

```bash
make verify
make pack
```

## Next step

Create a `C64 MEMORY PAL v0` card that produces one source file, one build path, one `.prg`, and one emulator observation.
