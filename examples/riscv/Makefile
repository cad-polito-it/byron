###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

SHELL=/bin/sh
CFLAGS = -O3

# GNU timeout is /opt/homebrew/bin/gtimeout in GX's machine
TIMEOUT_CMD=gtimeout
ALLOWED_TIME=3

.PHONY: run compile _clean

run: compile
	${TIMEOUT_CMD} ${ALLOWED_TIME} riscv64-unknown-elf-run $(name) 2>&1 || echo -1

compile: main.c
	#./unset_cleaner
	riscv64-unknown-elf-as --warn --fatal-warnings -march=rv64imd -mno-relax $(name).s -o $(name).o
	riscv64-unknown-elf-gcc --all-warnings -o $(name) $< $(name).o

clean: _clean

_clean:
	-rm -f $(name)
	-rm -f *.o *.out
	-rm -f *ind*[a-f0-9]*.s
	-rm -f *.svg *.png
