# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
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
# v1 / April 2023 / Squillero (GX)

__all__ = [
    '_get_first_macro',
    'discard_useless_components',
    'fasten_subtree_parameters',
    'get_all_frames',
    'get_all_macros',
    'get_all_parameters',
    'get_dfs_subtree',
    'get_node_color_dict',
    'get_parent_frame_dictionary',
    'get_predecessor',
    'get_siblings',
    'get_structure_tree',
    'get_successors',
    'make_digraph',
    'set_successors_order',
]

from collections.abc import Sequence
from functools import lru_cache
from collections import deque

import networkx as nx

from byron.global_symbols import *
from byron.classes.node import *
from byron.user_messages import *
from byron.classes.node_reference import NodeReference
from byron.classes.parameter import ParameterABC, ParameterStructuralABC

# =[PUBLIC FUNCTIONS]===================================================================================================


def get_successors(ref: NodeReference) -> tuple[int]:
    G = ref.graph
    return tuple(v for u, v, d in G.out_edges(ref.node, data="_type") if d == FRAMEWORK)


def get_predecessor(ref: NodeReference) -> int:
    return next((u for u, v, k in ref.graph.in_edges(ref.node, data="_type") if k == FRAMEWORK), 0)


def get_siblings(ref: NodeReference) -> tuple[int]:
    """
    Returns the list of all successors of node's only predecessor. That is, the node itself and its siblings.

    Args:
        ref: a NodeRef

    Returns:
        A list of node indexes
    """

    assert ref.node != NODE_ZERO, f"ValueError: NODE_ZERO has ho siblings."
    return get_successors(NodeReference(ref.graph, get_predecessor(ref)))


def set_successors_order(ref: NodeReference, new_order: Sequence[int]) -> None:
    assert check_valid_type(new_order, Sequence)
    G = ref.graph
    current = tuple((u, v, k) for u, v, k, d in G.out_edges(ref.node, keys=True, data="_type") if d == FRAMEWORK)
    assert all(k == 0 for u, v, k in current), f"ValueError: Found a FRAMEWORK edge with key != 0."
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
    known_labels = dict()
    colors = dict()
    for n in G:
        name = G.nodes[n]["_selement"].__class__.__name__
        if name not in known_labels:
            known_labels[name] = len(known_labels)
        colors[n] = known_labels[name]
    return colors


def get_all_frames(
    G: nx.classes.MultiDiGraph, root: int | None = None, *, data: bool = True, node_id: bool = False
) -> tuple:
    node_lst = _get_node_list(G, root=root, type_=FRAME_NODE)
    if data:
        data_lst = tuple(G.nodes[n]["_selement"] for n in node_lst)
    if data and node_id:
        return tuple(zip(data_lst, node_lst))
    elif data and not node_id:
        return data_lst
    elif not data and node_id:
        return node_lst
    else:
        raise tuple()


def get_all_macros(
    G: nx.classes.MultiDiGraph, root: int | None = None, *, data: bool = True, node_id: bool = False
) -> tuple:
    node_lst = _get_node_list(G, root=root, type_=MACRO_NODE)
    if data:
        data_lst = tuple(G.nodes[n]["_selement"] for n in node_lst)
    if data and node_id:
        return tuple(zip(data_lst, node_lst))
    elif data and not node_id:
        return data_lst
    elif not data and node_id:
        return node_lst
    else:
        raise NotImplementedError


def get_all_parameters(G: nx.classes.MultiDiGraph, root: int | None = None, *, node_id: bool = False) -> tuple:
    r"""Returns all parameters of all macro instances

    Parameters
    ----------
    G
        The MultiDiGraph with both the framework tree and the structural links
    root
        If specified, the function returns only parameters in the node traversed by a depth-first visit of the
        framework tree starting from `root` (possibly much slower).
    node_id
        If ``True`` the functions returns a list of tuple `(parameter, node)`

    Return
    ------
    list
        A list of parameters (ie. ``list[ParameterABC]``), or a list of parameters with the associated node
        (ie. ``list[tuple[ParameterABC, node_id]]``)
    """

    if node_id:
        return tuple(
            (p, n)
            for n in _get_node_list(G, root=root, type_=None)
            for p in G.nodes[n].values()
            if isinstance(p, ParameterABC)
        )
    else:
        return tuple(
            p
            for n in _get_node_list(G, root=root, type_=None)
            for p in G.nodes[n].values()
            if isinstance(p, ParameterABC)
        )


# =[PRIVATE FUNCTIONS]==================================================================================================


def _get_first_macro(root: int, G: nx.MultiDiGraph, T: nx.DiGraph) -> int:
    """Quick n' dirty."""
    return next((n for n in nx.dfs_preorder_nodes(T, root) if G.nodes[n]["_type"] == MACRO_NODE), None)


def _get_node_list(G: nx.classes.MultiDiGraph, *, root: int, type_: str | None) -> tuple:
    """Get all nodes, or some nodes through dfs"""
    if root is None:
        return tuple(n for n in G.nodes if type_ is None or G.nodes[n]["_type"] == type_)
    else:
        tree = make_digraph(tuple(G.nodes), tuple((u, v) for u, v, k in G.edges(data="_type") if k == FRAMEWORK))
        return tuple(n for n in nx.dfs_preorder_nodes(tree, root) if type_ is None or G.nodes[n]["_type"] == type_)


def fasten_subtree_parameters(node_reference: NodeReference):
    for p, n in (
        _
        for _ in get_all_parameters(node_reference.graph, node_reference.node, node_id=True)
        if isinstance(_[0], ParameterStructuralABC)
    ):
        p.fasten(NodeReference(node_reference.graph, n))


def discard_useless_components(G: nx.MultiDiGraph) -> None:
    """Removes unconnected and unreached components"""
    H = nx.Graph()
    H.add_edges_from(G.edges(keys=False))
    H.remove_node(NODE_ZERO)
    node_zero, first_tree = next((u, v) for u, v in G.edges(NODE_ZERO))
    H.add_edge(node_zero, first_tree)
    for nodes in list(nx.connected_components(H)):
        if NODE_ZERO not in nodes:
            G.remove_nodes_from(nodes)


def get_structure_tree(G: nx.MultiDiGraph) -> nx.DiGraph | None:
    tree = make_digraph(tuple(G.nodes), tuple((u, v) for u, v, k in G.edges(data="_type") if k == FRAMEWORK))
    if not nx.is_branching(tree) or not nx.is_weakly_connected(tree):
        return None
    return tree


def get_parent_frame_dictionary(genome: nx.MultiDiGraph) -> dict:
    @lru_cache(1024)
    def get_parent_frame_dictionary_cached(G, nodes_list) -> dict:
        tree = make_digraph(tuple(G.nodes), tuple((u, v) for u, v, k in G.edges(data="_type") if k == FRAMEWORK))
        assert nx.is_branching(tree) and nx.is_weakly_connected(tree), f"{PARANOIA_SYSTEM_ERROR}: Not a valid genome"
        parent_frames = dict()
        for node, path in nx.single_source_dijkstra_path(tree, NODE_ZERO).items():
            parent_frames[node] = tuple(G.nodes[n]['_selement'].__class__ for n in path)
        return parent_frames

    return get_parent_frame_dictionary_cached(genome, tuple(genome.nodes))


@lru_cache(1024)
def make_digraph(nodes, edges):
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
            if G.nodes[new_node]['_type'] == MACRO_NODE:
                subtree.append(new_node)
            else:
                queue.append(new_node)
    return subtree
