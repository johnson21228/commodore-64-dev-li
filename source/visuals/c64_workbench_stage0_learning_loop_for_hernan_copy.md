# Source Copy — C64 Workbench Stage 0 Learning Loop for Hernan

This infographic shows the workflow behind the C64 Learning Lab. The project is not just random C64 examples — it is a repeatable loop.

We use the conversation to design the next small lab, then capture that into a local repo as source code, docs, prompts, cards, and verification rules. `make verify` checks that the Workbench is still coherent. cc65 builds real C64 `.prg` files. VICE runs them in an emulator so each lesson has visible evidence.

Each lab teaches one machine concept: screen memory, color memory, PETSCII, keyboard input, sprites, SID sound, and then a tiny Memory Pal app. The loop is: idea → repo → verify → build → run in emulator → capture back → next lab.

The goal is a re-enterable learning system, not just a pile of snippets.

