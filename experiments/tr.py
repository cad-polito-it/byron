#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
#   __                          (`/\                                        #
#  |  |--.--.--.----.-----.-----`=\/\   This file is part of byron v0.1     #
#  |  _  |  |  |   _|  _  |     |`=\/\  An evolutionary optimizer & fuzzer  #
#  |_____|___  |__| |_____|__|__| `=\/  https://github.com/squillero/byron  #
#        |_____|                     \                                      #
#############################################################################
# Copyright 2022-23 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron

# @byron.genetic_operator(num_parents=1)
# def foo():
#    pass


@byron.fitness_function
def onemax1(x):
    return x


print(f"Genetic operators: {byron.sysinfo.genetic_operators}")
print(foo.stats)
x = foo("x")
print(f"Genetic operators: {byron.sysinfo.genetic_operators}")
print(foo.stats)

print(onemax1(1234.2))
print(onemax1(1234.2))
print(onemax1(1234.2))

print(f"Genetic operators: {byron.sysinfo.genetic_operators}")
print(f"Fitness functions: {byron.sysinfo.fitness_functions}")

byron.sysinfo.show(foo)
byron.sysinfo.show("foo")
byron.sysinfo.show(print)
pass

i = byron.classes.Individual(None)
i.fitness = byron.fitness.Scalar(3)
# i.fitness = byron.fitness.Scalar(3)
