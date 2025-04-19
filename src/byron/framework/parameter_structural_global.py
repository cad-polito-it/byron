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
# v1 / April 2023 / Squillero (GX)

from functools import cache

import networkx as nx

from byron.classes.frame import MacroBunch
from byron.classes.node import NODE_ZERO
from byron.classes.node_reference import NodeReference
from byron.classes.parameter import ParameterStructuralABC
from byron.classes.selement import SElement
from byron.global_symbols import *
from byron.global_symbols import FRAMEWORK, PARANOIA_VALUE_ERROR
from byron.operators.graph_tools import *
from byron.randy import rrandom
from byron.tools.graph import *
from byron.tools.providers import *
from byron.user_messages import *

__all__ = ["global_reference"]


@cache
def _global_reference(
    *,
    target_name: str | None = None,
    target_frame: type[SElement] | None = None,
    first_macro: bool = True,
    creative_zeal: int | float = 0,
) -> type[ParameterStructuralABC]:
    class T(ParameterStructuralABC):
        __slots__ = ["_target_frame"]  # Preventing the automatic creation of __dict__

        def __init__(self):
            super().__init__()
            # NOTE[GX] if target_frame is a string it works thanks to selement string magic!
            self._target_frame = target_frame

        def get_potential_targets(self, T: nx.DiGraph):
            r"""
            Get potential targets for the global reference.

            Parameters
            ----------
            T :
                The structure tree of the inddividual with valid _path attributes.

            Returns
            -------
            List of potential targets for the global reference.
            """

            G = self._node_reference.graph
            provide_tags(G, '_path', '_typepath', force=True)
            targets = [
                (n, G.nodes[n]['_typepath'])
                for n in T.nodes
                if G.nodes[n]['_type'] == MACRO
                and target_frame in G.nodes[n]['_typepath']
                and not (
                    '_invalid_target' in G.nodes[n]['_selement'].EXTRA_PARAMETERS
                    and G.nodes[n]['_selement'].EXTRA_PARAMETERS['_invalid_target']
                )
            ]
            if first_macro:
                tmp = list()
                for n, p in targets:
                    idx = p.index(target_frame)
                    tmp.append((n, G.nodes[n]['_path'][idx]))
                targets = [c for i, c in enumerate(tmp) if c[1] not in {_[1] for _ in tmp[:i]}]

            return [t[0] for t in targets]

        def mutate(self, strength: float = 1.0) -> None:
            assert self.is_fastened, f"{PARANOIA_VALUE_ERROR}: Node is unfastened"

            G = self._node_reference.graph
            tree = get_structure(G)
            provide_tags(G, '_typepath')

            # first try -- if needed add None
            potential_targets = self.get_potential_targets(tree)
            if self.value in potential_targets:
                # Force mutation to be a mutation (ie. bring some change)
                potential_targets.remove(self.value)

            if not potential_targets and creative_zeal > 0:
                potential_targets = [None]
            elif isinstance(creative_zeal, int):
                # Add N = creative_zeal 'creation slots'
                potential_targets += [None] * creative_zeal
            elif rrandom.boolean(p_true=creative_zeal):
                # Force creation with p = creative_zeal
                potential_targets = [None]

            if potential_targets:
                # Don't use strength (not meaningful)
                target = rrandom.choice(potential_targets)
            else:
                target = None

            if target is None:
                # We need to create a new target
                # We don't need the first macro, let's see if we can grow a pool
                growable_nodes = [
                    (n, p)
                    for n, p in G.nodes(data='_typepath')
                    if self._target_frame in p
                    and isinstance(G.nodes[n]['_selement'], MacroBunch)
                    and G.nodes[n]['_selement'].SIZE[0] <= G.out_degree(n) < G.nodes[n]['_selement'].SIZE[1] - 1
                ]
                if growable_nodes:
                    node = rrandom.choice(growable_nodes)[0]
                    macros_in_bunch = list(get_successors(NodeReference(G, node)))
                    new_macro_type = rrandom.choice(G.nodes[node]['_selement'].POOL)
                    new_macro = unroll_selement(new_macro_type, G)

                    G.add_edge(node, new_macro.node, _type=FRAMEWORK)
                    initialize_subtree(new_macro)
                    if macros_in_bunch:
                        i = rrandom.random_int(0, len(macros_in_bunch))
                        set_successors_order(
                            NodeReference(G, node),
                            macros_in_bunch[:i] + [new_macro.node] + macros_in_bunch[i:],
                        )
                    target = new_macro
                else:
                    # The new target will be a new tree in the forest
                    new_node = unroll_selement(self._target_frame, self._node_reference.graph)
                    # TODO: check this self!!!!
                    self._node_reference.graph.add_edge(NODE_ZERO, new_node.node, _type=FRAMEWORK)
                    initialize_subtree(new_node)

                    new_tree = get_structure(G)
                    new_potential_targets = [
                        t for t in self.get_potential_targets(new_tree) if t not in potential_targets
                    ]
                    if self.value in new_potential_targets:
                        new_potential_targets.remove(self.value)
                    if new_potential_targets:
                        target = rrandom.choice(new_potential_targets)
                        # else, we have a problem... we didn't manage to create a suitable target

            if target is None:
                raise ByronOperatorFailure
            self.value = target

            # TODO[gx]: check this!?!?!?!?
            for ccomp in tuple(nx.weakly_connected_components(self.graph)):
                if NODE_ZERO not in ccomp:
                    self.graph.remove_nodes_from(ccomp)

    if isinstance(target_frame, str):
        T._patch_info(name=f"GlobalReference['{target_frame}']")
    else:
        T._patch_info(name=f"GlobalReference[{target_frame}]")
    return T


def global_reference(
    target_frame: str | type[SElement], *, creative_zeal=0, first_macro: bool = False
) -> type[ParameterStructuralABC]:
    assert isinstance(creative_zeal, int) or 0.0 <= creative_zeal <= 1.0, (
        f"ValueError: creative zeal is integer or 0 <= float <= 1: found {creative_zeal}"
    )
    return _global_reference(target_frame=target_frame, first_macro=bool(first_macro), creative_zeal=creative_zeal)
