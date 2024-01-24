##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

SHELL=/bin/sh
CFLAGS = -O3

# GNU timeout is /opt/homebrew/bin/gtimeout in GX's machine
TIMEOUT_CMD=gtimeout
ALLOWED_TIME=3

.PHONY: run _clean

run: onemax
	${TIMEOUT_CMD} ${ALLOWED_TIME} ./onemax || echo -1

onemax: main.o onemax.s
	gcc -o $@ $^

clean: _clean main.o

_clean:
	-rm -f onemax
	-rm -f *.o *.out
	-rm -f *ind*[a-f0-9]*.s
	-rm -f *.svg *.png
