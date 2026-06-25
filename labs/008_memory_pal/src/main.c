#include <conio.h>

static void draw_home(void) {
    clrscr();
    bordercolor(COLOR_CYAN);
    bgcolor(COLOR_BLACK);
    textcolor(COLOR_WHITE);

    cputsxy(8, 3,  "C64 LEARNING LAB");
    cputsxy(11, 5, "LAB 008 MEMORY PAL");
    cputsxy(4, 9,  "1 SCREEN RAM");
    cputsxy(4, 10, "2 COLOR RAM");
    cputsxy(4, 11, "3 SID SOUND");
    cputsxy(4, 12, "Q QUIT");
    cputsxy(4, 16, "ASK ME A TINY C64 FACT.");
}

static void show_fact(const char *line1, const char *line2, const char *line3) {
    clrscr();
    textcolor(COLOR_LIGHTGREEN);
    cputsxy(4, 6, line1);
    cputsxy(4, 8, line2);
    cputsxy(4, 10, line3);
    cputsxy(4, 20, "PRESS ANY KEY FOR MENU");
    cgetc();
}

int main(void) {
    unsigned char ch;

    while (1) {
        draw_home();
        ch = cgetc();

        if (ch == 'q' || ch == 'Q') {
            break;
        } else if (ch == '1') {
            show_fact("SCREEN RAM STARTS AT $0400.", "EACH BYTE IS ONE CELL.", "TOP LEFT IS OFFSET 0.");
        } else if (ch == '2') {
            show_fact("COLOR RAM STARTS AT $D800.", "IT COLORS SCREEN CELLS.", "PAIR IT WITH $0400.");
        } else if (ch == '3') {
            show_fact("SID REGISTERS START AT $D400.", "WRITE FREQUENCY + WAVEFORM.", "THEN OPEN THE GATE.");
        } else {
            show_fact("I ONLY KNOW 1, 2, 3, Q.", "SMALL MEMORY IS OK.", "TINY APPS CAN TEACH.");
        }
    }

    clrscr();
    cputsxy(11, 11, "READY.");
    return 0;
}
