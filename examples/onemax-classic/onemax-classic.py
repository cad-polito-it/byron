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

import logging
import itertools
import argparse

import byron

NUM_BITS = 100


@byron.fitness_function
def fitness(genotype):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


def main():
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS + 1))
    top_frame = byron.f.sequence([macro])

    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    # evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool'))
    # evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib'))
    # evaluators.append(byron.evaluator.ScriptEvaluator('./onemax-shell.sh', args=['-f']))
    # evaluators.append(byron.evaluator.MakefileEvaluator('genome.dat', required_files=['onemax-shell.sh']))

    byron.logger.info("main: Using %s", evaluator)
    population = byron.ea.vanilla_ea(top_frame, evaluator, max_generation=5, lambda_=20, mu=30)
    population[0].as_lgp('best-lgp.png')
    population[0].as_forest('best-forest.png')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase log verbosity')
    parser.add_argument(
        '-d', '--debug', action='store_const', dest='verbose', const=2, help='log debug messages (same as -vv)'
    )
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
        byron.logger.setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
        byron.logger.setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)
        byron.logger.setLevel(level=logging.DEBUG)

    main()
