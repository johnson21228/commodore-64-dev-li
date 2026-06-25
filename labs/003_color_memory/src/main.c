#include <stdint.h>
#include <conio.h>

#define SCREEN ((volatile uint8_t*)0x0400)
#define COLOR  ((volatile uint8_t*)0xD800)

static void put_direct(uint16_t offset, uint8_t ch, uint8_t color) {
    SCREEN[offset] = ch;
    COLOR[offset] = color;
}

int main(void) {
    uint16_t row10_col5 = (uint16_t)(10 * 40 + 5);

    clrscr();
    bordercolor(COLOR_BLACK);
    bgcolor(COLOR_BLUE);
    textcolor(COLOR_WHITE);

    cputsxy(2, 1, "C64 LEARNING LAB");
    cputsxy(2, 3, "LAB 003 COLOR MEMORY");
    cputsxy(2, 5, "SCREEN RAM: $0400");
    cputsxy(2, 6, "COLOR  RAM: $D800");
    cputsxy(2, 8, "COLOR[0] COLORS SCREEN[0]");
    cputsxy(2, 12, "A B C USE DIFFERENT COLORS");
    cputsxy(2, 20, "CLOSE EMULATOR TO END");

    /* Direct top-left screen/color memory writes. */
    put_direct(0, 1, COLOR_RED);       /* A at SCREEN[0], red COLOR[0]. */
    put_direct(2, 2, COLOR_YELLOW);    /* B at SCREEN[2], yellow COLOR[2]. */
    put_direct(4, 3, COLOR_LIGHTGREEN);/* C at SCREEN[4], light green COLOR[4]. */

    /* A second direct write away from the top-left. */
    put_direct(row10_col5, 4, COLOR_CYAN); /* D at row 10, column 5. */

    while (1) {
    }

    return 0;
}
