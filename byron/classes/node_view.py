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

__all__ = ["NodeView"]

import dataclasses
from dataclasses import dataclass
from functools import cached_property

import networkx as nx

from byron.global_symbols import *
from byron.user_messages import *
from byron.classes.value_bag import ValueBag
from byron.classes.node_reference import NodeReference
from byron.classes.selement import SElement
from byron.classes.parameter import ParameterABC

from byron.tools.graph import *

# NOTE[GX]: Rewritten almost from scratch taking advantage of 'dataclasses' (py>=3.7) and
# '@cached_property' (py>=3.8)


@dataclass(frozen=True, slots=False)
class NodeView:
    """A lazy, read-only view to almost all node information."""

    ref: NodeReference

    def __str__(self) -> str:
        return f"n{self.node}"

    @property
    def graph(self) -> nx.classes.MultiDiGraph:
        return self.ref.graph

    @property
    def node(self) -> int:
        return self.ref.node

    @property
    def selement(self) -> SElement:
        return self.ref.graph.nodes[self.ref.node]['_selement']

    @property
    def type_(self) -> type:
        return self.ref.graph.nodes[self.ref.node]['_selement'].__class__

    @property
    def node_type(self) -> type:
        return self.ref.graph.nodes[self.ref.node]['_type']

    @property
    def path_string(self) -> str:
        return ".".join(f"{nv}" for nv in self.path[1:])

    @cached_property
    def node_attributes(self) -> ValueBag:
        return dict(self.ref.graph.nodes[self.ref.node])

    @cached_property
    def p(self) -> ValueBag:
        return ValueBag(
            {k: v.value for k, v in self.ref.graph.nodes[self.ref.node].items() if isinstance(v, ParameterABC)}
        )

    @cached_property
    def structure_tree(self) -> nx.DiGraph:
        tree = nx.DiGraph()
        tree.add_nodes_from(self.ref.graph.nodes)
        tree.add_edges_from((u, v) for u, v, k in self.ref.graph.edges(data="_type") if k == FRAMEWORK)
        return tree

    @cached_property
    def predecessor(self) -> 'NodeView':
        """NodeView of the predecessor in the structure tree"""
        predecessor = next((u for u, v, k in self.ref.graph.in_edges(self.ref.node, data="_type") if k == FRAMEWORK), 0)
        return NodeView(NodeReference(self.ref.graph, predecessor))

    @cached_property
    def successors(self) -> list['NodeView']:
        """NodeView of all direct successors in the structure tree"""
        return [
            NodeView(NodeReference(self.ref.graph, v))
            for u, v, d in self.ref.graph.out_edges(self.ref.node, data="_type")
            if d == FRAMEWORK
        ]

    @cached_property
    def path(self) -> list['NodeView']:
        """List of NodeView of the nodes in the path from top-frame to node"""
        path = list()
        node = self.ref.node
        while node > 0:
            path.append(NodeView(NodeReference(self.ref.graph, node)))
            node = next(u for u, v, k in self.ref.graph.in_edges(node, data="_type") if k == FRAMEWORK)
        path.append(NodeView(NodeReference(self.ref.graph, node)))
        return list(reversed(path))

    @cached_property
    def out_degree(self):
        """Number of successors in the structure tree"""
        return sum(1 for u, v, k in self.ref.graph.out_edges(self.ref.node, data="_type") if k == FRAMEWORK)

    @property
    def fields(self):
        return sorted(k for k in self.__dir__() if k[0] != '_')


# class Old_NodeView:
#        elif item == "links":
#
#            self.__dict__[item] = sorted(
#                (u, v, k)
#                for u, v, k in chain(G.out_edges(id, data="_type"), G.in_edges(id, data="_type"))
#                if k != FRAMEWORK
#            )
#        elif item == "index":
#            # Index of a node id among the successors
#            return lambda n: self._successor_ids.index(n)
#        elif item == "name":
#            # Name of the SElement inside a node
#            self.__dict__[item] = G.nodes[id]["_selement"].__class__.__name__
#        elif item == "pathname":
#            return ".".join(f"n{_}" for _ in self.path[1:])
#        elif item == "out_degree":
#            # Global out degree (fanout)
#            self.__dict__[item] = len(G.out_edges(id, data="_type"))
#        elif item == "in_degree":
#            # Global in degree (fanin)
#            self.__dict__[item] = len(G.in_edges(id, data="_type"))
#        elif item.endswith("_out_degree"):
#            # Out degree from a specific type of edges
#            tag, _ = item.split("_", maxsplit=1)
#            self.__dict__[item] = sum(1 for u, v, k in G.out_edges(id, data="_type") if k == tag)
#        elif item.endswith("_in_degree"):
#            # In degree from a specific type of edges
#            tag, _ = item.split("_", maxsplit=1)
#            self.__dict__[item] = sum(1 for u, v, k in G.in_edges(id, data="_type") if k == tag)
#        elif item == "all_edges":
#            self.__dict__[item] = sorted(
#                [(u, v, k) for u, v, k in G.in_edges(id, data="_type")]
#                + [(u, v, k) for u, v, k in G.out_edges(id, data="_type")]
#            )
#        else:
#            raise KeyError(f"Unknown property: {item!r}")
#
#        return self.__dict__[item]
#
#    def __setattr__(self, key, value):
#        raise NotImplementedError(f"{self!r} is read only.")
#
