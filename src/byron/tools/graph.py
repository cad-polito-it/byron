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

# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)
# v1.1 / August 2024 / Squillero (GX)

__all__ = [
    '_get_first_macro',
    'discard_useless_components',
    'get_structure',
    'fasten_subtree_parameters',
    # 'get_all_frames',
    # 'get_all_macros',
    'get_all_parameters',
    'get_node_parameters',
    'get_dfs_subtree',
    'get_node_color_dict',
    'get_parent_frame_dictionary',
    'get_predecessor',
    'get_siblings',
    'get_successors',
    'make_digraph_cached',
    'set_successors_order',
]

from collections import deque
from collections.abc import Sequence
from functools import lru_cache

import networkx as nx

from byron.classes.node import *
from byron.classes.node_reference import NodeReference
from byron.classes.parameter import ParameterABC, ParameterStructuralABC
from byron.classes.selement import SElement
from byron.global_symbols import *
from byron.user_messages import *

# =[PUBLIC FUNCTIONS]===================================================================================================


def get_successors(ref: NodeReference) -> tuple[int]:
    G = ref.graph
    return tuple(v for u, v, d in G.out_edges(ref.node, data='_type') if d == FRAMEWORK)


def get_predecessor(ref: NodeReference) -> int:
    return next((u for u, v, k in ref.graph.in_edges(ref.node, data='_type') if k == FRAMEWORK), 0)


def get_siblings(ref: NodeReference) -> tuple[int]:
    """
    Returns the list of all successors of node's only predecessor. That is, the node itself and its siblings.

    Args:
        ref: a NodeRef

    Returns:
        A list of node indexes
    """

    assert ref.node != NODE_ZERO, "ValueError: NODE_ZERO has ho siblings."
    return get_successors(NodeReference(ref.graph, get_predecessor(ref)))


def set_successors_order(ref: NodeReference, new_order: Sequence[int]) -> None:
    assert check_valid_type(new_order, Sequence)
    G = ref.graph
    current = tuple((u, v, k) for u, v, k, d in G.out_edges(ref.node, keys=True, data='_type') if d == FRAMEWORK)
    assert all(k == 0 for u, v, k in current), "ValueError: Found a FRAMEWORK edge with key != 0."
    assert {v for u, v, k in current} == set(
        new_order
    ), f"{PARANOIA_VALUE_ERROR}: Mismatching new order: {[v for u, v, k in current]} vs. {new_order}."

    attributes = dict()
    for u, v, k in current:
        attributes[(u, v)] = G.edges[u, v, k]  # save all attributes
        G.remove_edge(u, v, k)
    for v in new_order:
        G.add_edge(ref.node, v, **attributes[(u, v)])  # replace all attributes


def get_node_color_dict(G: nx.MultiDiGraph) -> dict[int, int]:
    """Assign an index to each node based on the name of the underlying macro."""
    known_labels: dict[str, int] = dict()
    colors = dict()
    for n in G:
        name = G.nodes[n]['_selement'].__class__.__name__
        if name not in known_labels:
            known_labels[name] = len(known_labels)
        colors[n] = known_labels[name]
    return colors


def get_all_successors(ref: NodeReference, with_path: bool = True, filter_type: SElement | None = None): ...


def get_all_parameters(G: nx.classes.MultiDiGraph, root: int | None = None) -> tuple:
    raise NotImplementedError("This function is not yet implemented.")


def get_node_parameters(G: nx.classes.MultiDiGraph, root: int | None = None) -> list[tuple]:
    r"""Returns a list of `(node, parameter)` with all parameters of all macro instances

    Parameters
    ----------
    G
        The MultiDiGraph with both the framework tree and the structural links
    root
        If specified, the function returns only parameters in the node traversed by a depth-first visit of the
        framework tree starting from `root` (possibly much slower).

    Return
    ------
    list
        A list of parameters (ie. ``list[ParameterABC]``), or a list of parameters with the associated node
        (ie. ``list[tuple[ParameterABC, node_id]]``)
    """

    if root is None:
        nodes = G.nodes
    else:
        nodes = list(nx.dfs_preorder_nodes(get_structure(G), root))

    return [(n, p) for n in nodes for p in G.nodes[n].values() if isinstance(p, ParameterABC)]


# =[PRIVATE FUNCTIONS]==================================================================================================


def _get_first_macro(root: int, G: nx.MultiDiGraph, T: nx.DiGraph) -> int:
    """Quick n' dirty."""
    return next((n for n in nx.dfs_preorder_nodes(T, root) if G.nodes[n]['_type'] == MACRO), None)


def _get_node_list(G: nx.classes.MultiDiGraph, *, root: int | None, type_: str | None) -> tuple:
    """Get all nodes, or some nodes through dfs"""
    if root is None:
        return tuple(n for n in G.nodes if type_ is None or G.nodes[n]['_type'] == type_)
    else:
        # TODO[gx]: Understand WHY and WHERE this is used
        tree = get_structure(G)
        return tuple(n for n in nx.dfs_preorder_nodes(tree, root) if type_ is None or G.nodes[n]['_type'] == type_)


def fasten_subtree_parameters(node_reference: NodeReference):
    for n, p in get_node_parameters(node_reference.graph, node_reference.node):
        if isinstance(p, ParameterStructuralABC):
            p.fasten(NodeReference(node_reference.graph, n))


def discard_useless_components(G: nx.MultiDiGraph) -> None:
    """Removes unconnected and unreached components"""

    # generate a MultiDiGraph with the provided edges and unconnect all the tree except the first
    def multi_di_graph_with_unconnected_zero(edges):
        h = nx.MultiDiGraph()
        h.add_edges_from(edges)
        h.remove_node(NODE_ZERO)
        node_zero, first_tree = next((u, v) for u, v in G.edges(NODE_ZERO))
        h.add_edge(node_zero, first_tree)
        return h

    # generate the 2 multi di graph (the second only with framework edges)
    H = multi_di_graph_with_unconnected_zero(G.out_edges(keys=False))
    H_framework = multi_di_graph_with_unconnected_zero(
        (u, v) for u, v, d in G.out_edges(keys=False, data='_type') if d == FRAMEWORK
    )

    # remove unconnected nodes
    G.remove_nodes_from(G.nodes - H.nodes)

    # add recursively to the H and H_framework graph the connections to the subroutine subtrees
    while len(nodes_to_connect := nx.descendants(H, NODE_ZERO) - nx.descendants(H_framework, NODE_ZERO)) != 0:
        for n in nodes_to_connect:
            if n in H_framework.nodes:
                tree_parent = next(iter(nx.ancestors(H_framework, n) | {n}))
            else:
                tree_parent = n
            H.add_edge(NODE_ZERO, tree_parent)
            H_framework.add_edge(NODE_ZERO, tree_parent)

    # removes the node not usefull(node that are not descendants of the first tree or there are not part of subroutines called by the first tree)
    nodes_to_remove = H.nodes - (nx.descendants(H, NODE_ZERO) | {NODE_ZERO})
    G.remove_nodes_from(nodes_to_remove)


def get_parent_frame_dictionary(genome: nx.MultiDiGraph) -> dict:
    @lru_cache(1024)
    def get_parent_frame_dictionary_cached(G, nodes_list) -> dict:
        tree = make_digraph_cached(tuple(G.nodes), tuple((u, v) for u, v, k in G.edges(data='_type') if k == FRAMEWORK))
        assert nx.is_branching(tree) and nx.is_weakly_connected(tree), f"{PARANOIA_SYSTEM_ERROR}: Not a valid genome"
        parent_frames = dict()
        for node, path in nx.single_source_dijkstra_path(tree, NODE_ZERO).items():
            parent_frames[node] = tuple(G.nodes[n]['_selement'].__class__ for n in path)
        return parent_frames

    return get_parent_frame_dictionary_cached(genome, tuple(genome.nodes))


@lru_cache(1024)
def make_digraph_cached(nodes, edges):
    """Creates a directed graph from a list of nodes and a list of edges,
    trying to exploit lru_cache using hashable nodes and edges"""
    # TODO[gx]: the use frozen_set for nodes/edge should be evaluated
    tree = nx.DiGraph()
    tree.add_nodes_from(nodes)
    tree.add_edges_from(edges)
    return tree


def get_dfs_subtree(G: nx.MultiDiGraph, root: Node):
    subtree = list()
    queue = deque([root])
    index = 0
    while queue:
        node = deque.pop()
        for new_node in reversed(v for u, v, k in G.out_edges(node, data='_kind') if k == FRAMEWORK):
            if G.nodes[new_node]['_type'] == MACRO:
                subtree.append(new_node)
            else:
                queue.append(new_node)
    return subtree


def get_structure(G: nx.MultiDiGraph) -> nx.DiGraph:
    r"""Returns the framework of a genome. Might be a tree or not."""
    nodes = tuple(sorted(G.nodes))
    edges = tuple(sorted((u, v) for u, v, k in G.edges(data='_type') if k == FRAMEWORK))
    tree = _mk_digraph_cached(nodes, edges)
    # if not nx.is_arborescence(tree):
    #     ic(nx.is_arborescence(tree))
    return tree


@lru_cache(1024)
def _mk_digraph_cached(nodes, edges):
    tree = nx.DiGraph()
    tree.add_nodes_from(nodes)
    tree.add_edges_from(edges)
    return tree
