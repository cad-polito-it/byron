#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from math import sqrt
from itertools import combinations

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


def test(type_, n1, n2):
    f1 = type_(n1)
    f2 = type_(n2)
    print(f"* {type_.__name__:<18s} :: {f1} == {f2}: {f1 == f2}")
    print(f"* {type_.__name__:<18s} :: {f1} < {f2}: {f1 < f2}")
    print(f"* {type_.__name__:<18s} :: {f1} > {f2}: {f1 > f2}")
    print(f"* {type_.__name__:<18s} :: {f1} << {f2}: {f1 << f2}")
    print(f"* {type_.__name__:<18s} :: {f1} >> {f2}: {f1 >> f2}")


def main():
    for d, n1, n2 in MAGIC_NUMBERS:
        print(f"\n# {d}")
        for type_ in FITNESS_TYPES:
            test(type_, n1, n2)
        for type_ in FITNESS_TYPES:
            test(byron.fit.reverse_fitness(type_), n1, n2)


if __name__ == "__main__":
    main()
