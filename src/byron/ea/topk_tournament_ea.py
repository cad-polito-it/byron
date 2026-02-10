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
# v1 / January 2026 / Franout (FA)

__all__ = ['topk_tournament_ea']
"""
Top-K Tournament Evolutionary Algorithm for Byron

This module provides an evolutionary algorithm using top-k tournament selection for parent selection.
"""

from datetime import timedelta
from inspect import signature
from pathlib import Path
from time import perf_counter_ns, process_time_ns
from typing import Callable

from byron.classes.evaluator import *
from byron.classes.frame import *
from byron.fitness import make_fitness
from byron.operators import *
from byron.sys import *
from byron.tools.checkpoint import save_population
from byron.user_messages import *
from byron.user_messages import logger as byron_logger
from .estimator import Estimator
from .selection import top_k_tournament_selection


def _elapsed(start, *, process: bool = False, steps: int = 0):
    """
    Helper function to format elapsed time for logging.

    Args:
        start (tuple): Start times (process_time_ns, perf_counter_ns).
        process (bool): Whether to include process time.
        steps (int): Number of steps for average time per step.

    Returns:
        str: Formatted elapsed time string.
    """
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

def _new_best(population: Population, evaluator: EvaluatorABC):
    byron_logger.info(
        f"TopK-TournamentEA: 🍀 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=False)}"
        + f" [🕓 gen: {population.generation:,} / fcalls: {evaluator.fitness_calls:,}]"
    )


def topk_tournament_ea(
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
    checkpoint_every: int | None = None,
    checkpoint_file: str | Path | None = None,
    checkpoint_callback: Callable[[Population, int], None] | None = None,
    checkpoint_on_improvement: bool = False,
    tournament_size: int = 2,
    maxSelectable: int = 2,
    tournament_cost_function: Callable[[Individual], float] | None = None,
    with_replacement: bool = False,
) -> Population:
    """
    Evolutionary algorithm using top-k tournament selection for parent selection.

    Parameters
    ----------
    top_frame : type[FrameABC]
        The top frame class for individuals.
    evaluator : EvaluatorABC
        Evaluator used to evaluate individuals.
    mu : int, optional
        Population size (default: 10).
    lambda_ : int, optional
        Offspring size per generation (default: 20).
    max_generation : int, optional
        Maximum number of generations (default: 100).
    target_fitness : FitnessABC or None, optional
        Target fitness to stop evolution (default: None).
    top_n : int, optional
        Number of champions in population (default: 0).
    lifespan : int or None, optional
        Number of generations an individual survives (default: None).
    operators : list[Callable], optional
        List of genetic operators (default: None).
    rewards : list[float], optional
        Rewards for creating fitter individuals (default: [0.7, 0.3]).
    temperature : float, optional
        Exploration/exploitation parameter (default: 0.85).
    entropy : bool, optional
        Use population entropy for diversity (default: False).
    population_extra_parameters : dict, optional
        Extra parameters for population (default: None).
    stopper : Callable or None, optional
        Custom stopping condition (default: None).
    checkpoint_every : int or None, optional
        Save checkpoint every N generations (default: None).
    checkpoint_file : str or Path or None, optional
        Filename for checkpoints (default: None).
    checkpoint_callback : Callable or None, optional
        Custom callback after each generation (default: None).
    checkpoint_on_improvement : bool, optional
        Save checkpoint on improvement (default: False).
    tournament_size : int, optional
        Number of candidates in each tournament (default: 2).
    maxSelectable : int, optional
        Number of winners per tournament (default: 2).
    tournament_cost_function : Callable or None, optional
        Optional cost function for tournament selection (default: None).
    with_replacement : bool, optional
        Select winners with replacement (default: False).

    Returns
    -------
    Population
        The final population after evolution.
    """
    start = perf_counter_ns(), process_time_ns()
    silent_pause = 1
    if notebook_mode:
        silent_pause = 5
    byron_logger.info("TopK-TournamentEA: 🧬 [b]TopK-TournamentEA started[/] ┈ %s", _elapsed(start, process=True))

    # Checkpoint setup
    if checkpoint_every is not None or checkpoint_on_improvement:
        if checkpoint_file is None:
            checkpoint_file = 'checkpoint_gen{generation}.pkl'
        checkpoint_file = Path(checkpoint_file)
    def _save_checkpoint(pop: Population, reason: str = ""):
        if checkpoint_file is None:
            return
        try:
            filename = str(checkpoint_file).format(generation=pop.generation)
            save_population(pop, Path(filename))
            if reason:
                byron_logger.info(f"TopK-TournamentEA: 💾 Checkpoint saved ({reason}) ➜ {filename}")
        except Exception as e:
            byron_logger.error(f"TopK-TournamentEA: Failed to save checkpoint: {e}")

    population = Population(top_frame, extra_parameters=population_extra_parameters, memory=False)

    stopping_conditions = list()
    if stopper:
        stopping_conditions.append(lambda: stopper(population))
    if max_generation:
        stopping_conditions.append(lambda: population.generation >= max_generation)
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

    if checkpoint_every is not None or checkpoint_on_improvement:
        _save_checkpoint(population, "generation 0")
    if checkpoint_callback:
        try:
            checkpoint_callback(population, population.generation)
        except Exception as e:
            byron_logger.error(f"TopK-TournamentEA: Checkpoint callback error: {e}")

    all_individuals = set()

    while not any(s() for s in stopping_conditions):
        new_individuals = list()
        strength = ext.strength(entropy)
        for _ in range(lambda_):
            op = ext.take()
            parents = list()
            for _ in range(op.num_parents):
                byron_logger.info(f"TopK-TournamentEA: 🚀TopK-TournamentEA -Starting championship evaluation for {tournament_size} individuals")
                selected = top_k_tournament_selection(
                    population,
                    tournament_size=tournament_size,
                    maxSelectable=maxSelectable,
                    tournament_cost_function=tournament_cost_function,
                    with_replacement=with_replacement
                )
                byron_logger.info("TopK-TournamentEA: 🚀TopK-TournamentEA selection completed ┈ %s", _elapsed(start, process=True))
                parents.extend(selected)
            parents = parents[:op.num_parents]
            if 'strength' in signature(op).parameters:
                new_individuals += op(*parents, strength=strength)
            else:
                new_individuals += op(*parents)
        if not new_individuals:
            byron_logger.warning(
                "TopK-TournamentEA: empty offspring (no new individuals) ┈ %s", _elapsed(start, steps=evaluator.fitness_calls)
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
            if checkpoint_on_improvement:
                _save_checkpoint(population, f"improvement at gen {population.generation}")
        if checkpoint_every is not None and population.generation % checkpoint_every == 0:
            _save_checkpoint(population, f"periodic (every {checkpoint_every} gen)")
        if checkpoint_callback:
            try:
                checkpoint_callback(population, population.generation)
            except Exception as e:
                byron_logger.error(f"TopK-TournamentEA: Checkpoint callback error: {e}")

        byron_logger.hesitant_log(
            silent_pause,
            LOGGING_INFO,
            f"TopK-TournamentEA: End of generation %s (𝐻: {population.entropy:.4f}) ┈ %s",
            population.generation,
            _elapsed(start, steps=evaluator.fitness_calls),
        )
    if checkpoint_file is not None:
        _save_checkpoint(population, "final")
    end = process_time_ns()
    byron_logger.info("TopK-TournamentEA: 🍦 [b]TopK-TournamentEA completed[/] ┈ %s", _elapsed(start, process=True))
    byron_logger.info(
        f"TopK-TournamentEA: 🏆 {population[0].describe(include_fitness=True, include_structure=False, include_age=True, include_lineage=True)}",
    )
    byron_logger.info("TopK-TournamentEA: Genetic operators statistics:")
    for op in get_operators():
        byron_logger.info(f"TopK-TournamentEA: * {op.__qualname__}: {op.stats}")
    return population
