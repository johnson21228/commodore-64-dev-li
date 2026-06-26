APP := c64net_proxy_ping
SRC_DIR := src
DIST_DIR := dist
ASM := $(SRC_DIR)/generated.s
INTENT := $(SRC_DIR)/generated_intent.json
GOAL := $(SRC_DIR)/goal.lang
PROGRAM := $(SRC_DIR)/program.lang

.PHONY: build generate clean run server

generate:
	python3 $(SRC_DIR)/generate_asm.py $(GOAL) $(PROGRAM) $(INTENT) $(ASM)

build: generate
	mkdir -p $(DIST_DIR)
	cl65 -t c64 -o $(DIST_DIR)/$(APP).prg $(ASM)

run: build
	@if command -v x64sc >/dev/null 2>&1; then x64sc $(DIST_DIR)/$(APP).prg; else echo "x64sc not found. Install VICE or open $(DIST_DIR)/$(APP).prg manually."; exit 1; fi

server:
	python3 host/proxy_server.py

clean:
	rm -rf $(DIST_DIR)
	rm -f $(SRC_DIR)/*.o
