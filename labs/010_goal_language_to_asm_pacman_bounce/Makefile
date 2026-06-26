APP := pacman_bounce
SRC_DIR := src
DIST_DIR := dist
ASM := $(SRC_DIR)/generated.s
INTENT := $(SRC_DIR)/generated_intent.json
GOAL := $(SRC_DIR)/goal.lang
PROGRAM := $(SRC_DIR)/program.lang
PRG := $(DIST_DIR)/$(APP).prg

.PHONY: build run clean regenerate

build: $(PRG)

$(ASM) $(INTENT): $(GOAL) $(PROGRAM) $(SRC_DIR)/generate_asm.py
	python3 $(SRC_DIR)/generate_asm.py $(GOAL) $(PROGRAM) $(INTENT) $(ASM)

$(PRG): $(ASM)
	mkdir -p $(DIST_DIR)
	cl65 -t c64 -o $(PRG) $(ASM)

run: build
	@if command -v x64sc >/dev/null 2>&1; then x64sc $(PRG); else echo "x64sc not found. Install VICE or open $(PRG) manually."; exit 1; fi

regenerate:
	python3 $(SRC_DIR)/generate_asm.py $(GOAL) $(PROGRAM) $(INTENT) $(ASM)

clean:
	rm -rf $(DIST_DIR)
	rm -f $(SRC_DIR)/*.o
