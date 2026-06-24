TARGET := hello
BUILD_DIR := build
PRG := $(BUILD_DIR)/$(TARGET).prg

.PHONY: all clean run

all: $(PRG)

$(PRG): hello.c
	mkdir -p $(BUILD_DIR)
	cl65 -t c64 -o $(PRG) hello.c

run: $(PRG)
	x64sc -autostart $(PRG)

clean:
	rm -rf $(BUILD_DIR)
