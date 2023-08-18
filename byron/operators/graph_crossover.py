# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
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

__all__ = []

import networkx as nx

from byron.user_messages import *
from byron.global_symbols import *
from byron.registry import *
from byron.classes.individual import *
from byron.classes.node_reference import *
from byron.operators.unroll import *


def _merge_individuals(individuals: list[Individual]) -> Individual:
    # merge = Individual(individuals[0].top_frame)
    merge = individuals[0].clone
    merge._genome = nx.convert_node_labels_to_integers(merge._genome)
    for ind in individuals[1:]:
        new_nodezero = len(merge._genome)
        merge._genome = nx.disjoint_union(merge._genome, ind._genome)
        for u, v in merge._genome.edges(new_nodezero):
            merge._genome.add_edge(NODE_ZERO, v, _type=FRAMEWORK)
        merge._genome.remove_node(new_nodezero)
    fasten_subtree_parameters(NodeReference(merge._genome, NODE_ZERO))
    return merge
