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
# v1 / April 2023 / Squillero (GX)

__all__ = ["NodeView"]

from itertools import chain
import networkx as nx

from byron.global_symbols import *
from byron.user_messages import *

from byron.classes.value_bag import ValueBag
from byron.classes.node_reference import NodeReference

from byron.tools.graph import *


class NodeView:
    """A lazy, read-only view to almost all node information."""

    _genome: nx.classes.MultiDiGraph
    _node_id: int
    framework_tree: nx.classes.DiGraph

    def __init__(
        self,
        *args: NodeReference,
    ):
        if len(args) == 1:
            node_ref = args[0]
        elif len(args) == 2:
            node_ref = NodeReference(args[0], args[1])
        else:
            assert 1 <= len(args) <= 2, f"Expected NodeRef or (Graph, node)"
        assert check_valid_type(node_ref, NodeReference)
        self.__dict__["_ref"] = node_ref
        self.__dict__["_genome"] = node_ref.graph
        self.__dict__["_node_id"] = node_ref.node

    @property
    def genome(self) -> nx.classes.MultiDiGraph:
        return self._genome

    @property
    def id(self) -> int:
        return self._node_id

    def __str__(self) -> str:
        return f"n{self._node_id}"

    def __getattr__(self, item):
        id, G = self._node_id, self._genome
        if item == "G":  # Networkx MultiDiGraph (deprecated)
            deprecation("Direct access to the internal Networkx MultiDiGraph is generally considered a bad idea")
            self.__dict__[item] = G
        elif item == "attributes":  # ValueBag with all node attributes
            self.__dict__[item] = ValueBag(G.nodes[id])
        elif item == "framework_tree":  # Framework tree from the full genome
            tree = nx.DiGraph()
            tree.add_edges_from((x, y) for x, y, _ in G.edges(data=FRAMEWORK, keys=False))
            self.__dict__[item] = tree
        elif item == "predecessor":  # Predecessor in the tree framework
            self.__dict__[item] = NodeView(NodeReference(G, get_predecessor(NodeReference(G, id))))
        elif item == "successors":
            # Successors NodeView in the tree framework
            self.__dict__[item] = list(NodeView(NodeReference(G, v)) for v in get_successors(NodeReference(G, id)))
        elif item == "links":
            # All incoming and outgoing edges not in the tree framework
            self.__dict__[item] = sorted(
                (u, v, k)
                for u, v, k in chain(G.out_edges(id, data="_type"), G.in_edges(id, data="_type"))
                if k != FRAMEWORK
            )
        elif item == "index":
            # Index of a node id among the successors
            return lambda n: self._successor_ids.index(n)
        elif item == "name":
            # Name of the SElement inside a node
            self.__dict__[item] = G.nodes[id]["_selement"].__class__.__name__
        elif item == "path":
            # Tuple of the path from top-frame to node
            path = list()
            node = id
            while node > 0:
                path.append(node)
                node = next(u for u, v, k in G.in_edges(node, data="_type") if k == FRAMEWORK)
            path.append(node)
            self.__dict__[item] = tuple(reversed(path))
        elif item == "pathname":
            return ".".join(f"n{_}" for _ in self.path[1:])
        elif item == "out_degree":
            # Global out degree (fanout)
            self.__dict__[item] = len(G.out_edges(id, data="_type"))
        elif item == "in_degree":
            # Global in degree (fanin)
            self.__dict__[item] = len(G.in_edges(id, data="_type"))
        elif item.endswith("_out_degree"):
            # Out degree from a specific type of edges
            tag, _ = item.split("_", maxsplit=1)
            self.__dict__[item] = sum(1 for u, v, k in G.out_edges(id, data="_type") if k == tag)
        elif item.endswith("_in_degree"):
            # In degree from a specific type of edges
            tag, _ = item.split("_", maxsplit=1)
            self.__dict__[item] = sum(1 for u, v, k in G.in_edges(id, data="_type") if k == tag)
        elif item == "all_edges":
            self.__dict__[item] = sorted(
                [(u, v, k) for u, v, k in G.in_edges(id, data="_type")]
                + [(u, v, k) for u, v, k in G.out_edges(id, data="_type")]
            )
        else:
            raise KeyError(f"Unknown property: {item!r}")

        return self.__dict__[item]

    def __setattr__(self, key, value):
        raise NotImplementedError(f"{self!r} is read only.")
