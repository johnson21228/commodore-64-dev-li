# Expected Result: Lab 002 Screen Memory

A valid run shows that direct memory writes to `$0400` affect the visible C64 text screen.

The app should:

1. build to `dist/screen_memory.prg`;
2. set a blue border and black background;
3. clear the 40x25 text screen by writing spaces into screen RAM;
4. write visible text by storing C64 screen codes into `$0400` onward;
5. show a red `A` in the top-left character cell by writing to `SCREEN[0]`;
6. remain visible until the emulator is closed or reset.

This lab is complete when the `.prg` builds locally and emulator evidence confirms the `SCREEN[0]` observation.
