###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
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
# v1 / January 2024 / Sacchet (MS)

__all__ = ['simple_ea', 'adaptive_ea']


from datetime import timedelta
from inspect import signature
from time import perf_counter_ns, process_time_ns
from typing import Callable

from byron.classes.evaluator import *
from byron.classes.frame import *
from byron.fitness import make_fitness
from byron.operators import *
from byron.sys import *
from byron.user_messages import *
from byron.user_messages import logger as byron_logger

from .estimator import Estimator
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
        data.append('🕙  ' + s)
    return ' / '.join(data)


def adaptive_ea(*args, **kwargs):
    deprecation_warning("adaptive_ea() is deprecated, use simple_ea() instead.")
    return simple_ea(*args, **kwargs)


def _new_best(population: Population, evaluator: EvaluatorABC):
    byron_logger.info(
        f"SimpleEA: 🍀 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=False)}"
        + f" [🕓 gen: {population.generation:,} / fcalls: {evaluator.fitness_calls:,}]"
    )


def simple_ea(
    top_frame: type[FrameABC],
    evaluator: EvaluatorABC,
    mu: int = 10,
    lambda_: int = 20,
    max_generation: int = 100,
    target_fitness: FitnessABC | None = None,
    top_n: int = 0,
    lifespan: int = None,
    operators: list[Callable] = None,
    rewards: list[float] = [0.7, 0.3],
    temperature: float = 0.85,
    entropy: bool = False,
    population_extra_parameters: dict = None,
    stopper: Callable | None = None,
) -> Population:
    r"""A configurable self-adaptive evolutionary algorithm

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
    target_fitness
        Fitness target
    top_n
        The size of champions population
    lifespan
        The number of generation an individual survive
    operators
        Which operators you want to use
    rewards
        List of rewards for creating an individual fitter than parents [0] and for a successfully created individual [1]
    temperature
        A all round value to tune exploration vs exploitation
    entropy
        Use population entropy parameter to promote diversity in population. Set True only if you understand how population entropy is computed!
    Returns
    -------
    Population
        The last population
    """

    start = perf_counter_ns(), process_time_ns()
    silent_pause = 1
    if notebook_mode:
        silent_pause = 5
    byron_logger.info("SimpleEA: 🧬 [b]SimpleEA started[/] ┈ %s", _elapsed(start, process=True))

    # initialize population
    population = Population(top_frame, extra_parameters=population_extra_parameters, memory=False)

    # stopping conditions
    stopping_conditions = list()
    if stopper:
        stopping_conditions.append(lambda: stopper(population))
    if max_generation:
        stopping_conditions.append(lambda: population.generation >= max_generation)
    # TODO: if max_fitness is alredy a fitness? if minimizing?
    if target_fitness is not None:
        if not isinstance(target_fitness, FitnessABC):
            target_fitness = make_fitness(target_fitness)
        stopping_conditions.append(lambda: best.fitness == target_fitness or best.fitness >> target_fitness)

    if not operators:
        operators = get_operators()

    population.operators_gen0 = [op for op in operators if op.num_parents is None]
    population.operators = [op for op in operators if op.num_parents is not None]
    ext = Estimator(population, max_generation, rewards, population.operators, target_fitness, temperature)

    gen0 = list()
    while len(gen0) < mu:
        o = rrandom.choice(population.operators_gen0)
        gen0 += o(top_frame=top_frame)
    population += gen0
    evaluator(population)
    population.sort()
    best = population[0]
    _new_best(population, evaluator)

    all_individuals = set()

    # begin evolution!
    while not any(s() for s in stopping_conditions):
        new_individuals = list()
        strength = ext.strength(entropy)
        for _ in range(lambda_):
            op = ext.take()
            parents = list()
            for _ in range(op.num_parents):
                parents.append(tournament_selection(population, 1))
            if 'strength' in signature(op).parameters:
                new_individuals += op(*parents, strength=strength)
            else:
                new_individuals += op(*parents)
        if not new_individuals:
            byron_logger.warning(
                "SimpleEA: empty offspring (no new individuals) ┈ %s", _elapsed(start, steps=evaluator.fitness_calls)
            )

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

        byron_logger.hesitant_log(
            silent_pause,
            LOGGING_INFO,
            f"SimpleEA: End of generation %s (𝐻: {population.entropy:.4f}) ┈ %s",
            population.generation,
            _elapsed(start, steps=evaluator.fitness_calls),
        )

    end = process_time_ns()

    byron_logger.info("SimpleEA: 🍦 [b]SimpleEA completed[/] ┈ %s", _elapsed(start, process=True))
    byron_logger.info(
        f"SimpleEA: 🏆 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=True)}",
    )
    byron_logger.info("SimpleEA: Genetic operators statistics:")
    for op in get_operators():
        byron_logger.info(f"SimpleEA: * {op.__qualname__}: {op.stats}")
    return population
