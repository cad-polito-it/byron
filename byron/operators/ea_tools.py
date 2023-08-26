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

__all__ = [
    'merge_individuals',
    'group_selements',
    'group_parameters_on_macro',
    'group_parameters_on_classpath',
]

import networkx as nx

from typing import Sequence
from collections import defaultdict
from functools import partial

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.classes.individual import Individual
from byron.classes.macro import Macro
from byron.classes.node_reference import *
from byron.classes.parameter import ParameterABC
from byron.classes.readymade_macros import MacroZero
from byron.classes.selement import SElement
from byron.operators.graph_tools import *


def _parent(G: nx.MultiDiGraph, n: int) -> int:
    return next((u for u, v, t in G.in_edges(n, data='_type') if t == FRAMEWORK), NODE_ZERO)


def _is_head(G: nx.MultiDiGraph, n: int) -> bool:
    n = _parent(G, n)
    while G.nodes[n]['_type'] != MACRO_NODE:
        n = _parent(G, n)
    return isinstance(G.nodes[n]['_selement'], MacroZero)


def _is_target(G: nx.MultiDiGraph, n: int) -> bool:
    return G.in_degree(n) > 1


def group_selements(
    individuals: Sequence[Individual], choosy: bool = False, only_direct_targets: bool = False, only_heads: bool = False
) -> dict[tuple[SElement], dict[Individual, list[int]]]:
    """Group macros"""

    partial_filters = list()
    if only_direct_targets:
        partial_filters.append(lambda G, n: _is_target(G, n))
    if only_heads:
        partial_filters.append(lambda G, n: _is_head(G, n))
    node_filter = lambda G, n: all(f(G, n) for f in partial_filters)

    if choosy:
        make_index = lambda G, path: tuple(G.nodes[v]['_selement'].__class__ for v in path)
    else:
        make_index = lambda G, path: ind.genome.nodes[path[-1]]['_selement'].__class__

    groups = defaultdict(lambda: defaultdict(list))
    for ind in individuals:
        for node, path in nx.single_source_dijkstra_path(ind.genome, 0).items():
            groups[make_index(ind.genome, path)][ind].append(node)

    # remove NodeZero
    for cleanup in {MacroZero, (MacroZero,)}:
        if cleanup in groups:
            del groups[cleanup]
    # remove entries with empty values
    groups = {macro: {p: v for p, v in values.items() if v} for macro, values in groups.items()}

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
        assert set(ind.structure_tree.nodes) == set(ind.genome.nodes)
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
