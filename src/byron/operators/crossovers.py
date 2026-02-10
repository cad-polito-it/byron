###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
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

# =[ HISTORY ]===============================================================
# v1 / February 2026 / Crossover operators

__all__ = [
    'parameter_uniform_crossover',
    'bunch_onepoint_crossover',
    'subtree_crossover',
]

from copy import deepcopy

import networkx as nx
from networkx import dfs_preorder_nodes

from byron.classes import *
from byron.classes.frame import MacroBunch, FrameBunch
from byron.operators.graph_tools import *
from byron.randy import rrandom
from byron.registry import *
from byron.tools.graph import *
from byron.user_messages import *


@genetic_operator(num_parents=2)
def parameter_uniform_crossover(parent1: Individual, parent2: Individual, strength: float = 0.5) -> list[Individual]:
    """Uniform crossover of parameters between two individuals.
    
    For each parameter in the offspring, randomly choose the value from either parent
    based on the strength parameter (probability of choosing from parent2).
    
    Parameters
    ----------
    parent1 : Individual
        First parent individual
    parent2 : Individual
        Second parent individual  
    strength : float
        Probability of choosing parameter value from parent2 (0.0-1.0)
        Default 0.5 means equal probability from each parent.
    
    Returns
    -------
    list[Individual]
        A list containing one offspring individual
    """
    offspring = parent1.clone
    
    # Get parameters grouped by macro type from both parents
    from byron.operators.ea_tools import group_parameters_on_macro
    
    params1 = group_parameters_on_macro([parent1])
    params2 = group_parameters_on_macro([parent2])
    
    # Find common macro types between parents
    common_macros = set(params1.keys()) & set(params2.keys())
    
    if not common_macros:
        raise ByronOperatorFailure("No common macro types between parents")
    
    crossover_happened = False
    
    # For each parameter in offspring, potentially swap with parent2's value
    for node in offspring.genome.nodes:
        selement = offspring.genome.nodes[node].get('_selement')
        if selement is None:
            continue
            
        macro_class = selement.__class__
        if macro_class not in common_macros:
            continue
            
        # Get parent2's parameters for this macro type
        if parent2 not in params2.get(macro_class, {}):
            continue
        p2_params = params2[macro_class][parent2]
        
        if not p2_params:
            continue
            
        # For each parameter in this node, maybe swap with one from parent2
        for key, param in list(offspring.genome.nodes[node].items()):
            if not isinstance(param, ParameterABC):
                continue
            if key.startswith('_'):
                continue
                
            if rrandom.random_float(0, 1) < strength:
                # Find a compatible parameter from parent2
                compatible = [p for p in p2_params if type(p) == type(param)]
                if compatible:
                    donor_param = rrandom.choice(compatible)
                    param._value = deepcopy(donor_param.value)
                    crossover_happened = True
    
    if not crossover_happened:
        raise ByronOperatorFailure("No crossover occurred")
    
    return [offspring]


@genetic_operator(num_parents=2)
def bunch_onepoint_crossover(parent1: Individual, parent2: Individual, strength: float = 1.0) -> list[Individual]:
    """One-point crossover within bunch structures.
    
    Finds matching bunch nodes (same type) in both parents and swaps
    a portion of their children at a random crossover point.
    
    Parameters
    ----------
    parent1 : Individual
        First parent individual
    parent2 : Individual
        Second parent individual
    strength : float
        Controls crossover probability (unused, kept for API consistency)
    
    Returns
    -------
    list[Individual]
        A list containing one offspring individual
    """
    offspring = parent1.clone
    G1 = offspring.genome
    G2 = parent2.genome
    
    # Find bunch nodes in both parents grouped by type
    def get_bunch_nodes(G):
        bunches = {}
        for n in G.nodes:
            selement = G.nodes[n].get('_selement')
            if selement and isinstance(selement, (MacroBunch, FrameBunch)):
                macro_class = selement.__class__
                if macro_class not in bunches:
                    bunches[macro_class] = []
                bunches[macro_class].append(n)
        return bunches
    
    bunches1 = get_bunch_nodes(G1)
    bunches2 = get_bunch_nodes(G2)
    
    # Find common bunch types
    common_types = set(bunches1.keys()) & set(bunches2.keys())
    if not common_types:
        raise ByronOperatorFailure("No common bunch types between parents")
    
    # Choose a random bunch type and nodes
    bunch_type = rrandom.choice(list(common_types))
    node1 = rrandom.choice(bunches1[bunch_type])
    node2 = rrandom.choice(bunches2[bunch_type])
    
    # Get children of each bunch
    children1 = list(get_successors(NodeReference(G1, node1)))
    children2 = list(get_successors(NodeReference(G2, node2)))
    
    if len(children1) < 2 or len(children2) < 2:
        raise ByronOperatorFailure("Bunches too small for crossover")
    
    # Choose crossover points
    point1 = rrandom.random_int(1, len(children1))
    point2 = rrandom.random_int(1, len(children2))
    
    # Get size constraints
    size_min = G1.nodes[node1]['_selement'].SIZE[0]
    size_max = G1.nodes[node1]['_selement'].SIZE[1] - 1
    
    # Calculate new size
    new_size = point1 + (len(children2) - point2)
    if new_size < size_min or new_size > size_max:
        raise ByronOperatorFailure("Crossover would violate size constraints")
    
    # Remove children after crossover point from offspring
    for child in children1[point1:]:
        # Remove entire subtree
        subtree = list(dfs_preorder_nodes(G1, child))
        G1.remove_nodes_from(subtree)
    
    # Copy children from parent2 after its crossover point
    node_mapping = {}  # Track all copied nodes across all children
    
    for child2 in children2[point2:]:
        # Deep copy the subtree from parent2
        subtree2_nodes = list(dfs_preorder_nodes(G2, child2))
        
        for old_node in subtree2_nodes:
            new_node = Node()
            node_mapping[old_node] = new_node
            G1.add_node(new_node)
            # Copy node attributes
            for key, value in G2.nodes[old_node].items():
                if isinstance(value, ParameterABC):
                    G1.nodes[new_node][key] = deepcopy(value)
                elif key == '_selement':
                    G1.nodes[new_node][key] = value.__class__()
                else:
                    G1.nodes[new_node][key] = deepcopy(value)
        
        # Add edges within the copied subtree
        for old_node in subtree2_nodes:
            for _, v, data in G2.out_edges(old_node, data=True):
                if v in node_mapping:
                    G1.add_edge(node_mapping[old_node], node_mapping[v], **deepcopy(data))
        
        # Connect to parent bunch
        G1.add_edge(node1, node_mapping[child2], _type=FRAMEWORK)
    
    # Update successors order
    new_children = children1[:point1] + [node_mapping[c] for c in children2[point2:] if c in node_mapping]
    if new_children:
        set_successors_order(NodeReference(G1, node1), new_children)
    
    # Re-fasten parameters
    fasten_subtree_parameters(NodeReference(G1, node1))
    
    return [offspring]


@genetic_operator(num_parents=2)
def subtree_crossover(parent1: Individual, parent2: Individual, strength: float = 1.0) -> list[Individual]:
    """Subtree crossover between two individuals.
    
    Finds matching frame nodes (same type) in both parents and replaces
    a subtree in parent1 with a subtree from parent2.
    
    Parameters
    ----------
    parent1 : Individual
        First parent individual
    parent2 : Individual
        Second parent individual
    strength : float
        Controls selection bias (unused, kept for API consistency)
    
    Returns
    -------
    list[Individual]
        A list containing one offspring individual
    """
    offspring = parent1.clone
    G1 = offspring.genome
    G2 = parent2.genome
    
    # Find frame nodes (not MacroZero) in both parents grouped by type
    def get_frame_nodes(G):
        frames = {}
        for n in G.nodes:
            if n == NODE_ZERO:
                continue
            selement = G.nodes[n].get('_selement')
            if selement and isinstance(selement, FrameABC) and not isinstance(selement, (MacroBunch, FrameBunch)):
                frame_class = selement.__class__
                if frame_class not in frames:
                    frames[frame_class] = []
                frames[frame_class].append(n)
        return frames
    
    frames1 = get_frame_nodes(G1)
    frames2 = get_frame_nodes(G2)
    
    # Find common frame types
    common_types = set(frames1.keys()) & set(frames2.keys())
    if not common_types:
        raise ByronOperatorFailure("No common frame types between parents")
    
    # Choose a random frame type and nodes
    frame_type = rrandom.choice(list(common_types))
    node1 = rrandom.choice(frames1[frame_type])
    node2 = rrandom.choice(frames2[frame_type])
    
    # Get parent of node1 in offspring
    parent_node = None
    for u, v, data in G1.in_edges(node1, data=True):
        if data.get('_type') == FRAMEWORK:
            parent_node = u
            break
    
    if parent_node is None:
        raise ByronOperatorFailure("Cannot find parent node")
    
    # Remove the subtree at node1
    subtree1_nodes = list(dfs_preorder_nodes(G1, node1))
    G1.remove_nodes_from(subtree1_nodes)
    
    # Copy the subtree from parent2 starting at node2
    subtree2_nodes = list(dfs_preorder_nodes(G2, node2))
    node_mapping = {}
    
    for old_node in subtree2_nodes:
        new_node = Node()
        node_mapping[old_node] = new_node
        G1.add_node(new_node)
        # Copy node attributes
        for key, value in G2.nodes[old_node].items():
            if isinstance(value, ParameterABC):
                G1.nodes[new_node][key] = deepcopy(value)
            elif key == '_selement':
                G1.nodes[new_node][key] = value.__class__()
            else:
                G1.nodes[new_node][key] = deepcopy(value)
    
    # Add edges within the copied subtree
    for old_node in subtree2_nodes:
        for _, v, data in G2.out_edges(old_node, data=True):
            if v in node_mapping:
                G1.add_edge(node_mapping[old_node], node_mapping[v], **deepcopy(data))
    
    # Connect to parent
    G1.add_edge(parent_node, node_mapping[node2], _type=FRAMEWORK)
    
    # Re-fasten parameters
    fasten_subtree_parameters(NodeReference(G1, node_mapping[node2]))
    
    # Validate
    if not offspring.valid:
        raise ByronOperatorFailure("Crossover produced invalid individual")
    
    return [offspring]
