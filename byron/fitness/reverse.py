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

__all__ = ["reverse_fitness"]

from abc import ABC, abstractmethod
from functools import cache

from byron.classes.fitness import FitnessABC
from byron.user_messages import *


@cache
def reverse_fitness(fitness_class: type[FitnessABC]) -> type[FitnessABC]:
    """Reverse fitness class turning a maximization problem into a minimization one."""
    assert check_valid_type(fitness_class, FitnessABC, subclass=True)

    class T(fitness_class):
        def is_fitter(self, other: FitnessABC) -> bool:
            assert (
                self.__class__ == other.__class__
            ), f"TypeError: different types of fitness: '{self.__class__}' and '{other.__class__}'"
            return super(T, other).is_fitter(self)

        def is_dominant(self, other: FitnessABC) -> bool:
            assert (
                self.__class__ == other.__class__
            ), f"TypeError: different types of fitness: '{self.__class__}' and '{other.__class__}'"
            return super(T, other).is_dominant(self)

        def _decorate(self) -> str:
            # return 'ᴙ⟦' + fitness_class._decorate(self) + '⟧'
            return "ᴙ" + fitness_class._decorate(self)

    return T
