#include <conio.h>
#include <stdio.h>

int main(void) {
    clrscr();

    textcolor(COLOR_LIGHTBLUE);
    bordercolor(COLOR_BLUE);
    bgcolor(COLOR_BLACK);

    cputsxy(7, 5,  "C64 LEARNING LAB");
    cputsxy(8, 7,  "HELLO, WORLD!");
    cputsxy(5, 10, "LAB 001: HELLO SCREEN");
    cputsxy(4, 13, "BUILD: CC65 -> .PRG");
    cputsxy(4, 15, "RUN: VICE / X64SC");
    cputsxy(5, 20, "PRESS ANY KEY TO END");

    cgetc();
    return 0;
}
