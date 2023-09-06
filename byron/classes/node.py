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

__all__ = ['Node', 'NODE_ZERO']

import networkx as nx


class Node(int):
    r"""Simple helper to guarantee Node ids uniqueness"""
    __slots__ = []
    __LAST_BYRON_NODE = 0

    def __new__(cls, node_id: int or None = None):
        if node_id is not None:
            return int.__new__(cls, node_id)
        Node.__LAST_BYRON_NODE += 1
        return int.__new__(cls, Node.__LAST_BYRON_NODE)

    def __repr__(self):
        return f'n{int(self)}'

    @staticmethod
    def reset_labels(G: nx.MultiDiGraph) -> None:
        """Set Graph node labels to unique numbers"""
        from byron.tools.graph import fasten_subtree_parameters
        from byron.classes.node_reference import NodeReference

        new_labels = {k: Node() for k in G.nodes if k != NODE_ZERO}
        nx.relabel_nodes(G, new_labels, copy=False)
        for k, v in new_labels.items():
            G.nodes[v]['%old_label'] = k
        fasten_subtree_parameters(NodeReference(G, NODE_ZERO))

    @staticmethod
    def relabel_to_canonic_form(G: nx.MultiDiGraph) -> nx.MultiDiGraph:
        """Set Graph node labels to "canonic" labels"""
        from byron.tools.graph import fasten_subtree_parameters
        from byron.classes.node_reference import NodeReference

        new_labels = {k: Node(i) for i, k in enumerate(G.nodes)}
        G = nx.relabel_nodes(G, new_labels, copy=True)
        for k, v in new_labels.items():
            G.nodes[v]['%old_label'] = k
        fasten_subtree_parameters(NodeReference(G, NODE_ZERO))
        return G


NODE_ZERO = Node(0)
