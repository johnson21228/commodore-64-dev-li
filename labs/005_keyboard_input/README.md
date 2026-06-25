# Lab 005: Keyboard Input

Purpose: introduce controller behavior on the C64.

This lab waits for keystrokes and updates the screen based on the selected command.

Build:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab005
```

Run:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab005-run
```

Learning point: a useful C64 app can be modeled as a small loop: draw prompt, wait for key, update state, redraw response.
