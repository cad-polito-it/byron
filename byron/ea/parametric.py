# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################

# Copyright 2023 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

# =[ HISTORY ]===============================================================
# v1 / July 2023 / Squillero (GX)

__all__ = ["parametric_ea"]


from byron.operators import *
from byron.sys import *
from byron.classes.selement import *
from byron.classes.population import *
from byron.classes.frame import *
from byron.classes.evaluator import *
from byron.randy import rrandom
from byron.user_messages import *

from .selection import *


def _new_best(population: Population, evaluator: EvaluatorABC):
    logger.info(
        f"VanillaEA: 🍀 {population[0].describe(include_fitness=True, include_structure=False, include_lineage=False)}"
        + f" [🏃 gen: {population.generation:,} / fcalls: {evaluator.fitness_calls:,}]"
    )


def parametric_ea(
    top_frame: type[FrameABC],
    evaluator: EvaluatorABC,
    mu: int = 10,
    lambda_: int = 20,
    max_generation: int = 100,
    max_fitness: FitnessABC | None = None,
    top_best: int = None,
    lifespan: int = None,
    operators: list = None,
) -> Population:
    r"""A configurable evolutionary algorithm

    Parameters
    ----------
    top_frame
        The top_frame of individuals
    evaluator
        The evaluator used to evaluate individuals
    mu
        The size of the population
    lambda_
        The size the offspring
    top_best
        The size of champions population
    lifespan
        The number of generation an individual survive

    Returns
    -------
    Population
        The last population

    """
    population = Population(top_frame)
    if operators is None or all(op.num_parents is not None for op in operators):
        ops0 = [op for op in get_operators() if op.num_parents is None]
