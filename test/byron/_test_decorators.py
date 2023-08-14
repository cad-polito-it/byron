#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import _byron as byron


class MyFitness(byron.classes.FitnessABC):
    def __init__(self, value):
        self.value = value

    def calculate(self, individual):
        pass

    @classmethod
    def is_fitter(cls, fitness1, fitness2):
        pass


def test_fitness_function():
    @byron.decorators.fitness_function(MyFitness)
    def my_fitness_function():
        return MyFitness(42)

    fitness_object = my_fitness_function()

    assert isinstance(fitness_object, MyFitness)
