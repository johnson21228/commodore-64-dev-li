# C64 Learning Lab Principles

## Purpose

The C64 Learning Lab is the project direction for this Workbench. It is not one monolithic application first. It is a sequence of small, runnable Commodore 64 experiments that teach the machine one concept at a time.

Each lab should answer three questions:

```text
What C64 machine concept are we learning?
What runnable artifact demonstrates it?
What evidence shows that the artifact behaved as expected?
```

## Governing loop

Use this loop for every lab:

```text
concept truth -> tiny program -> emulator run -> observed evidence -> Capture Back
```

This mirrors the Workbench pattern used in other projects:

```text
source truth -> implementation -> verification -> captured continuity
```

## Lab scale

A lab should be deliberately small. Prefer a visible, memorable experiment over a large partially-working program.

Good lab examples:

```text
write one character directly to screen RAM
change foreground color through color RAM
move one sprite by changing x/y registers
make one SID tone
read one key and update the screen
save one small record to disk
```

Avoid starting with:

```text
full game engine
full chatbot
networked LLM terminal
large disk system
cycle-perfect demo effects
```

Those are synthesis projects that come after the smaller labs establish the machine model.

## Emulator-first evidence

The default proof surface is emulator evidence. A lab is not considered learned merely because code was generated. It becomes learned when the human can run it, observe the result, and capture what happened.

Acceptable evidence includes:

```text
VICE launch command
screenshot
terminal build log
short human observation note
known limitation note
```

## Synthesis path

The chatbot idea remains important, but it should become a synthesis lab after screen output, keyboard input, state, PETSCII layout, and memory limits have been explored.

Recommended synthesis path:

```text
Hello Screen -> Screen Memory -> Color Memory -> PETSCII Frame -> Keyboard Input -> Sprite Pet -> SID Mood Machine -> Memory Pal -> Online Gateway
```

## Boundary

Do not claim that the C64 is running a modern LLM natively. The C64 can run rule-based chatbot logic. A modern LLM belongs on a host or server, with the C64 acting as a terminal, interface, or charm layer.
