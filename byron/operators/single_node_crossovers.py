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
from collections import defaultdict

from .ea_tools import *
from byron.classes import *
from byron.randy import rrandom
from byron.registry import *
from byron.tools.graph import *
from byron.user_messages import *


def _generic_node_crossover(
    parent1: Individual, parent2: Individual, *, choosy: bool = False, only_targets: bool = False, link_type: str
):
    # assert parent1.run_paranoia_checks()
    # assert parent2.run_paranoia_checks()

    common_selements_raw = group_selements([parent1, parent2], only_targets=only_targets, choosy=choosy)
    common_selements = defaultdict(lambda: defaultdict(list))
    for path, elements in common_selements_raw.items():
        if len(elements) < 2:
            continue
        for ind, nodes in elements.items():
            plausible_nodes = [
                n for n in nodes if link_type in set(t for u, v, t in ind.genome.in_edges(n, data='_type'))
            ]
            if not plausible_nodes:
                continue
            common_selements[path][ind] = plausible_nodes
        if len(common_selements[path]) != 2:
            del common_selements[path]

    if not common_selements:
        raise ByronOperatorFailure

    target = rrandom.choice(list(common_selements.keys()))
    node1 = rrandom.choice(common_selements[target][parent1])
    node2 = rrandom.choice(common_selements[target][parent2])
    new_genome = nx.compose(deepcopy(parent1.genome), deepcopy(parent2.genome))
    node1_fanin = new_genome.in_edges(node1, data=True, keys=True)
    node2_fanin = new_genome.in_edges(node2, data=True, keys=True)
    try:
        node1_parent_link = rrandom.choice([(u, v, k, d) for u, v, k, d in node1_fanin if d['_type'] == link_type])
        node2_parent_link = rrandom.choice(
            [(u, v, k, d) for u, v, k, d in node2_fanin if d['_type'] == node1_parent_link[3]['_type']]
        )
    except:
        raise ByronOperatorFailure

    # NOTE[GX]: replace link in node1_parent -> node1 with node1_parent -> node2 preserving links order
    parent1_complete_fanout = list(new_genome.edges(node1_parent_link[0], data=True, keys=True))
    for edge in parent1_complete_fanout:
        new_genome.remove_edge(edge[0], edge[1], key=edge[2])
    for edge in parent1_complete_fanout:
        if edge == node1_parent_link:
            new_genome.add_edge(
                node1_parent_link[0], node2_parent_link[1], node1_parent_link[2], **node1_parent_link[3]
            )
        else:
            new_genome.add_edge(edge[0], edge[1], key=edge[2], **edge[3])
    # NOTE[GX]: replace link in node2_parent -> node2 with node2_parent -> node1 preserving links order
    parent2_complete_fanout = list(new_genome.edges(node1_parent_link[0], data=True, keys=True))
    for edge in parent2_complete_fanout:
        new_genome.remove_edge(edge[0], edge[1], key=edge[2])
    for edge in parent2_complete_fanout:
        if edge == node2_parent_link:
            new_genome.add_edge(
                node2_parent_link[0], node1_parent_link[1], node2_parent_link[2], **node2_parent_link[3]
            )
        else:
            new_genome.add_edge(edge[0], edge[1], key=edge[2], **edge[3])

    discard_useless_components(new_genome)

    if not get_structure_tree(new_genome):
        raise ByronOperatorFailure

    Node.reset_labels(new_genome)
    new_individual = Individual(parent1.top_frame, new_genome)
    # assert new_individual.run_paranoia_checks()

    # assert parent1.run_paranoia_checks()
    # assert parent2.run_paranoia_checks()
    return [new_individual]


# @genetic_operator(num_parents=2)
def linked_node_crossover(parent1: Individual, parent2: Individual):
    return _generic_node_crossover(parent1, parent2, only_targets=True, link_type=LINK)


@genetic_operator(num_parents=2)
def leaf_crossover_unfussy(parent1: Individual, parent2: Individual):
    return _generic_node_crossover(parent1, parent2, choosy=False, only_targets=False, link_type=FRAMEWORK)


@genetic_operator(num_parents=2)
def leaf_crossover_choosy(parent1: Individual, parent2: Individual):
    return _generic_node_crossover(parent1, parent2, choosy=True, only_targets=False, link_type=FRAMEWORK)
