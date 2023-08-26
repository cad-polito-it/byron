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
# v1 / April 2023 / Squillero (GX)

__all__ = ["vanilla_ea"]

from typing import Optional

from time import perf_counter_ns, process_time_ns
from datetime import timedelta

from tqdm.auto import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm, tqdm_logging_redirect

from byron.operators import *
from byron.sys import *
from byron.classes.selement import *
from byron.classes.frame import *
from byron.classes.evaluator import *
from byron.fitness import make_fitness
from byron.user_messages import logger as byron_logger
from .selection import *


def _elapsed(start, *, process: bool = False, steps: int = 0):
    data = list()
    end = [process_time_ns(), perf_counter_ns()][::-1]
    e = str(timedelta(microseconds=(end[0] - start[0]) // 1e3)) + '.0000000000'
    s = e[: e.index('.') + 3] + ' [t]'
    data.append('⌛ ' + s)
    if steps:
        e = str(timedelta(microseconds=(end[0] - start[0]) // 1e3 // steps)) + '.0000000000'
        s = e[: e.index('.') + 3]
        data.append('🏃 ' + s)
    if process:
        e = str(timedelta(microseconds=(end[1] - start[1]) // 1e3)) + '.0000000000'
        s = e[: e.index('.') + 3] + ' [byron]'
        data.append('⏱️  ' + s)
    return ' / '.join(data)


def _new_best(population: Population, evaluator: EvaluatorABC):
    byron_logger.info(
        f"VanillaEA: 🍀 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=False)}"
    )


def vanilla_ea(
    top_frame: type[FrameABC],
    evaluator: EvaluatorABC,
    mu: int = 10,
    lambda_: int = 20,
    max_generation: int = 100,
    max_fitness: Optional = None,
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
    byron_logger.info("VanillaEA: 🍦 [b]VanillaEA started[/] ┈ %s", _elapsed(start, process=True))

    SElement.is_valid = SElement._is_valid_debug
    population = Population(top_frame, extra_parameters=population_extra_parameters, memory=False)

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

    silent_pause = 1
    if notebook_mode:
        silent_pause = 5

    byron_logger.info("VanillaEA: End of initialization ┈ %s", _elapsed(start, steps=evaluator.fitness_calls))

    stopping_conditions = list()
    stopping_conditions.append(lambda: population.generation >= max_generation)
    if max_fitness:
        if not isinstance(max_fitness, FitnessABC):
            max_fitness = make_fitness(max_fitness)
        stopping_conditions.append(lambda: best.fitness == max_fitness or best.fitness >> max_fitness)

    # Let's roll
    while not any(s() for s in stopping_conditions):
        ops = [op for op in get_operators() if op.num_parents is not None]
        new_individuals = list()
        for step in range(lambda_):
            op = rrandom.choice(ops)
            parents = list()
            for _ in range(op.num_parents):
                parent = tournament_selection(population, 1)
                parents.append(parent)
            new_individuals += op(*parents)

        if not new_individuals:
            byron_logger.warning(
                "VanillaEA: empty offspring (no new individuals) ┈ %s", _elapsed(start, steps=evaluator.fitness_calls)
            )
        population += new_individuals

        old_best = best
        evaluator(population)
        # population.freeze_individual()
        population.sort()
        population.individuals[mu:] = []
        best = population[0]
        if best.fitness >> old_best.fitness:
            _new_best(population, evaluator)

        byron_logger.hesitant_log(
            silent_pause,
            LOGGING_INFO,
            f"VanillaEA: End of generation %s (𝐻: {population.entropy:.4f}) ┈ %s",
            population.generation,
            _elapsed(start, steps=evaluator.fitness_calls),
        )

    end = process_time_ns()

    byron_logger.info("VanillaEA: 🍦 [b]VanillaEA completed[/] ┈ %s", _elapsed(start, process=True))
    byron_logger.info(
        f"VanillaEA: 🏆 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=True)}",
    )

    return population
