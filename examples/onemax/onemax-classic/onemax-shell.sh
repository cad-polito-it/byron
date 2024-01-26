#!/usr/bin/env bash
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

if [[ $1 == -f ]]; then
    shift
    genomes=$(tail -1 -q "$@")
else
    genomes="$*"
fi

for g in $genomes; do
    ret="${g//[^1]}"
    echo ${#ret}
done
