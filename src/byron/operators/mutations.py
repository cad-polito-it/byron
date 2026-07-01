###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
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

from collections import Counter
from copy import deepcopy
from math import floor

from networkx import dfs_preorder_nodes

from byron.classes import *
from byron.operators.graph_tools import *
from byron.randy import rrandom
from byron.registry import *
from byron.tools.graph import *
from byron.user_messages import *


@genetic_operator(num_parents=1)
def generic_parameter_mutation(parent: Individual, strength=1.0) -> list['Individual']:
    """Mutates a parameter

    The function tries at least 100 times to change the parameter by calling `mutate` with the given strength.
    However, if `strength` is 0, `mutate` is not called at all and the parameter is left untouched.

    strength
        the strength of the mutation
    """

    offspring = parent.clone
    if not offspring.parameters:
        raise ByronOperatorFailure

    parameter = rrandom.choice(offspring.parameters)
    old_value = deepcopy(parameter.value)
    parameter.mutate(strength=strength)
    if strength > 0 and parameter.value == old_value:
        raise ByronOperatorFailure

    return [offspring]


@genetic_operator(num_parents=1)
def array_parameter_mutation(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    candidates = [p for p in offspring.parameters if isinstance(p, ParameterArrayABC)]
    if not candidates:
        raise ByronOperatorFailure

    parameter = rrandom.choice(candidates)
    parameter.mutate(strength=strength)
    return [offspring]


@genetic_operator(num_parents=1)
def add_macro_to_bunch(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    G = offspring.genome
    candidates = [
        n
        for n in offspring.genome
        if isinstance(G.nodes[n]['_selement'], MacroBunch) and G.out_degree[n] < G.nodes[n]['_selement'].SIZE[1] - 1
    ]
    if not candidates:
        raise ByronOperatorFailure

    node = rrandom.choice(candidates)
    macros_in_bunch = list(get_successors(NodeReference(G, node)))
    new_macro_type = rrandom.choice(G.nodes[node]['_selement'].POOL)
    new_macro = unroll_selement(new_macro_type, G)

    G.add_edge(node, new_macro.node, _type=FRAMEWORK)
    initialize_subtree(new_macro)
    if len(macros_in_bunch) > 0:
        i = rrandom.random_int(0, len(macros_in_bunch))
        set_successors_order(NodeReference(G, node), macros_in_bunch[:i] + [new_macro.node] + macros_in_bunch[i:])
    return [offspring]


@genetic_operator(num_parents=1)
def remove_macro_from_bunch(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    G = offspring.genome
    frame_candidates = [
        n
        for n in offspring.genome
        if isinstance(G.nodes[n]['_selement'], MacroBunch) and G.out_degree[n] > G.nodes[n]['_selement'].SIZE[0]
    ]
    if not frame_candidates:
        raise ByronOperatorFailure
    frame_node = rrandom.choice(frame_candidates)
    candidates = [
        (n, G.nodes[n]['_selement'].BYRON_CLASS_NAME)
        for n in dfs_preorder_nodes(G, frame_node)
        if isinstance(G.nodes[n]['_selement'], Macro) and G.in_degree(n) == 1
    ]

    if not candidates:
        raise ByronOperatorFailure

    frequency_candidates = [
        c[0] for c in sorted(candidates, key=lambda x: Counter(i[1] for i in candidates)[x[1]], reverse=True)
    ]

    node = rrandom.choice(frequency_candidates[floor(len(frequency_candidates) * (1 - strength)) :])
    G.remove_node(node)
    return [offspring]
