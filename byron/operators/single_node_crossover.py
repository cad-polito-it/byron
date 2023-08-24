# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
import networkx as nx

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

from copy import deepcopy

from .ea_tools import *
from byron.classes import *
from byron.randy import rrandom
from byron.registry import *
from byron.tools.graph import *
from byron.user_messages import *

# unfussy vs. chosy


@genetic_operator(num_parents=2)
def single_node_crossover(parent1: Individual, parent2: Individual):
    common_selements = {k: v for k, v in group_selements([parent1, parent2], only_targets=True).items() if len(v) == 2}
    if not common_selements:
        raise ByronOperatorFailure
    target = rrandom.choice(list(common_selements.keys()))
    node1 = rrandom.choice(common_selements[target][parent1])
    node2 = rrandom.choice(common_selements[target][parent2])
    offspring = nx.compose(parent1.genome, parent2.genome)
    node1_fanin = offspring.in_edges(node1, data='_type', keys=True)
    node2_fanin = offspring.in_edges(node2, data='_type', keys=True)
    node1_parent_link = rrandom.choice([(u, v, k, t) for u, v, k, t in node1_fanin if t != FRAMEWORK])
    node2_parent_link = rrandom.choice([(u, v, k, t) for u, v, k, t in node2_fanin if t == node1_parent_link[3]])

    offspring.remove_edge(node1_parent_link[0], node1_parent_link[1], node1_parent_link[2])
    offspring.remove_edge(node2_parent_link[0], node2_parent_link[1], node2_parent_link[2])
    offspring.add_edge(node1_parent_link[0], node2_parent_link[1], node1_parent_link[2], _type=node1_parent_link[3])
    discard_useless_components(offspring)

    if not get_structure_tree(offspring):
        raise ByronOperatorFailure

    Node.reset_labels(offspring)
    return [Individual(parent1.top_frame, offspring)]
