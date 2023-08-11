#!/usr/bin/env bash
#############################################################################
#   __                          (`/\                                        #
#  |  |--.--.--.----.-----.-----`=\/\   This file is part of byron v0.1     #
#  |  _  |  |  |   _|  _  |     |`=\/\  An evolutionary optimizer & fuzzer  #
#  |_____|___  |__| |_____|__|__| `=\/  https://github.com/squillero/byron  #
#        |_____|                     \                                      #
#############################################################################
# Copyright 2022-23 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

# Compiles and runs a genome, kills it if it does not terminate swiftly
# (GNU timeout is /opt/homebrew/bin/gtimeout on my system)
TIMEOUT_CMD=gtimeout
ALLOWED_TIME=3

for file in "$@"; do
    gcc -o onemax.out main.o "$file"
    $TIMEOUT_CMD $ALLOWED_TIME ./onemax.out || ( cp "$file" "problem-$file"; echo -1 )
    grep -q 'nNone' "$file" && cp "$file" "nNone-$file"
done

exit 0
