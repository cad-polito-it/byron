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

import itertools
import byron

# test_sizes = [10**n for n in range(1, 3)]
test_sizes = [100, 200, 500, 1000]
generators = [op for op in byron.sys.get_operators() if op.num_parents is None]
mutations = [op for op in byron.sys.get_operators() if op.num_parents == 1]
xovers = [op for op in byron.sys.get_operators() if op.num_parents == 2]


def get_base_macros():
    macros = list()
    macros.append(byron.f.macro('int 0x{num:X}', num=byron.f.integer_parameter(0, 2**32)))
    macros.append(byron.f.macro('float 0x{num:X}', num=byron.f.float_parameter(-1, 1)))
    macros.append(byron.f.macro('array 0x{num:X}', num=byron.f.array_parameter('01-', 64)))
    macros.append(byron.f.macro('choice 0x{num:X}', num=byron.f.choice_parameter('ABCDEFG')))
    return macros


@pytest.mark.avoidable
@pytest.mark.parametrize('generator,size', itertools.product(generators, test_sizes))
def test_individual_creation(individuals, generator, size):
    bar1 = byron.f.macro('bar {ref}', ref=byron.f.global_reference('bunch1'))
    bar2 = byron.f.macro('bar {ref}', ref=byron.f.global_reference('bunch2', first_macro=True))
    bunch1 = byron.f.bunch(get_base_macros() + [bar2], size=size // 2, name='bunch1')
    bunch2 = byron.f.bunch(get_base_macros() + [bar1], size=size // 2, name='bunch2')
    body = byron.f.sequence([bunch1, bunch2])
    individuals[size].extend(generator(body))
    individuals[size].extend(generator(body))


@pytest.mark.avoidable
@pytest.mark.parametrize('mutation,size', itertools.product(mutations, test_sizes))
def test_mutation(individuals, mutation, size):
    bar1 = byron.f.macro('bar {ref}', ref=byron.f.global_reference('bunch1'))
    bar2 = byron.f.macro('bar {ref}', ref=byron.f.global_reference('bunch2'))
    bunch1 = byron.f.bunch(get_base_macros() + [bar2], size=(round(size * 0.8), round(size * 1.2)), name='bunch1')
    bunch2 = byron.f.bunch(get_base_macros() + [bar1], size=(round(size * 0.8), round(size * 1.2)), name='bunch2')
    body = byron.f.sequence([bunch1, bunch2])
    offspring = mutation(individuals[size][0])


@pytest.mark.avoidable
@pytest.mark.parametrize('xover,size', itertools.product(xovers, test_sizes))
def test_crossover(individuals, xover, size):
    bar1 = byron.f.macro('bar {ref}', ref=byron.f.global_reference('bunch1'))
    bar2 = byron.f.macro('bar {ref}', ref=byron.f.global_reference('bunch2'))
    bunch1 = byron.f.bunch(get_base_macros() + [bar2], size=(round(size * 0.8), round(size * 1.2)), name='bunch1')
    bunch2 = byron.f.bunch(get_base_macros() + [bar1], size=(round(size * 0.8), round(size * 1.2)), name='bunch2')
    body = byron.f.sequence([bunch1, bunch2])
    offspring = xover(individuals[size][0], individuals[size][1])
