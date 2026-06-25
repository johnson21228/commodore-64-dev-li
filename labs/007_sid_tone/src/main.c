#include <conio.h>

#define POKE(addr, val) (*(unsigned char *)(addr) = (unsigned char)(val))

static void sid_silence(void) {
    unsigned char i;
    for (i = 0; i < 25; ++i) {
        POKE(0xd400 + i, 0);
    }
}

int main(void) {
    clrscr();
    bordercolor(COLOR_RED);
    bgcolor(COLOR_BLACK);
    textcolor(COLOR_YELLOW);

    cputsxy(7, 4,  "C64 LEARNING LAB");
    cputsxy(10, 6, "LAB 007 SID TONE");
    cputsxy(4, 10, "VOICE 1 FREQUENCY: $D400/$D401");
    cputsxy(4, 12, "CONTROL REGISTER:  $D404");
    cputsxy(4, 15, "PRESS ANY KEY TO STOP");

    sid_silence();
    POKE(0xd418, 15);       /* volume */
    POKE(0xd405, 0x11);     /* attack/decay */
    POKE(0xd406, 0xf0);     /* sustain/release */
    POKE(0xd400, 0x25);     /* frequency low */
    POKE(0xd401, 0x11);     /* frequency high */
    POKE(0xd404, 0x21);     /* sawtooth + gate */

    cgetc();
    sid_silence();
    return 0;
}
