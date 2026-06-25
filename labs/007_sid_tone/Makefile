LAB := sid_tone
DIST := dist
SRC := src/main.c
OUT := $(DIST)/$(LAB).prg

.PHONY: build clean

build: $(OUT)

$(OUT): $(SRC)
	mkdir -p $(DIST)
	cl65 -t c64 -o $(OUT) $(SRC)

clean:
	rm -rf $(DIST)
	rm -f src/*.o
