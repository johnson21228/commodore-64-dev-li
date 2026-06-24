# Capture Back: C64 Application Brainstorm and Chatbot Direction

## Trigger

The user asked to Capture Back a brainstorm for what application to build in the Commodore 64 Development Workbench, specifically asking whether a chatbot could be built.

## Captured conclusion

A chatbot can be a good C64 Workbench project if the term is handled honestly:

- A native C64 chatbot should be rule-based, ELIZA-style, and memory-conscious.
- A modern LLM cannot be treated as running natively on the C64 in this Workbench.
- A C64-as-terminal architecture is possible later, where the C64 UI communicates with a modern host process.
- The best first project is a text shell that can grow into an ELIZA-style assistant.

## New durable direction

Working title:

```text
C64 MEMORY PAL
```

First behavior:

- boot into a title screen;
- ask for the user's name;
- accept one-line text input;
- match a small set of keywords;
- respond with a C64/Workbench-flavored persona;
- support HELP and BYE;
- build to `.prg` and run in VICE before any hardware claims.

## Files created

```text
docs/c64/application_brainstorm_chatbot.md
prompts/c64_brainstorm_first_application.md
cards/002_brainstorm_c64_first_application_chatbot_card.md
```

## Verification expectation

The C64 verifier should check for the brainstorm and prompt so future sessions can find the decision.
