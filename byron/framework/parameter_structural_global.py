# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of byron v0.1    #
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

from itertools import chain
from functools import cache
from numbers import Number

import networkx as nx

from byron.user_messages import *
from byron.randy import rrandom
from byron.global_symbols import *

from byron.classes.parameter import ParameterStructuralABC
from byron.operators.unroll import *
from byron.classes.node_reference import NodeReference
from byron.classes.frame import FrameABC

from byron.tools.graph import *
from byron.tools.names import canonize_name, _patch_class_info

__all__ = ["global_reference"]


@cache
def _global_reference(
    *,
    target_name: str | None = None,
    target_frame: type[FrameABC] | None = None,
    first_macro: bool = True,
    creative_zeal: Number = 0,
) -> type[ParameterStructuralABC]:
    class T(ParameterStructuralABC):
        __slots__ = ["_target_frame"]  # Preventing the automatic creation of __dict__

        if target_frame:

            def __init__(self):
                super().__init__()
                self._target_frame = target_frame

        else:

            def __init__(self):
                super().__init__()
                self._target_frame = FRAMEWORK_DIRECTORY[
                    canonize_name(target_name, tag="Frame", user=True, warn_duplicates=False)
                ]

        def get_potential_targets(self, suitable_frames: list | None = None):
            G = self._node_reference.graph
            if suitable_frames:
                suitable_frames_ = suitable_frames
            else:
                suitable_frames_ = [
                    n
                    for n in nx.dfs_preorder_nodes(G)
                    if G.nodes[n]["_type"] == FRAME_NODE and isinstance(G.nodes[n]["_selement"], self._target_frame)
                ]
            if first_macro:
                targets = list(
                    chain.from_iterable(
                        get_all_macros(G, root=f, data=False, node_id=True)[:1] for f in suitable_frames_
                    )
                )
            else:
                targets = list(
                    chain.from_iterable(get_all_macros(G, root=f, data=False, node_id=True) for f in suitable_frames_)
                )

            if suitable_frames:
                pass
            elif not targets and creative_zeal > 0:
                targets = [None]
            elif isinstance(creative_zeal, int):
                # Add N = creative_zeal 'creation slots'
                targets += [None] * creative_zeal
            elif rrandom.boolean(p_true=creative_zeal):
                # Force creation with p = creative_zeal
                targets = [None]

            if not targets:
                raise GeneticOperatorFail
            return targets

        def mutate(self, strength: float = 1.0, node_reference: NodeReference | None = None, *args, **kwargs) -> None:
            if node_reference is not None:
                self.fasten(node_reference)

            # first try
            if strength == 1.0:
                target = rrandom.sigma_choice(self.get_potential_targets())
            else:
                target = rrandom.sigma_choice(self.get_potential_targets(), self.value, strength)
            if target is None:
                new_node_reference = unroll_selement(self._target_frame, self._node_reference.graph)
                self._node_reference.graph.add_edge(NODE_ZERO, new_node_reference.node, _type=FRAMEWORK)
                initialize_subtree(new_node_reference)

                # second and last try
                if strength == 1.0:
                    target = rrandom.sigma_choice(self.get_potential_targets([new_node_reference.node]))
                else:
                    target = rrandom.sigma_choice(
                        self.get_potential_targets([new_node_reference.node]), self.value, strength
                    )

            if not target:
                raise GeneticOperatorFail
            self._node_reference.graph.add_edge(self._node_reference.node, target, key=self.key, _type=LINK)

    _patch_class_info(T, f"GlobalReference[{target_frame.__name__}]", tag="parameter")
    return T


def global_reference(
    target_frame: str | type[FrameABC], *, creative_zeal=0, first_macro: bool = False
) -> type[ParameterStructuralABC]:
    assert (
        isinstance(creative_zeal, int) or 0 < creative_zeal < 1
    ), f"ValueError: creative zeal is integer or 0 <= float < 1: found {creative_zeal}"
    if isinstance(target_frame, str):
        return _global_reference(target_name=target_frame, first_macro=bool(first_macro), creative_zeal=creative_zeal)
    else:
        return _global_reference(target_frame=target_frame, first_macro=bool(first_macro), creative_zeal=creative_zeal)
