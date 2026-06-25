#include <conio.h>

static void draw_box(unsigned char left, unsigned char top, unsigned char width, unsigned char height) {
    unsigned char x;
    unsigned char y;

    revers(1);
    for (x = 0; x < width; ++x) {
        cputcxy(left + x, top, ' ');
        cputcxy(left + x, top + height - 1, ' ');
    }
    for (y = 0; y < height; ++y) {
        cputcxy(left, top + y, ' ');
        cputcxy(left + width - 1, top + y, ' ');
    }
    revers(0);
}

int main(void) {
    clrscr();
    bordercolor(COLOR_BLUE);
    bgcolor(COLOR_BLACK);
    textcolor(COLOR_LIGHTGREEN);

    draw_box(2, 2, 36, 17);

    cputsxy(7, 4,  "C64 LEARNING LAB");
    cputsxy(8, 6,  "LAB 004 PETSCII UI");
    cputsxy(5, 9,  "REVERSE VIDEO BOX");
    cputsxy(5, 11, "SCREEN AS TEXT SURFACE");
    cputsxy(5, 13, "UI BEFORE GRAPHICS");
    cputsxy(6, 17, "PRESS ANY KEY TO END");

    cgetc();
    return 0;
}
