#!/usr/bin/env python3 -OO
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging

import byron

NUM_BITS = 16


@byron.fitness_function
def fitness(genotype):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


def main():
    byron.welcome()

    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend=None)
    byron.logger.info("main: Using %s", evaluator)
    population = byron.ea.adaptive_ea(
        top_frame, evaluator, max_generation=5_000, lambda_=20, mu=30, max_fitness=NUM_BITS
    )

    macro = byron.f.macro('{v}', v=byron.f.array_parameter(range(2), NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend=None)
    byron.logger.info("main: Using %s", evaluator)
    population = byron.ea.adaptive_ea(
        top_frame, evaluator, max_generation=5_000, lambda_=20, mu=30, max_fitness=NUM_BITS
    )

    # evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    # evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool'))
    # evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib'))
    # evaluators.append(byron.evaluator.ScriptEvaluator('./onemax-shell.sh', args=['-f']))
    # evaluators.append(byron.evaluator.MakefileEvaluator('genome.dat', required_files=['onemax-shell.sh']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        dest='verbose',
        const=2,
        default=1,
        help='use verbose logging (debug messages)',
    )
    parser.add_argument(
        '-q', '--quiet', action='store_const', dest='verbose', const=0, help='be quiet (only log warning messages)'
    )
    args = parser.parse_args()

    if args.verbose == 0:
        byron.logger.setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        byron.logger.setLevel(level=logging.INFO)
    elif args.verbose == 2:
        byron.logger.setLevel(level=logging.DEBUG)

    main()
