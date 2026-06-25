#include <stdint.h>

#define SCREEN ((volatile uint8_t*)0x0400)
#define COLOR  ((volatile uint8_t*)0xD800)
#define BORDER (*(volatile uint8_t*)0xD020)
#define BG     (*(volatile uint8_t*)0xD021)

#define COLOR_WHITE      1
#define COLOR_RED        2
#define COLOR_LIGHT_BLUE 14
#define COLOR_LIGHT_GREEN 13
#define COLOR_YELLOW     7

static uint8_t screen_code(char c) {
    if (c >= 'A' && c <= 'Z') {
        return (uint8_t)(c - 'A' + 1);
    }
    if (c >= '0' && c <= '9') {
        return (uint8_t)c;
    }
    if (c == ' ') {
        return 32;
    }
    if (c == '$') {
        return 36;
    }
    if (c == '-') {
        return 45;
    }
    if (c == '[') {
        return 27;
    }
    if (c == ']') {
        return 29;
    }
    return 32;
}

static uint16_t offset(uint8_t row, uint8_t col) {
    return (uint16_t)row * 40u + (uint16_t)col;
}

static void clear_screen(void) {
    uint16_t i;
    for (i = 0; i < 1000; ++i) {
        SCREEN[i] = 32;
        COLOR[i] = COLOR_LIGHT_BLUE;
    }
}

static void put_text(uint8_t row, uint8_t col, const char* text, uint8_t color) {
    uint16_t pos = offset(row, col);
    while (*text && pos < 1000) {
        SCREEN[pos] = screen_code(*text);
        COLOR[pos] = color;
        ++text;
        ++pos;
    }
}

int main(void) {
    BORDER = 6; /* blue */
    BG = 0;     /* black */

    clear_screen();

    put_text(4,  10, "C64 LEARNING LAB", COLOR_WHITE);
    put_text(7,   7, "LAB 002 SCREEN MEMORY", COLOR_LIGHT_GREEN);
    put_text(10,  8, "WRITING TO $0400", COLOR_YELLOW);
    put_text(13,  4, "TOP LEFT IS SCREEN[0]", COLOR_LIGHT_BLUE);
    put_text(16,  2, "ROW 10 COL 5 IS OFFSET 405", COLOR_LIGHT_BLUE);
    put_text(21,  7, "CLOSE EMULATOR TO END", COLOR_WHITE);

    SCREEN[0] = screen_code('A');
    COLOR[0] = COLOR_RED;

    while (1) {
        /* Keep the screen visible for emulator review. */
    }

    return 0;
}
