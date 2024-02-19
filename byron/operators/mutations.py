# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
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

#############################################################################
# HISTORY
# v1 / June 2023 / Squillero (GX)

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.operators.graph_tools import *
from byron.user_messages import *
from byron.classes import *
from byron.registry import *
from byron.functions import *
from byron.randy import rrandom
from byron.tools.graph import *

from networkx import dfs_preorder_nodes
from collections import Counter
from math import ceil, floor


@genetic_operator(num_parents=1)
def single_parameter_mutation(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    candidates = offspring.parameters
    if not candidates:
        raise ByronOperatorFailure
    param = rrandom.choice(candidates)
    mutate(param, strength=strength)
    return [offspring]


@genetic_operator(num_parents=1)
def single_element_array_parameter_mutation(parent: Individual, strength=1.0) -> list['Individual']:
    scale = 0.05
    ext_mutation = 1 / (scale * strength)
    offspring = parent.clone
    candidates = [p for p in offspring.parameters if isinstance(p, ParameterArrayABC)]
    if not candidates:
        raise ByronOperatorFailure
    param = rrandom.choice(candidates)
    new_value = list(param.value)
    for _ in range(ceil(len(param.value) // ext_mutation)):
        i = rrandom.random_int(0, len(param.value))
        new_value[i] = rrandom.choice(param.DIGITS)
    param.value = ''.join(new_value)

    return [offspring]


@genetic_operator(num_parents=1)
def add_macro_to_bunch(parent: Individual, strength=1.0) -> list['Individual']:

    offspring = parent.clone
    G = offspring.genome
    candidates = [
        n
        for n in offspring.genome
        if isinstance(G.nodes[n]["_selement"], FrameMacroBunch)
        and G.out_degree[n] < G.nodes[n]["_selement"].SIZE[1] - 1
    ]
    if not candidates:
        raise ByronOperatorFailure
    node = rrandom.choice(candidates)
    successors = list(get_successors(NodeReference(G, node)))
    # check if any macro in the pool is not present in successors
    not_present = set(
        [
            i
            for i, n in enumerate(G.nodes[node]["_selement"].POOL)
            if n.BYRON_CLASS_NAME not in [G.nodes[i]["_selement"].BYRON_CLASS_NAME for i in successors]
        ]
    )
    if len(not_present) != 0 and strength >= 0.5:
        new_macro_type = G.nodes[node]["_selement"].POOL[rrandom.choice(list(not_present))]
    else:
        # take a list of the successors ordered by frequency
        frequency_ordered = [
            n for n, _ in Counter([G.nodes[i]["_selement"].BYRON_CLASS_NAME for i in successors]).most_common()
        ]
        macro_fo = [m for m in G.nodes[node]["_selement"].POOL if m.BYRON_CLASS_NAME in frequency_ordered]
        # randomly select a macro. The less the strength, the less the variety of macros
        new_macro_type = rrandom.choice(macro_fo[: ceil(len(macro_fo) * strength)])

    new_macro_type = rrandom.choice(G.nodes[node]["_selement"].POOL)

    new_macro_reference = unroll_selement(new_macro_type, G)
    G.add_edge(node, new_macro_reference.node, _type=FRAMEWORK)
    initialize_subtree(new_macro_reference)
    i = rrandom.random_int(0, len(successors))
    set_successors_order(NodeReference(G, node), successors[:i] + [new_macro_reference.node] + successors[i:])
    return [offspring]


@genetic_operator(num_parents=1)
def remove_macro_from_bunch(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    G = offspring.genome
    frame_candidates = [
        n
        for n in offspring.genome
        if isinstance(G.nodes[n]["_selement"], FrameMacroBunch) and G.out_degree[n] > G.nodes[n]["_selement"].SIZE[0]
    ]
    if not frame_candidates:
        raise ByronOperatorFailure
    frame_node = rrandom.choice(frame_candidates)
    candidates = [
        (n, G.nodes[n]["_selement"].BYRON_CLASS_NAME)
        for n in dfs_preorder_nodes(G, frame_node)
        if isinstance(G.nodes[n]["_selement"], Macro) and G.in_degree(n) == 1
    ]

    if not candidates:
        raise ByronOperatorFailure

    frequency_candidates = [
        c[0] for c in sorted(candidates, key=lambda x: Counter(i[1] for i in candidates)[x[1]], reverse=True)
    ]

    node = rrandom.choice(frequency_candidates[floor(len(frequency_candidates) * (1 - strength)) :])
    G.remove_node(node)
    return [offspring]
