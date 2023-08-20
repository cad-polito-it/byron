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

__all__ = [
    'merge_individuals',
    'group_macros_on_classpath',
    'group_parameters_on_macro',
    'group_parameters_on_classpath',
]

import networkx as nx

from typing import Sequence
from collections import defaultdict

from byron.global_symbols import *
from byron.classes.individual import Individual
from byron.classes.macro import Macro
from byron.classes.node_reference import *
from byron.classes.parameter import ParameterABC
from byron.classes.readymade_macros import MacroZero
from byron.classes.selement import SElement
from byron.operators.unroll import *


def group_macros_on_classpath(
    individuals: Sequence[Individual],
) -> dict[tuple[SElement], dict[Individual, list[int]]]:
    """Group macros"""
    groups = defaultdict(lambda: defaultdict(list))

    for ind in individuals:
        for node, path in nx.single_source_dijkstra_path(ind.structure_tree, 0).items():
            groups[tuple(ind.genome.nodes[v]['_selement'].__class__ for v in path)][ind].append(node)
    del groups[(MacroZero,)]
    # remove entries with empty values
    groups = {path: {p: v for p, v in values.items() if v} for path, values in groups.items()}
    return {k: v for k, v in groups.items() if v}


def group_parameters_on_macro(
    individuals: Sequence[Individual], *, parameter_type=None
) -> dict[SElement, dict[Individual, list[ParameterABC]]]:
    if parameter_type is None:
        parameter_type = ParameterABC
    groups = defaultdict(lambda: defaultdict(list))
    for ind in individuals:
        for node, selement in ind.genome.nodes(data='_selement'):
            groups[selement.__class__][ind].extend(
                [p for p in ind.genome.nodes[node].values() if isinstance(p, parameter_type)]
            )
    # remove entries with empty values
    groups = {path: {p: v for p, v in values.items() if v} for path, values in groups.items()}
    return {k: v for k, v in groups.items() if v}


def group_parameters_on_classpath(
    individuals: Sequence[Individual], *, parameter_type=None
) -> dict[tuple[SElement], dict[Individual, list[ParameterABC]]]:
    if parameter_type is None:
        parameter_type = ParameterABC
    groups = defaultdict(lambda: defaultdict(list))
    for ind in individuals:
        for node, path in (
            (n, p)
            for n, p in nx.single_source_dijkstra_path(ind.structure_tree, 0).items()
            if isinstance(ind.genome.nodes[n]['_selement'], Macro)
        ):
            groups[tuple(ind.genome.nodes[v]['_selement'].__class__ for v in path)][ind].extend(
                [p for p in ind.genome.nodes[node].values() if isinstance(p, parameter_type)]
            )
    # remove entries with empty values
    groups = {path: {p: v for p, v in values.items() if v} for path, values in groups.items()}
    return {k: v for k, v in groups.items() if v}


def merge_individuals(individuals: list[Individual]) -> Individual:
    merge = individuals[0].clone
    merge._genome = nx.convert_node_labels_to_integers(merge._genome)
    for n in merge._genome.nodes:
        merge._genome.nodes[n]['_parent'] = 0
    for ind in individuals[1:]:
        new_nodezero = len(merge._genome)
        merge._genome = nx.disjoint_union(merge._genome, ind._genome)
        for u, v in merge._genome.edges(new_nodezero):
            merge._genome.add_edge(NODE_ZERO, v, _type=FRAMEWORK)
        merge._genome.remove_node(new_nodezero)
        for n in range(new_nodezero):
            pass
    fasten_subtree_parameters(NodeReference(merge._genome, NODE_ZERO))
    return merge
