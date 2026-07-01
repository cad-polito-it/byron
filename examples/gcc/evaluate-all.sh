#!/usr/bin/env bash
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

# Compiles and runs a genome, kills it if it does not terminate swiftly
# (GNU timeout is /opt/homebrew/bin/gtimeout on my system)
TIMEOUT_CMD=gtimeout
ALLOWED_TIME=1

for file in "$@"; do
    gcc -o onemax.out main.o "$file"
    $TIMEOUT_CMD $ALLOWED_TIME ./onemax.out || ( cp "$file" "problem-$file"; echo -1 )
    grep -q 'nNone' "$file" && cp "$file" "nNone-$file"
done

exit 0
