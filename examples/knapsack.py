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
MAX_WEIGHT = 15
WEIGHTS = [1, 1, 12, 2, 4]
VALUES = [1, 2, 4, 2, 10]


@byron.fitness_function
def fitness(genotype):
    """Knapsack value"""
    fitness = [0, 0]
    max_v = 0
    gen = genotype.replace('\n', '')
    for b in gen:
        ib = int(b)
        fitness[0] += VALUES[ib]
        fitness[1] -= WEIGHTS[ib]
        if VALUES[ib] > max_v:
            max_v = VALUES[ib]
    if fitness[1] < -MAX_WEIGHT:
        fitness[0] -= max_v * (-MAX_WEIGHT - fitness[1])
    return fitness


def main():

    macro = byron.f.macro('{v}', v=byron.f.integer_parameter(0, len(VALUES)))
    top_frame = byron.f.bunch([macro], (1, 15))

    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool')
    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib')

    byron.logger.info("main: Using %s", evaluator)

    population = byron.ea.parametric_ea(
        top_frame, evaluator, max_generation=50, lambda_=20, mu=30, top_n=5, lifespan=100
    )

    print()

    byron.sys.log_operators()


byron.logger.setLevel(level=logging.INFO)

main()
