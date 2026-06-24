#include <stdint.h>

int main(void) {
    volatile uint8_t* screen = (uint8_t*)0x0400;
    screen[0] = 1;   /* screen code for A in the default character set */
    screen[1] = 2;   /* B */
    screen[2] = 3;   /* C */
    while (1) { }
    return 0;
}
