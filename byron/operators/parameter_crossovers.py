# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
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
# v1 / August 2023 / Squillero (GX)

__all__ = ['array_parameter_uniform_crossover_choosy']

from byron.user_messages import *
from byron.classes import *
from byron.registry import *
from byron.randy import rrandom
from .ea_tools import *

# unfussy vs. chosy


@genetic_operator(num_parents=2)
def array_parameter_uniform_crossover_choosy(parent1: Individual, parent2: Individual) -> list['Individual']:
    offspring = parent1.clone

    groups = group_parameters_on_classpath([offspring, parent2], parameter_type=ParameterArrayABC)
    suitable_groups = {k: v for k, v in groups.items() if len(v) == 2}
    if not suitable_groups:
        raise ByronOperatorFailure

    path = rrandom.choice(tuple(suitable_groups.keys()))
    array_in_offspring = rrandom.choice(groups[path][offspring])
    array_in_parent2 = rrandom.choice(groups[path][parent2])
    new_value = [rrandom.choice([p1, p2]) for p1, p2 in zip(array_in_offspring.value, array_in_parent2.value)]
    array_in_offspring.value = ''.join(new_value)

    return [offspring]
