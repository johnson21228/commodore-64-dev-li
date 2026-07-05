# Workbench Loops — Commodore 64 Pac-Man Lab

**Audience:** Hernan  
**Repo:** `commodore-64-dev-li`  
**Purpose:** Show how a person would interact with Workbench while building a C64 Pac-Man-like game through small, verified, language-backed slices.

This document compresses a raw ChatGPT/terminal transcript into the repeatable Workbench loops that actually appeared in the `commodore-64-dev-li` work. The original file contained long terminal command blocks, pasted outputs, and repeated “run this / verify / status” cycles. Here those are replaced with compact interaction patterns, so the workflow is easier to consume.

---

## 1. What this Workbench session is really demonstrating

The session is not mainly about “using AI to write assembly.” It is about using Workbench to keep generated code accountable.

The C64 program evolves through small slices:

1. declare or discover the next product/game behavior,
2. map that behavior to local source authority,
3. patch the generator and verifier,
4. regenerate assembly,
5. build the PRG,
6. manually inspect visible behavior in VICE,
7. commit only after the loop is coherent.

The AI is not treated as the source of truth. The source chain is:

```text
LI / goal language / board authority
        ↓
generator
        ↓
generated intent receipt
        ↓
generated assembly
        ↓
C64 PRG behavior
        ↓
verify + visual inspection
```

---

## 2. The core Workbench loop

A typical loop with `commodore-64-dev-li` looks like this:

```text
User observes or requests behavior.
Assistant scopes a small slice.
Assistant gives a copy/paste terminal block.
User runs it locally.
Terminal output is pasted back.
Assistant reads the output and either repairs, verifies, or commits.
```

Compressed command form:

```text
cd repo
patch focused files
regenerate generated artifacts
build
run focused verifier
run whole-repo verify
show diff/status
manual visual test when behavior is graphical
commit if coherent
```

The important point for Hernan: Workbench is not a chat-only process. The terminal is the execution surface. Chat is the thinking/interview/control surface.

---

## 3. What “verify” means in this workflow

`verify` is more than “does it compile?”

It checks continuity of meaning:

```text
Does it build?
Does the generated artifact match the declared source?
Does the focused slice exist?
Did previous promises remain true?
Did the new promise become true?
Did deferred promises remain honestly deferred?
Did adjacent labs and governance still pass?
```

For Lab 010, the focused verifier checks things like:

```text
- buffered Pac-Man turns still exist
- compact board rendering still exists
- scoring still exists
- lives still exist
- ghost state/reset still exists
- legal ghost movement exists
- smooth ghost movement exists when F.10 is active
- targeting, eyes, animation, and multiple ghosts remain deferred unless implemented
```

`make verify` then widens the check to Workbench governance and neighboring labs.

A good phrase:

```text
Verify is testing the continuity of meaning from LI → generator → assembly → visible behavior.
```

---

## 4. The slice pattern used so far

### Slice A — Board rendering

The user starts with screenshots/images of a Pac-Man board and asks whether the repo has a board image and whether the gameboard can be rendered.

Workbench response pattern:

```text
Inspect repo/pack.
Identify source authority.
Patch generator or board model.
Regenerate.
Build.
Run in VICE.
Check visible board.
```

Compressed terminal phrasing:

```text
Render board from declared board source.
Verify board dimensions, walls, dots, power dots, starts.
Build PRG and visually inspect in VICE.
```

Key lesson: the board image is inspiration/input, but the runtime authority becomes structured board data.

---

### Slice B — Constrained Pac-Man movement

The user asks whether Pac-Man can be constrained to hallway paths.

The early version tries a deterministic/random path walker. It exposes a problem: Pac-Man stops at the end of a hallway.

Workbench loop:

```text
Observation: Pac-Man stops at hallway end.
Diagnosis: movement policy is not complete enough.
Repair path logic.
Verify path stays on traversable cells.
Build and re-run visual test.
```

Compressed phrasing:

```text
Movement must be hallway-authorized, not screen-coordinate free motion.
A visible failure becomes the next slice.
```

Key lesson: manual visual testing is part of the loop because not every C64 visual behavior is captured by static verification.

---

### Slice C — Buffered Pac-Man movement

The workflow shifts from random path walking to player-like Pac-Man movement:

```text
- joystick port 2
- W/A/S/D fallback
- requested direction buffer
- turn only at cell centers
- blocked turns ignored
- current direction continues if legal
```

Workbench loop:

```text
Define movement policy.
Patch generated assembly through generator.
Update generated_intent.json as a receipt.
Update verifier to require the policy.
Build and manually test controls.
```

Compressed terminal-output replacement:

```text
Patched movement controller.
Regenerated assembly.
Verifier confirms buffered turns and legal path constraints.
Manual test confirms Pac-Man movement behaves like a Pac-Man-style grid walker.
```

---

### Slice D — Compact rendering

The board renderer becomes table-driven rather than unrolled or audit-heavy.

Workbench loop:

```text
Optimize generated assembly while preserving source authority.
Verify no unrolled per-cell writes.
Verify board still renders from compact board tables.
Build and visually inspect.
```

Compressed phrase:

```text
Efficiency is allowed under the hood, but source authority remains outside generated assembly.
```

Key lesson: Workbench allows low-level code to be efficient without making low-level code the authoring surface.

---

### Slice E — Scoring and item consumption

The game adds dot and energizer scoring:

```text
- dot = +10
- energizer = +50
- score only once per consumed cell
- Pac-Man owns item consumption
```

Workbench loop:

```text
Patch scoring model.
Patch generated assembly.
Update generated intent with scoring rules.
Verify scoring constants and consumption behavior.
Build and visually inspect score behavior.
```

Compressed replacement for terminal output:

```text
Scoring added as a generated behavior with explicit values.
Verifier guards dot/energizer values and one-time consumption.
```

---

### Slice F — Expiration and lives

The game adds Pac-Man expiration and lives:

```text
- alive
- expiring
- game over
- initial lives = 3
- expiration consumes one life
- reset if lives remain
- freeze on game over
```

Workbench loop:

```text
Capture product/game concept first.
Separate expiration from lives.
Patch state machine.
Verify state constants and reset behavior.
Build and manually trigger expiration.
Commit after focused verification.
```

Compressed phrase:

```text
Expiration is a primitive. Lives are accounting around that primitive.
```

---

### Slice G — Ghost appearance and collision

The game adds one visible ghost:

```text
- hardware sprite 1
- red ghost appearance
- ghost starts on board
- ghost is overlay, not item owner
- collision triggers Pac-Man expiration
```

Workbench loop:

```text
First make ghost visible.
Then make ghost a runtime object.
Then make collision use ghost state.
Verify ghost sprite pointer, ghost state variables, and collision hook.
```

Compressed replacement:

```text
A ghost is introduced as a visible overlay hazard.
Pac-Man owns dots. Ghosts do not erase or consume board cells.
```

Key lesson: Workbench separated appearance, board state, collision, and later movement.

---

### Slice H — Ghost runtime state and reset

The stationary ghost becomes stateful:

```text
ghost_cell_x
ghost_cell_y
ghost_direction
reset_ghost_to_start
position_ghost_sprite
```

Workbench loop:

```text
Move from hard-coded display to runtime state.
Make reset explicit.
Verify state variables and reset routines.
Manual test confirms collision still works.
```

Compressed phrase:

```text
F.8 turns the ghost from a placed sprite into an object with state.
```

---

### Slice I — Ghost legal movement

The ghost starts moving, but initially in chunky cell steps.

F.9 behavior:

```text
- one ghost moves through legal board paths
- uses current direction first
- tries perpendicular turns before reversing
- movement uses board legal masks
- collision still triggers expiration
```

Observed repair:

```text
Problem: ghost only reversed 180° at wall hit.
Repair: fallback becomes direction-aware.
Policy: try 90°/270° turns before reversing.
```

Compressed terminal-output replacement:

```text
F.9 implemented ghost movement over legal board masks.
Visual test showed reversal too early.
F.9 was repaired so perpendicular turns are tried before reversing.
Verifier was updated to guard the policy in generated intent.
```

Key lesson: the user’s visual observation becomes a Workbench correction loop.

---

### Slice J — Ghost smooth movement

The user asks whether movement can get smoother. Workbench decides to keep F.9 as legal movement, then make F.10 presentation movement.

F.10 behavior:

```text
- preserve legal path choice from F.9
- add ghost target cell
- add ghost sprite pixel state
- move sprite gradually toward target
- commit cell when target reached
- collision checks current and target cell
- animation/eyes/targeting remain deferred
```

Compressed terminal-output replacement:

```text
F.10 replaces cell jumping with target-cell interpolation.
The verifier initially carried stale F.9 checks.
Those were repaired from speedTicks/GHOST_SPEED_TICKS to pixelSpeedTicks/GHOST_PIXEL_SPEED_TICKS.
Build and verify now confirm smooth ghost movement.
```

Key lesson: Workbench verification itself evolves with the slice. Stale verifier expectations are treated as repairable artifacts, not hidden failures.

---

## 5. How to replace raw terminal transcript blocks

The raw file included long blocks like:

```text
cd repo
python patch
make regenerate
make build
verify
diff
status
```

For Hernan, replace those blocks with this compressed form:

```text
Workbench action:
- patched generator/verifier for [slice]
- regenerated generated.s and generated_intent.json
- built dist/pacman_bounce.prg
- ran focused Lab 010 verifier
- ran whole-repo make verify
- visually tested in VICE
- committed if behavior and verification agreed
```

When a repair happens, use:

```text
Repair loop:
- user observed [visible problem]
- assistant identified stale or incomplete invariant
- patched source/generator/verifier
- regenerated and verified
- reran visual test
```

When a commit happens, use:

```text
Commit loop:
- final focused verify passed
- whole-repo verify passed
- staged only scoped files
- reviewed cached diff/stat
- committed with slice message
```

---

## 6. What Hernan should understand about interacting with this WB

Hernan’s role is not to write every line of code manually. His role is to drive the loop with observations, constraints, and acceptance tests.

Useful interaction phrases:

```text
Can you inspect the repo and identify the source authority?
Can you make this a small slice?
What should remain deferred?
Can you patch only the generator and verifier?
Show me the diff before commit.
This visual behavior is wrong; repair the slice.
What does verify prove here?
Commit this slice.
What is the next coherent slice?
```

The WB responds by converting those into local terminal actions, verifier updates, and source-controlled increments.

---

## 7. What makes this Workbench, not just prompting

A simple prompt asks for code.

Workbench keeps the code accountable through:

```text
- local source authority
- generated intent receipts
- generated assembly as artifact
- focused verifiers
- whole-repo governance checks
- manual visual acceptance
- scoped commits
- explicit deferred promises
```

The loop is cumulative. Each slice preserves prior truth while adding one new behavior.

---

## 8. Short executive summary for Hernan

`commodore-64-dev-li` shows Workbench as an AI-assisted development environment where chat, terminal, generator, verifier, and visual runtime form one loop.

The user does not merely ask for code. The user steers visible behavior. The assistant proposes scoped slices. The local repo executes patches. Verification checks that generated assembly still agrees with declared intent. Visual testing catches what static checks cannot. Commits happen only after the slice is coherent.

Compressed thesis:

```text
Workbench turns AI-generated changes into accountable, inspectable, verified increments.
```

For this C64 Pac-Man lab:

```text
LI defines meaning.
The generator produces assembly.
The verifier protects the meaning.
VICE exposes visible behavior.
The user’s observations drive the next slice.
```
