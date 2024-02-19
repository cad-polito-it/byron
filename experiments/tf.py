# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
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
