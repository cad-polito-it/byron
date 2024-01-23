#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0


import pytest
from byron.classes.fitness import FitnessABC


class MyFitness(FitnessABC):#like previous ones it is a mock class
    def __init__(self, value):
        self.value = value

    def is_fitter(self, other):
        return self.value > other.value

    def is_distinguishable(self, other):
        return self.value != other.value

def test_fitness_equality():
    fitness1 = MyFitness(10)
    fitness2 = MyFitness(10)
    assert fitness1 == fitness2

def test_fitness_inequality():
    fitness1 = MyFitness(10)
    fitness2 = MyFitness(20)
    assert fitness1 != fitness2

def test_fitness_greater_than():
    fitness1 = MyFitness(20)
    fitness2 = MyFitness(10)
    assert fitness1 > fitness2

def test_fitness_less_than():
    fitness1 = MyFitness(10)
    fitness2 = MyFitness(20)
    assert fitness1 < fitness2

def test_fitness_dominance():
    fitness1 = MyFitness(20)
    fitness2 = MyFitness(10)
    assert fitness1 >> fitness2
    assert not (fitness1 << fitness2)

def test_fitness_not_dominant():
    fitness1 = MyFitness(10)
    fitness2 = MyFitness(10)
    assert not (fitness1 >> fitness2)
    assert not (fitness1 << fitness2)


def test_fitness_repr():
    fitness = MyFitness(10)
    expected_repr = f"<{fitness.__class__.__module__}.{fitness.__class__.__name__} @ {hex(id(fitness))}>"
    assert repr(fitness) == expected_repr

def test_fitness_str():
    fitness = MyFitness(10)
    expected_str = f"{fitness._decorate()}Ƒ"  # Assuming _decorate returns a string representation of fitness.value
    assert str(fitness) == expected_str


def test_fitness_distinguishability():
    fitness1 = MyFitness(10)
    fitness2 = MyFitness(20)
    fitness3 = MyFitness(10)
    assert fitness1.is_distinguishable(fitness2)
    assert not fitness1.is_distinguishable(fitness3)
