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

import logging
import byron

# data from: https://en.wikipedia.org/wiki/Knapsack_problem
# MAX_WEIGHT = 15
# WEIGHTS = [1, 1, 12, 2, 4]
# VALUES = [1, 2, 4, 2, 10]


MAX_WEIGHT = 50
WEIGHTS = [31, 10, 20, 19, 4, 3, 6]
VALUES = [70, 20, 39, 37, 7, 5, 10]
#max value: 107


@byron.fitness_function
def fitness(genotype):
    """Knapsack value"""
    fitness = [0, 0]
    max_v = 0
    gen = genotype.replace('\n', '')
    for b in gen:
        ib = int(b) - 1
        fitness[0] += VALUES[ib]
        fitness[1] -= WEIGHTS[ib]
        if VALUES[ib] > max_v:
            max_v = VALUES[ib]
    if fitness[1] < -MAX_WEIGHT:
        fitness[0] -= max_v * (-MAX_WEIGHT - fitness[1])
    return fitness


def main():

    macro1 = byron.f.macro('{v}', v=byron.f.integer_parameter(1,3))
    macro2 = byron.f.macro('{v}', v=byron.f.integer_parameter(3,6))
    macro3 = byron.f.macro('{v}', v=byron.f.integer_parameter(6,8))

    top_frame = byron.f.bunch([macro1, macro2, macro3], (1,181))

    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool')
    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib')

    byron.logger.info("main: Using %s", evaluator)

    population = byron.ea.adaptive_ea(
        top_frame, evaluator, max_generation=500, lambda_=20, mu=10, top_n=1, lifespan=2
    )

    byron.sys.log_operators()


byron.logger.setLevel(level=logging.INFO)

main()
