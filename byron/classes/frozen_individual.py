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
# v1 / August 2023 / Squillero (GX)

# NOTE[GX]: This file contains code that some programmer may find upsetting

__all__ = ['FrozenIndividual']

from functools import cache, cached_property

import networkx as nx

from byron.classes.fitness import FitnessABC
from byron.classes.frame import FrameABC
from byron.classes.parameter import ParameterABC
from byron.classes.macro import Macro
from byron.classes.individual import Individual


class FrozenIndividual(Individual):
    def __str__(self):
        return f"𝐢{self._id}"

    @property
    def id(self) -> int:
        return self._id

    @property
    def is_finalized(self) -> bool:
        return self._fitness is not None

    @cached_property
    def valid(self) -> bool:
        return super().valid

    @cached_property
    def dfs_nodes(self) -> list[int]:
        return super().dfs_nodes

    @cached_property
    def macros(self) -> list[Macro]:
        return super().macros

    @cached_property
    def frames(self) -> list[FrameABC]:
        return super().frames

    @cached_property
    def parameters(self) -> list[ParameterABC]:
        return super().parameters

    @cached_property
    def structure_tree(self) -> nx.classes.DiGraph:
        return super().structure_tree

    @property
    def fitness(self) -> FitnessABC:
        return self._fitness

    @fitness.setter
    def fitness(self, value: FitnessABC) -> None:
        raise NotImplementedError

    def discard_useless_components(self):
        raise NotImplementedError
