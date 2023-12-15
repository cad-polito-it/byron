#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron

print(byron.fit.Scalar(2))
print(byron.fit.Integer(2))
print(byron.fit.Float(2))
print(byron.fit.reverse_fitness(byron.fit.Scalar)(2))
print(byron.fit.reverse_fitness(byron.fit.Integer)(2))
print(byron.fit.reverse_fitness(byron.fit.Float)(2))

print(
    byron.fit.Vector(
        [
            byron.fit.reverse_fitness(byron.fit.Scalar)(2),
            byron.fit.reverse_fitness(byron.fit.Integer)(2),
            byron.fit.reverse_fitness(byron.fit.Float)(2),
        ]
    )
)

print(
    byron.fit.reverse_fitness(byron.fit.Vector)(
        [
            byron.fit.reverse_fitness(byron.fit.Scalar)(2),
            byron.fit.reverse_fitness(byron.fit.Integer)(2),
            byron.fit.reverse_fitness(byron.fit.Float)(2),
        ]
    )
)
