SHELL=/bin/sh
CFLAGS = -O3

# GNU timeout is /opt/homebrew/bin/gtimeout in GX's machine
TIMEOUT_CMD=gtimeout
ALLOWED_TIME=3

.PHONY: run compile _clean

run: compile
	${TIMEOUT_CMD} ${ALLOWED_TIME} riscv64-unknown-elf-run --trace-register $(name) 2>&1 || echo -1

compile:
	riscv64-unknown-elf-as --warn --fatal-warnings -march=rv64imd -mno-relax $(name).s -o $(name).o
	riscv64-unknown-elf-ld --fatal-warnings -o $(name) $(name).o

clean: _clean

_clean:
	-rm -f $(name)
	-rm -f *.o *.out
	-rm -f *ind*[a-f0-9]*.s
	-rm -f *.svg *.png
