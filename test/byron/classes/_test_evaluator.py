#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron as byron


def test_evaluator_abstract_methods():
    try:
        evaluator = byron.classes.evaluator.EvaluatorABC()
    except TypeError:
        pass
    else:
        assert False, "EvaluatorABC should not be instantiable."

    class MyEvaluator(byron.classes.evaluator.EvaluatorABC):
        def evaluate(self, individuals):
            return [byron.classes.fitness.FitnessABC() for i in individuals]

    evaluator = MyEvaluator()
    assert callable(evaluator.evaluate)
