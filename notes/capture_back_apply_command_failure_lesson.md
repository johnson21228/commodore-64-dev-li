# Capture Back Apply Command Failure Lesson

A Capture Back overlay failed mechanically because the zip extracted to one top-level folder name while the terminal command copied from a different folder name.

The idea was right, but the delivery mechanism was brittle.

Lesson:

- Capture Back is the continuity act.
- The overlay is only the delivery mechanism.
- The Apply Command must be self-consistent and fail closed.
- Generated terminal commands must verify the extracted root folder and apply script before copying or running anything.
- Commands must not call `make verify` before the overlay has created or confirmed that target.

This lesson should inform future overlay generation.
