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
import os

import byron as byron

NUM_BITS = 100


@byron.fitness_function
def fitness(genotype):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


def test_evaluators():
    # byron.microgp_logger.setLevel(logging.WARNING)

    assert os.path.exists('runs') or os.path.exists('test/runs')
    if os.path.exists('test/runs'):
        os.chdir('test/runs')
    elif os.path.exists('runs'):
        os.chdir('runs')

    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS + 1))
    top_frame = byron.f.sequence([macro])

    evaluators = list()
    evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True))
    evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool'))
    evaluators.append(byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib'))
    evaluators.append(byron.evaluator.ScriptEvaluator('./onemax-shell.sh', args=['-f']))
    evaluators.append(byron.evaluator.MakefileEvaluator('genome.dat', required_files=['onemax-shell.sh']))

    populations = list()
    for e in evaluators:
        byron.rrandom.seed(42)
        byron.logger.info("main: Using %s", e)
        populations.append(byron.ea.vanilla_ea(top_frame, e, max_generation=100, lambda_=20, mu=30))
        pass

    for p1, p2 in itertools.combinations(populations, 2):
        for i1, i2 in zip(populations[0], populations[1]):
            assert i1[1].fitness == i2[1].fitness
