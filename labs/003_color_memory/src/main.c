#include <stdint.h>

int main(void) {
    volatile uint8_t* screen = (uint8_t*)0x0400;
    volatile uint8_t* color = (uint8_t*)0xD800;
    screen[0] = 3;   /* C */
    screen[1] = 6;   /* F */
    screen[2] = 4;   /* D */
    color[0] = 2;
    color[1] = 5;
    color[2] = 7;
    while (1) { }
    return 0;
}
