#!/usr/bin/env bash
#################################|###|##################################
#  _____                         |   |                                 #
# |  __ \--.--.----.-----.-----. |===| This file is part of Byron      #
# |  __ <  |  |   _|  _  |     | |___| Evolutionary optimizer & fuzzer #
# |____/ ___  |__| |_____|__|__|  ).(  v0.8a1 "Don Juan"               #
#       |_____|                   \|/                                  #
################################## ' ###################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

# Compiles and runs a genome, kills it if it does not terminate swiftly
# (GNU timeout is /opt/homebrew/bin/gtimeout on my system)
TIMEOUT_CMD=gtimeout
ALLOWED_TIME=3

for file in "$@"; do
    cp "$file" saved-"$file"
    $TIMEOUT_CMD $ALLOWED_TIME go run  main.go "$file" || ( cp "$file" "problem-$file"; echo -1 )
done

exit 0
