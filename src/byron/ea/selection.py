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

#############################################################################
# HISTORY
# v1 / July 2023 / Squillero (GX)

from typing import Callable, List
from byron.classes.individual import Individual
from byron.classes.population import Population
from byron.randy import rrandom
from byron.user_messages.checks import *
from byron.user_messages import logger as byron_logger

def top_k_tournament_selection(
    population: Population,
    tournament_size: int = 2,
    maxSelectable: int = 1,
    tournament_cost_function: Callable[List[Individual], float] | None = None,
    with_replacement: bool = False
) -> list[Individual]:
    """
    Select the top-k individuals from a tournament.
    If with_replacement is False, winners are unique; otherwise, individuals can be selected multiple times.
    If tournament_cost_function is provided, higher cost is better; otherwise, higher fitness is better.
    """
    assert check_value_range(tournament_size, min_=1)
    assert 1 <= maxSelectable <= tournament_size
    if len(population.individuals) < tournament_size:
        byron_logger.warning("Population size is smaller than tournament size.")
    
    candidates = [rrandom.choice(population.individuals) for _ in range(tournament_size)]
    if tournament_cost_function is not None:
        # Higher cost is better
        sorted_candidates = tournament_cost_function(candidates, maxSelectable)
    else:
        sorted_candidates = sorted(candidates, key=lambda i: i.fitness, reverse=True)
    if with_replacement:
        # Allow repeated selection of top individuals
        return [sorted_candidates[i % len(sorted_candidates)] for i in range(maxSelectable)]
    else:
        return sorted_candidates[:maxSelectable]

def tournament_selection(population: Population, tournament_size: float = 2, tournament_cost_function : Callable[[Individual], float] | None = None) -> Individual:
    """

    Args:
        population (Population): _description_
        tournament_size (float, optional): _description_. Defaults to 2.
        tournament_cost_function (Callable[[Individual], float] | None, optional): _description_. Defaults to None.

    Returns:
        Individual: _description_
    """
    assert check_value_range(tournament_size, min_=1)
    if tournament_cost_function is not None:
        candidates = [rrandom.choice(population.individuals) for _ in range(tournament_size)]
        if rrandom.boolean(p_true=tournament_size % 1):
            candidates.append(rrandom.choice(population.individuals))
        return max(candidates, key=lambda i: tournament_cost_function(i))
    if tournament_cost_function is not None:
        return tournament_selection_with_cost(population, tournament_size, tournament_cost_function)
    else :
        candidates = [rrandom.choice(population.individuals) for _ in range(tournament_size)]
        if rrandom.boolean(p_true=tournament_size % 1):
            candidates.append(rrandom.choice(population.individuals))
        return max(candidates, key=lambda i: i.fitness)


def tournament_selection_with_cost(population: Population, tournament_size: float = 2, cost_fn=None) -> Individual:
    """
    Tournament selection with an additional cost function.
    The cost_fn should take an Individual and return a numeric value (higher is better).
    """
    candidates = [rrandom.choice(population.individuals) for _ in range(tournament_size)]
    if rrandom.boolean(p_true=tournament_size % 1):
        candidates.append(rrandom.choice(population.individuals))
        return max(candidates, key=lambda i: (cost_fn(i), -i.fitness))