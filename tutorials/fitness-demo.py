#!/usr/bin/env python3
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from math import sqrt

import byron

FITNESS_TYPES = [
    byron.fit.Scalar,
    byron.fit.Integer,
    byron.fit.Float,
]

MAGIC_NUMBERS = [
    ("42.1 vs. 42.2", 42.1, 42.2),
    ("2 vs. sqrt(2)**2", 2, sqrt(2) ** 2),
    ("3 vs. .1+.1+.1", 0.3, 0.1 + 0.1 + 0.1),
]


def run_comparison(type_, n1, n2):
    f1 = type_(n1)
    f2 = type_(n2)
    # ic(f1 == f2)
    # ic(f1 < f2)
    # ic(f1 > f2)
    # ic(f1 << f2)
    # ic(f1 >> f2)


def main():
    for d, n1, n2 in MAGIC_NUMBERS:
        # ic()
        for type_ in FITNESS_TYPES:
            # ic(d, type_)
            run_comparison(type_, n1, n2)
            type2_ = byron.fit.reverse_fitness(type_)
            # ic(d, type2_)
            run_comparison(type2_, n1, n2)


if __name__ == "__main__":
    main()
