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

NUM_BITS = 500


@byron.fitness_function
def fitness(genotype):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


def main():
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS + 1))
    top_frame = byron.f.sequence([macro])

    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool')
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib')

    byron.logger.info("main: Using %s", evaluator)
    # population = byron.ea.vanilla_ea(
    #     top_frame, evaluator, max_generation=5_000, lambda_=20, mu=30, max_fitness=NUM_BITS
    # )

    population = byron.ea.parametric_ea(
        top_frame, evaluator, max_generation=5000, lambda_=20, mu= 30, max_fitness=NUM_BITS
    )

    print()

    byron.sys.log_operators()

byron.logger.setLevel(level=logging.INFO)

main()

# from byron.randy import rrandom

# seq = [0,1,2,3,4,5,6,7,8,9]
# p0 = 1/len(seq)
# prob = [p0] * len(seq)
# p1 = 0.1/(len(seq)-1)
# prob = [p1] * len(seq)
# prob[0] = 0.9
# print(prob)
# res = dict()
# for _ in range(100):
#     s = rrandom.weighted_choice(seq,prob)
#     if s not in res: res[s]= 1 
#     else: res[s] += 1
# print(res)