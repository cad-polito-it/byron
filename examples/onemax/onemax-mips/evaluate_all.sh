#!/usr/bin/env bash
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

# Compiles and runs a genome, kills it if it does not terminate swiftly
TIMEOUT_CMD=timeout
ALLOWED_TIME=1
re='^[0-9]+$'

for file in "$@"; do
    mipsel-linux-gnu-gcc -static "$file" main.c -o onemax.out
    out="$($TIMEOUT_CMD $ALLOWED_TIME qemu-mipsel onemax.out)" || ( cp "$file" "problem-$file"; echo -1 )
    if [[ $out =~ $re ]] ; then
        echo $out
    fi
    grep -q 'nNone' "$file" && cp "$file" "nNone-$file"
done
rm onemax.out

exit 0
