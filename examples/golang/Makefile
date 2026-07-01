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

help:
	# Use either 'make fmt' or 'make clean'

fmt:
	go fmt *.go

clean:
	-rm -f individual[0-9]*.go saved-individual[0-9]*.go
	-rm -f *-ind*[a-f0-9]*.go
	-rm -f *.png
