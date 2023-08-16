# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
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
# v1 / April 2023 / Squillero (GX)

__all__ = ["vanilla_ea"]

from time import perf_counter_ns, process_time_ns
from datetime import timedelta

from byron.operators import *
from byron.sys import *
from byron.classes.selement import *
from byron.classes.population import *
from byron.classes.frame import *
from byron.classes.evaluator import *
from byron.randy import rrandom
from byron.user_messages import *

from .selection import *


def _elapsed(start):
    e = str(timedelta(microseconds=(perf_counter_ns() - start[0]) // 1e3)) + '.0000000000'
    s1 = e[: e.index('.') + 3] + ' [t]'
    e = str(timedelta(microseconds=(process_time_ns() - start[1]) // 1e3)) + '.0000000000'
    s2 = e[: e.index('.') + 3] + ' [byron]'
    return '⏱ ' + s1 + ' / ' + s2


def _new_best(population: Population, evaluator: EvaluatorABC):
    logger.info(
        f"vanilla_ea: 🍀 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=False)}"
    )


def vanilla_ea(
    top_frame: type[FrameABC],
    evaluator: EvaluatorABC,
    mu: int = 10,
    lambda_: int = 20,
    max_generation: int = 100,
    max_fitness: FitnessABC | None = None,
    population_extra_parameters: dict = None,
) -> Population:
    r"""A simple evolutionary algorithm

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

    Returns
    -------
    Population
        The last population

    """
    start = perf_counter_ns(), process_time_ns()
    logger.info("vanilla_ea: 🍦 OPTIMIZATION STARTED ┈ %s", _elapsed(start))

    SElement.is_valid = SElement._is_valid_debug
    population = Population(top_frame, extra_parameters=population_extra_parameters, memory=True)

    # Initialize population
    ops0 = [op for op in get_operators() if op.num_parents is None]
    gen0 = list()
    while len(gen0) < mu:
        o = rrandom.choice(ops0)
        gen0 += o(top_frame=top_frame)

    population += gen0
    evaluator(population)
    population.sort()
    best = population[0]
    _new_best(population, evaluator)

    logger.info("vanilla_ea: End of initialization ┈ %s", _elapsed(start))

    stopping_conditions = list()
    stopping_conditions.append(lambda: population.generation >= max_generation)
    if max_fitness:
        stopping_conditions.append(lambda: best.fitness == max_fitness or best.fitness >> max_fitness)

    # Let's roll
    while not any(s() for s in stopping_conditions):
        ops = [op for op in get_operators() if op.num_parents is not None]
        new_individuals = list()
        for step in range(lambda_):
            op = rrandom.choice(ops)
            parents = list()
            for _ in range(op.num_parents):
                parents.append(tournament_selection(population, 1))
            new_individuals += op(*parents)

        assert new_individuals, f"{PARANOIA_VALUE_ERROR}: empty offspring (no new individuals)."
        population += new_individuals

        old_best = best
        evaluator(population)
        population.sort()
        population.individuals[mu:] = []
        best = population[0]
        if old_best != best:
            _new_best(population, evaluator)

        logger.info("vanilla_ea: End of generation %s ┈ %s", population.generation, _elapsed(start))

    end = process_time_ns()

    logger.info("vanilla_ea: 🍦 OPTIMIZATION COMPLETED ┈ %s", _elapsed(start))
    logger.info("vanilla_ea: %s", _elapsed(start))
    logger.info(
        f"vanilla_ea: 🏆 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=True)}"
    )

    # for p in population._memory:
    #    if p not in population:
    #        population += [p]

    # print(f"Elapsed: {(end-start)/1e9:.2} seconds")

    return population
