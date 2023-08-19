# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
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

# NOTE[GX]: This file contains code that some programmer may find upsetting

__all__ = ['Individual', 'Lineage', 'Age']

from typing import Any, Callable, Optional
from itertools import chain
from copy import deepcopy, copy
import operator

import networkx as nx

from byron.user_messages import *
from byron.user_messages.messaging import logger as byron_logger
from byron.global_symbols import *
from byron.tools.graph import *

if matplotlib_available:
    import matplotlib.pyplot as plt

from byron.global_symbols import *
from byron.classes.byron import Byron
from byron.classes.dump import *
from byron.classes.fitness import FitnessABC
from byron.classes.paranoid import Paranoid
from byron.classes.value_bag import ValueBag
from byron.classes.node_reference import NodeReference
from byron.classes.node_view import NodeView
from byron.classes.macro import Macro
from byron.classes.frame import FrameABC
from byron.classes.parameter import ParameterABC, ParameterStructuralABC
from byron.classes.readymade_macros import MacroZero


@dataclass(frozen=True, slots=True)
class Lineage:
    operator: Optional[Callable]
    parents: tuple

    def __str__(self):
        parents = list()
        for p in self.parents:
            try:
                parents.append(str(p))
            except ReferenceError:
                # ☠ ⚰ (coffin) ⚱ (urn) 💀 ✝
                parents.append("☠")

        return self.operator.__name__ + "(" + ", ".join(parents) + ")"


@dataclass(slots=True)
class Age:
    birth: int | None = None
    apparent_age: int = 0

    def __iadd__(self, generations):
        self.apparent_age += generations

    def __str__(self):
        return f'⚝ {self.birth}' + (f' (⌛ {self.apparent_age})' if self.apparent_age else '')


class Individual(Paranoid):
    """
    An individual, that is, a genotype and its fitness

    An Individual is a forest stored in a NetworkX MultiDiGraph, each tree representing a chunk of code,
    plus the framework definition to check its structural correctness.

    All tree root nodes are connected to "Node Zero" -- thus, technically, it is not a forest, but a single tree :$

    Edges of `kind=FRAMEWORK` store the structure, while edges of `kind=LINK` store parameters and other references
    -- thus, technically, the individual is not even a tree, but a weekly-connected multigraph that may contains
    loops ://)

    Individuals are created by passing a reference to the top frame. Please note that frames are types, and their
    instances (ie. the objects) are stored as attributes inside the tree nodes.

    Individuals are managed by a `Population` class.
    """

    __COUNTER: int = 0

    _genome: nx.classes.MultiDiGraph
    _fitness: FitnessABC | None
    _lineage: Lineage | None
    _age: Age
    _str: str

    BYRON: Byron = Byron()

    from ._individual_as import as_forest, as_lgp, _draw_forest, _draw_multipartite

    def __init__(self, top_frame: type[FrameABC]) -> None:
        Individual.__COUNTER += 1
        self._id = Individual.__COUNTER
        self._genome = nx.MultiDiGraph(node_count=NODE_ZERO + 1, top_frame=top_frame)
        self._genome.add_node(NODE_ZERO, _selement=MacroZero(), _type=MACRO_NODE)
        self._fitness = None
        self._str = ""
        self._lineage = None
        self._age = Age()

    def __del__(self) -> None:
        self._genome.clear()  # NOTE[GX]: I guess it's useless...

    def __str__(self):
        return f"𝕚{self._id}"

    def __eq__(self, other) -> bool:
        return (
            type(self) == type(other)
            and self._fitness == other._fitness
            and nx.isomorphism.is_isomorphic(
                self._genome, other._genome, node_match=operator.eq, edge_match=operator.eq
            )
        )

    def __hash__(self) -> int:
        return hash(self._id)

    # PROPERTIES

    @property
    def id(self) -> int:
        return self._id

    @property
    def is_finalized(self) -> bool:
        return self._fitness is not None

    @property
    def valid(self) -> bool:
        return all(
            self.genome.nodes[n]["_selement"].is_valid(NodeView(NodeReference(self.genome, n)))
            for n in nx.dfs_preorder_nodes(self.genome)
        )

    @property
    def clone(self) -> "Individual":
        scratch = self._fitness, self._lineage
        self._fitness, self._lineage = None, None
        I = deepcopy(self)
        I.__class__ = Individual
        Individual.__COUNTER += 1
        I._id = Individual.__COUNTER
        self._fitness, self._lineage = scratch
        I._age = Age()
        I._lineage = Lineage(None, (self,))
        return I

    @property
    def dfs_nodes(self) -> list[int]:
        """Return all node indexes in reliable order."""
        return list(nx.dfs_preorder_nodes(self.structure_tree))

    @property
    def top_frame(self) -> FrameABC:
        return self._genome.graph['top_frame']

    @property
    def macros(self) -> list[Macro]:
        """Return all macro instances in unreliable order."""
        return [
            self._genome.nodes[n]["_selement"] for n in self._genome if self._genome.nodes[n]["_type"] == MACRO_NODE
        ]

    @property
    def frames(self) -> list[FrameABC]:
        """Return all frame instances in unreliable order."""
        return [
            self._genome.nodes[n]["_selement"] for n in self._genome if self._genome.nodes[n]["_type"] == FRAME_NODE
        ]

    @property
    def parameters(self) -> list[ParameterABC]:
        """Return all parameter instances in unreliable order."""
        return [p for n in self._genome for p in self._genome.nodes[n].values() if isinstance(p, ParameterABC)]

    @property
    def G(self) -> nx.classes.MultiDiGraph:
        """Individual's underlying NetworkX MultiDiGraph."""
        # TODO DeprecationWarning?
        return self._genome

    @property
    def genome(self) -> nx.classes.MultiDiGraph:
        """Individual's genome (ie. the underlying NetworkX MultiDiGraph)."""
        # TODO: Add paranoia check?
        return self._genome

    @property
    def structure_tree(self) -> nx.classes.DiGraph:
        """A tree with the structure tree of the individual (ie. only edges of `kind=FRAMEWORK`)."""

        tree = nx.DiGraph()
        tree.add_nodes_from(self._genome.nodes)
        tree.add_edges_from((u, v) for u, v, k in self._genome.edges(data="_type") if k == FRAMEWORK)
        assert nx.is_branching(tree) and nx.is_weakly_connected(
            tree
        ), f"{PARANOIA_VALUE_ERROR}: Structure of {self!r} is not a valid tree"
        return tree

    @property
    def lineage(self):
        return self._lineage

    @property
    def age(self):
        """The age of the individual"""
        return self._age

    @age.setter
    def age(self, value: int):
        assert value >= 0
        self._age = value

    @property
    def fitness(self) -> FitnessABC:
        """The fitness of the individual."""
        assert self.is_finalized, f"{PARANOIA_VALUE_ERROR}: Individual not marked as final, fitness value not set"
        return self._fitness

    def _check_fitness(self, value) -> bool:
        check_valid_types(value, FitnessABC)
        assert (
            not self.is_finalized
        ), f"{PARANOIA_VALUE_ERROR}: Individual marked as final, fitness value already set to {self._fitness}"
        return True

    @fitness.setter
    def fitness(self, value: FitnessABC) -> None:
        """Set the fitness of the individual and update operator stats"""
        assert self._check_fitness(value)
        self._fitness = value
        if any(value >> i.fitness for i in self._lineage.parents) and any(
            value >> i.fitness or not value.is_distinguishable(i.fitness) for i in self.lineage.parents
        ):
            self._lineage.operator.stats.successes += 1
        elif any(value << i.fitness for i in self.lineage.parents) and any(
            value << i.fitness or not value.is_distinguishable(i.fitness) for i in self.lineage.parents
        ):
            self._lineage.operator.stats.failures += 1
        logger.debug(f"Individual: Fitness of {self} is {value}")

        # Yeuch!
        from .frozen_individual import FrozenIndividual

        self.__class__ = FrozenIndividual

    #######################################################################
    # PUBLIC METHODS
    def run_paranoia_checks(self) -> bool:
        assert self.valid, f"{PARANOIA_VALUE_ERROR}: Individual {self!r} is not valid"

        # ==[check genome (structural)]======================================
        assert self.genome == self._genome, f"{PARANOIA_VALUE_ERROR}: Panic: genome != _genome"
        assert nx.is_weakly_connected(
            self._genome
        ), f"{PARANOIA_VALUE_ERROR}: genome of {self!r} is not a connected graph"

        G = nx.MultiDiGraph()
        G.add_edges_from(self.G.edges)
        G.remove_node(NODE_ZERO)
        assert (
            sum(1 for _ in nx.weakly_connected_components(G)) == 1
        ), f"{PARANOIA_TYPE_ERROR}: individual is not a weakly connected graph"

        assert nx.is_branching(self.structure_tree) and nx.is_weakly_connected(
            self.structure_tree
        ), f"{PARANOIA_VALUE_ERROR}: structure_tree of {self!r} is not a tree"
        assert (self._fitness is None and not self.is_finalized) or (
            self._fitness is not None and self.is_finalized
        ), f"Value Error (paranoia check): Mismatch fitness and is_finalized"

        # ==[check edges (semantic)]=========================================
        edges = self._genome.edges(keys=True, data=True)
        assert all("_type" in d for u, v, k, d in edges), "ValueError (paranoia check): missing '_type' attribute"
        assert all(
            d["_type"] != FRAMEWORK or len(d) == 1 for u, v, k, d in edges
        ), "ValueError (paranoia check): unknown attribute in tree edge"
        tree_edges = [(u, v) for u, v, k, d in edges if d["_type"] == FRAMEWORK]
        assert len(tree_edges) == len(set(tree_edges)), "ValueError (paranoia check): duplicated framework edge"

        # ==[check nodes (semantic)]=========================================
        assert all(
            n < self._genome.graph["node_count"] for n in self._genome
        ), f"{PARANOIA_VALUE_ERROR}: invalid 'node_count' attribute ({self._genome.graph['node_count']})"

        assert all(
            '_selement' in d for n, d in self._genome.nodes(data=True)
        ), f"{PARANOIA_VALUE_ERROR}: missing '_selement'"
        assert all(
            (isinstance(d['_selement'], Macro) and d['_type'] == 'macro')
            or (isinstance(d['_selement'], FrameABC) and d['_type'] == 'frame')
            for n, d in self._genome.nodes(data=True)
        )
        assert isinstance(self._genome.nodes[0]['_selement'], MacroZero), f"{PARANOIA_TYPE_ERROR}: incorrect NodeZero"

        # ==[check structural parameter]=====================================
        assert all(
            p._node_reference == NodeReference(self._genome, n)
            for n in self._genome
            for p in self._genome.nodes[n].values()
            if isinstance(p, ParameterStructuralABC)
        ), f"{PARANOIA_VALUE_ERROR}: Incorrect node_reference in structural parameter"

        structural_edges = [(u, v, k) for u, v, k, d in self._genome.edges(data='_type', keys=True) if d == LINK]
        assert len(structural_edges) == len(set(k for u, v, k in structural_edges)), (
            f"{PARANOIA_VALUE_ERROR}: found duplicated keys in structural edges: "
            + f"{set(x for i, x in enumerate(list(k for u, v, k in structural_edges)) if i != list(k for u, v, k in structural_edges).index(x))}"
        )
        structural_parameters = [p for p in self.parameters if isinstance(p, ParameterStructuralABC)]
        assert len(structural_edges) == len(structural_parameters), (
            f"{PARANOIA_VALUE_ERROR}: inconsistent number of structural edges: "
            + f"found {len(structural_edges)}, expecting {len(structural_parameters)}"
        )
        assert set(k for u, v, k in structural_edges) == set(
            p._key for p in structural_parameters
        ), f"{PARANOIA_VALUE_ERROR}: inconsistent keys in structural edges"

        return True

    def describe(
        self,
        *,
        include_fitness: bool = True,
        include_structure: bool = True,
        include_age: bool = True,
        include_lineage: bool = True,
        max_recursion: int = 0,
        _indent_level: str = "",
    ):
        desc = str(self)
        delem = list()
        if include_fitness:
            delem.append(f"fitness: {self.fitness}")
        if include_structure:
            node_types = list(t for n, t in self.G.nodes(data="_type"))
            n_nodes = len(self.G)
            n_macros = node_types.count(MACRO_NODE) - 1
            n_frames = node_types.count(FRAME_NODE)
            n_links = sum(True for _, _, k in self.G.edges(data="_type") if k != FRAMEWORK)
            n_params = sum(
                True
                for p in chain.from_iterable(
                    self.G.nodes[n]["_selement"].parameter_types.items()
                    for n in self.G
                    if self.G.nodes[n]["_type"] == MACRO_NODE
                )
            )
            delem.append(
                f"""{n_frames} frame{'s' if n_frames != 1 else ''} and {n_macros} macro{'s' if n_frames != 1 else ''}"""
                + f""" ({n_params:,} parameter{'s' if n_params != 1 else ''} total"""
                + f""", {n_links:,} structural)"""
            )
        if include_age:
            delem.append(str(self.age))
        if include_lineage:
            delem.append(str(self.lineage))
        descr = f"""{_indent_level}{desc} ⇨ {' / '.join(delem)}"""
        if max_recursion is None or max_recursion > 0:
            if max_recursion is not None:
                max_recursion -= 1
            for p in self.lineage.parents:
                try:
                    descr += "\n" + p.describe(
                        include_fitness=include_fitness,
                        include_structure=include_structure,
                        include_lineage=include_lineage,
                        max_recursion=max_recursion,
                        _indent_level=_indent_level + "  ",
                    )
                except ReferenceError:
                    pass
        return descr

    def discard_useless_components(self):
        G = nx.MultiDiGraph()
        G.add_edges_from(self.G.edges)
        G.remove_node(NODE_ZERO)
        u, v = next((u, v) for u, v in self.G.edges(0))
        G.add_edge(u, v)
        for ccomp in list(nx.weakly_connected_components(G)):
            if NODE_ZERO not in ccomp:
                self.G.remove_nodes_from(ccomp)

    def dump(self, extra_parameters: dict) -> str:
        # =[Flatten the graph into a list of nodes]==========================
        tree = nx.DiGraph()
        tree.add_nodes_from(self._genome.nodes)
        tree.add_edges_from((u, v) for u, v, k in self._genome.edges(data="_type") if k == FRAMEWORK)

        for node in list(v for _, v in tree.edges(NODE_ZERO) if self.genome.nodes[v]['_selement'].FORCED_PARENT):
            target = self.genome.nodes[node]['_selement'].FORCED_PARENT
            tree.remove_edge(NODE_ZERO, node)
            parent = next(n for n, f in self.genome.nodes(data='_selement') if f.__class__ == target)
            tree.add_edge(parent, node)

        frame_list = Individual._recursive_flatten_frames(
            NodeReference(self.genome, NODE_ZERO), tree, extra_parameters, tuple(), list()
        )

        # =[Let's dump it]===================================================
        phenotype = ''
        for nr, path in frame_list:
            local_parameters = copy(extra_parameters)
            for p in path:
                local_parameters |= p.EXTRA_PARAMETERS
            local_parameters |= {'_node': NodeView(nr)}
            local_parameters |= {'_byron': Individual.BYRON}
            local_parameters |= nr.graph.nodes[nr.node]

            # --[node]-------------------------------------------------------
            bag = ValueBag(local_parameters)
            node_str = "{_text_before_node}".format(**bag)
            if nr.graph.in_degree(nr.node) > 1:
                node_str += bag['_label'].format(**bag)
            if nr.graph.nodes[nr.node]['_type'] == MACRO_NODE:
                node_str += '{_text_before_macro}'.format(**bag)
                node_str += nr.graph.nodes[nr.node]['_selement'].dump(bag)
                if bag["$dump_node_info"]:
                    if node_str:
                        node_str += '  '
                    node_str += '{_comment} 🖋 {_node.pathname} ➜ {_node.name}'.format(**bag)
                node_str += "{_text_after_macro}".format(**bag)
            elif nr.graph.nodes[nr.node]["_type"] == FRAME_NODE:
                node_str += "{_text_before_frame}".format(**bag)
                if bag["$dump_node_info"]:
                    node_str += "{_comment} 🖋 {_node.pathname} ➜ {_node.name}{_text_after_macro}".format(**bag)
                node_str += "{_text_after_frame}".format(**bag)
            node_str += "{_text_after_node}".format(**bag)
            # ---------------------------------------------------------------

            if not bag['$omit_from_dump']:
                phenotype += node_str
        # ===================================================================

        return phenotype

    @staticmethod
    def _recursive_flatten_frames(
        nr: NodeReference, T: nx.DiGraph, extra_parameters: dict, path: tuple, dump: list
    ) -> list:
        local_parameters = copy(extra_parameters)
        local_parameters |= nr.graph.nodes[nr.node]['_selement'].EXTRA_PARAMETERS

        path = tuple(list(path) + [nr.graph.nodes[nr.node]['_selement']])
        dump.append((NodeReference(nr.graph, nr.node), path))
        for n in [v for u, v in T.out_edges(nr.node)]:
            Individual._recursive_flatten_frames(NodeReference(nr.graph, n), T, local_parameters, path, dump)

        return dump

    @staticmethod
    def _dump_node_recursive(nr: NodeReference, T: nx.DiGraph, extra_parameters: dict, dump: str):
        local_parameters = extra_parameters | nr.graph.nodes[nr.node]
        local_parameters |= {'_node': NodeView(nr)}
        local_parameters |= {'_byron': Individual.BYRON}
        local_parameters |= nr.graph.nodes[nr.node]['_selement'].EXTRA_PARAMETERS

        # ==[NODE]============================================================
        bag = ValueBag(local_parameters)
        node_str = "{_text_before_node}".format(**bag)
        if nr.graph.in_degree(nr.node) > 1:
            node_str += bag['_label'].format(**bag)
        if nr.graph.nodes[nr.node]['_type'] == MACRO_NODE:
            node_str += '{_text_before_macro}'.format(**bag)
            node_str += nr.graph.nodes[nr.node]['_selement'].dump(bag)
            if bag["$dump_node_info"]:
                node_str += "  {_comment} 🖋 {_node.pathname} ➜ {_node.name}".format(**bag)
            node_str += "{_text_after_macro}".format(**bag)
        elif nr.graph.nodes[nr.node]["_type"] == FRAME_NODE:
            node_str += "{_text_before_frame}".format(**bag)
            if bag["$dump_node_info"]:
                node_str += "{_comment} 🖋 {_node.pathname} ➜ {_node.name}{_text_after_macro}".format(**bag)
            node_str += "{_text_after_frame}".format(**bag)
        node_str += "{_text_after_node}".format(**bag)
        # ====================================================================

        dump += node_str
        for n in [v for u, v in T.out_edges(nr.node)]:
            dump = Individual._dump_node_recursive(NodeReference(nr.graph, n), T, local_parameters, dump)
        return dump
