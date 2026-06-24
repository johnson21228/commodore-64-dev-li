# Capture Back Root Detection Lesson

The Workbench Loop re-entry overlay exposed a second-order Capture Back flaw.

We had already captured the lesson that apply commands should be hardened, but the generated command still asked the human to supply a hardcoded `ROOT` value. The overlay zip root and command root did not match, so the guard correctly failed.

The improved lesson:

```text
Do not make the human synchronize the extracted root folder name.
Detect it.
```

A hardened Capture Back command should be resilient to harmless differences between the zip filename, root folder name, and human-facing overlay name, as long as the apply script is found and verified before execution.
