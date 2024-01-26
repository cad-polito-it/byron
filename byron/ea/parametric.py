# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
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


from typing import Callable

from byron.operators import *
from byron.sys import *
from byron.classes.selement import *
#from byron.classes.population import *
from byron.classes.frame import *
from byron.classes.evaluator import *
from byron.fitness import make_fitness
#from byron.randy import rrandom
from byron.user_messages import *
from .common import take_operators
from .selection import *

from math import sqrt, log

def _new_best(population: Population, evaluator: EvaluatorABC):
    logger.info(
        f"ParametricEA: 🍀 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=False)}"
        + f" [🕓 gen: {population.generation:,} / fcalls: {evaluator.fitness_calls:,}]")


def parametric_ea(top_frame: type[FrameABC],
                  evaluator: EvaluatorABC,
                  mu: int = 10,
                  lambda_: int = 20,
                  max_generation: int = 100,
                  max_fitness: FitnessABC | None = None,
                  top_n: int = 0,
                  lifespan: int = None,
                  operators: list[Callable] = None,
                  end_conditions: list[Callable] = None,
                  alpha: int = 10,
                  rewards: list[float] = [0.3, 0.7],
                  population_extra_parameters: dict = None,
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
    max_generation
        Maximum number of generation allowed
    max_fitness
        Fitness target
    top_n
        The size of champions population
    lifespan
        The number of generation an individual survive
    operators
        Which operators you want to use
    end_conditions
        List of possible conditions needed to end the evolution
    alpha
        Parameter to reduce early failure penalty for operators
    rewards
        List of rewards for a successfully created individual [0] and for an individual fitter than parents [1]
    Returns
    -------
    Population
        The last population
    """

    def estimate_operator_probability(operators_list: list[Callable], iterations: int, alpha: int) -> list[float]:
        i_r = rewards[0] # reward for creating individual 
        s_r = rewards[1] # reward for creating individual better than parents
        p0 = 1 / len(operators_list)
        if iterations <= alpha * len(operators_list):
            # list of equal probability for every operator
            return [p0] * len(operators_list)

        p_temp = list()
        # UCB1 algorithm
        for op in operators_list:
            mu = (op.stats.offspring*i_r + op.stats.successes*s_r)/op.stats.calls
            radius = sqrt((2*log(max_generation)/op.stats.calls))
            ucb = mu + radius
            p_temp.append(ucb)
        base = sum(p_temp)
        return [ p / base for p in p_temp ]


    if end_conditions:
        stopping_conditions = end_conditions
    else:
        stopping_conditions = list()
        stopping_conditions.append(lambda: population.generation >= max_generation)
    if max_fitness:
        max_fitness = make_fitness(max_fitness)
        stopping_conditions.append(lambda: best.fitness == max_fitness or best.fitness >> max_fitness)

    # initialize population
    population = Population(top_frame, extra_parameters=population_extra_parameters, memory=False)
    ops0 = take_operators(True, operators)

    gen0 = list()
    while len(gen0) < mu:
        o = rrandom.choice(ops0)
        gen0 += o(top_frame=top_frame)
    population += gen0
    evaluator(population)
    population.sort()
    best = population[0]
    _new_best(population, evaluator)

    all_individuals = set()
    ops = take_operators(False, operators)

    # begin evolution!
    count = 0
    while not any(s() for s in stopping_conditions):
        new_individuals = list()
        for _ in range(lambda_):
            count += 1
            p = estimate_operator_probability(ops, count, alpha)
            op = rrandom.weighted_choice(ops, p)
            parents = list()
            for _ in range(op.num_parents):
                parents.append(tournament_selection(population, 1))
            new_individuals += op(*parents)
            
        if lifespan is not None:
            population.life_cycle(lifespan, 1, top_n)
        population += new_individuals

        evaluator(population)
        population.sort()

        all_individuals |= set(population)

        population.individuals[mu:] = []

        if best.fitness << population[0].fitness:
            best = population[0]
            _new_best(population, evaluator)

    logger.info("ParametricEA: Genetic operators statistics:")
    for op in get_operators():
        logger.info(f"ParametricEA: * {op.__qualname__}: {op.stats}")
    return population