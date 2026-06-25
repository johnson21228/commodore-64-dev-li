#include <conio.h>

int main(void) {
    unsigned char ch;

    clrscr();
    bordercolor(COLOR_PURPLE);
    bgcolor(COLOR_BLACK);
    textcolor(COLOR_WHITE);

    cputsxy(7, 4,  "C64 LEARNING LAB");
    cputsxy(6, 6,  "LAB 005 KEYBOARD INPUT");
    cputsxy(4, 9,  "PRESS H FOR HELLO");
    cputsxy(4, 10, "PRESS C FOR C64");
    cputsxy(4, 11, "PRESS Q TO QUIT");

    while (1) {
        cputsxy(4, 15, "WAITING FOR KEY...     ");
        ch = cgetc();

        if (ch == 'q' || ch == 'Q') {
            break;
        } else if (ch == 'h' || ch == 'H') {
            cputsxy(4, 17, "HELLO FROM THE KEYBOARD ");
        } else if (ch == 'c' || ch == 'C') {
            cputsxy(4, 17, "COMMODORE 64 IS LISTENING");
        } else {
            cputsxy(4, 17, "TRY H, C, OR Q          ");
        }
    }

    clrscr();
    cputsxy(11, 11, "READY.");
    return 0;
}
