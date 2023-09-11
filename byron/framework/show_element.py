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

__all__ = ['as_text', 'as_lgp', 'as_forest']

from byron.randy import rrandom
from byron.sys import *
from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.classes.selement import SElement
from byron.classes.frame import FrameABC
from byron.framework.macro import macro
from byron.classes.parameter import ParameterABC
from byron.classes.population import Population
from byron.classes.individual import Individual
from byron.operators.initializers import *
from byron.classes.readymade_macros import MacroZero


def as_text(
    element: Individual | type[SElement] | ParameterABC,
    *,
    seed: int | None = 42,
    node_info: bool = True,
    extra_parameters: dict | None = None,
):
    if isinstance(element, type) and issubclass(element, ParameterABC):
        frame = macro(
            '{p1.__class__}\n'
            + '• {p1}\n'
            + '• {p2}\n'
            + '• {p3}\n'
            + '• {p4}\n'
            + '• {p5}\n'
            + '• {p6}\n'
            + '• {p7}\n'
            + '• {p8}\n',
            p1=element,
            p2=element,
            p3=element,
            p4=element,
            p5=element,
            p6=element,
            p7=element,
            p8=element,
        )
        node_info = False
        individual = _generate_random_individual(frame, seed=seed)
    elif isinstance(element, type) and issubclass(element, SElement):
        individual = _generate_random_individual(element, seed=seed)
    elif isinstance(element, Individual):
        individual = element
    else:
        raise NotImplementedError(f"{__name__}.as_text({element!r})")

    # individual = individual.canonic_representation

    if extra_parameters is None:
        extra_parameters = dict()
    parameters = DEFAULT_EXTRA_PARAMETERS | DEFAULT_OPTIONS | extra_parameters
    if node_info:
        parameters |= {'$dump_node_info': True}
    individual.genome.nodes[NODE_ZERO]['$omit_from_dump'] = True
    dump = individual.dump(parameters)
    del individual.genome.nodes[NODE_ZERO]['$omit_from_dump']

    if notebook_mode:
        print(dump)
        return None
    else:
        return dump


def as_lgp(
    element: type[SElement] | Individual,
    *,
    seed: int | None = 42,
):
    if isinstance(element, Individual):
        individual = element
    else:
        individual = _generate_random_individual(element, seed=seed)
    # individual = individual.canonic_representation
    if notebook_mode:
        return individual.as_lgp()
    else:
        return individual.as_lgp('byron_lgp.svg')


def as_forest(
    element: type[SElement] | Individual,
    *,
    seed: int | None = 42,
):
    if isinstance(element, Individual):
        individual = element
    else:
        individual = _generate_random_individual(element, seed=seed)
    # individual = individual.canonic_representation
    if notebook_mode:
        return individual.as_forest()
    else:
        return individual.as_forest('byron_forest.svg')


def _generate_random_individual(
    frame: type[SElement],
    *,
    seed: int | None = 42,
):
    rrandom_state = rrandom.state
    rrandom.seed(seed)

    random_individuals = []
    while not random_individuals:
        random_individuals = random_individual(frame)

    rrandom.state = rrandom_state
    return random_individuals[0]
