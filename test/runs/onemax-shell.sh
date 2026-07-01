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

if [[ $1 == -f ]]; then
    shift
    genomes=""
    for f in "$@"; do
        genomes="$genomes $(tail -n 1 "$f")"
    done
else
    genomes="$*"
fi

for g in $genomes; do
    ret="${g//[^1]}"
    echo ${#ret}
done
