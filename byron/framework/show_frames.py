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

__all__ = ['as_text', 'as_lgp', 'as_forest']

from byron.randy import rrandom
from byron.sys import *
from byron.global_symbols import *
from byron.classes.selement import SElement
from byron.classes.population import Population
from byron.classes.readymade_macros import MacroZero


def _prepare_test_population(
    frame: type[SElement],
    *,
    seed: int | None = 42,
    node_info: bool = True,
    extra_parameters: dict | None = None,
):
    rrandom_state = rrandom.state
    rrandom.seed(seed)
    population_parameters = dict()
    if node_info:
        population_parameters |= {'$dump_node_info': True}
    if extra_parameters:
        population_parameters |= extra_parameters
    population = Population(top_frame=frame, extra_parameters=population_parameters)

    generators = [op for op in get_operators() if op.num_parents is None]
    random_individuals = list()
    while not random_individuals:
        random_individuals = rrandom.choice(generators)(top_frame=frame)
    for ind in random_individuals:
        ind.genome.nodes[NODE_ZERO]['$omit_from_dump'] = True
    population += random_individuals

    rrandom.state = rrandom_state
    return population


def as_text(
    frame: type[SElement],
    *,
    seed: int | None = 42,
    node_info: bool = True,
    extra_parameters: dict | None = None,
):
    population = _prepare_test_population(frame, seed=seed, node_info=node_info, extra_parameters=extra_parameters)
    dump = population.dump_individual(0)
    if notebook_mode:
        print(dump)
        return None
    else:
        return dump


def as_lgp(
    frame: type[SElement],
    *,
    seed: int | None = 42,
    node_info: bool = True,
    extra_parameters: dict | None = None,
):
    population = _prepare_test_population(frame, seed=seed, extra_parameters=extra_parameters)
    if notebook_mode:
        return population[0].as_lgp()
    else:
        return population[0].as_lgp('byron_lgp.svg')


def as_forest(
    frame: type[SElement],
    *,
    seed: int | None = 42,
    node_info: bool = True,
    extra_parameters: dict | None = None,
):
    population = _prepare_test_population(frame, seed=seed, extra_parameters=extra_parameters)
    if notebook_mode:
        return population[0].as_forest()
    else:
        return population[0].as_forest('byron_forest.svg')
