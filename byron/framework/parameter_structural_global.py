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

from itertools import chain
from functools import cache
from numbers import Number

import networkx as nx

from byron.user_messages import *
from byron.randy import rrandom
from byron.global_symbols import *

from byron.classes.parameter import ParameterStructuralABC
from byron.operators.unroll import *
from byron.classes.selement import SElement
from byron.tools.names import *

from byron.tools.graph import *
from byron.tools.names import canonize_name, _patch_class_info

__all__ = ["global_reference"]


@cache
def _global_reference(
    *,
    target_name: str | None = None,
    target_frame: type[SElement] | None = None,
    first_macro: bool = True,
    creative_zeal: Number = 0,
) -> type[ParameterStructuralABC]:
    class T(ParameterStructuralABC):
        __slots__ = ["_target_frame"]  # Preventing the automatic creation of __dict__

        if isinstance(target_frame, str):

            def __init__(self):
                super().__init__()
                self._target_frame = FRAMEWORK_DIRECTORY[target_frame]

        else:

            def __init__(self):
                super().__init__()
                self._target_frame = target_frame

        def get_potential_targets(self, add_none=True):
            G = self._node_reference.graph
            suitable_frames = [
                n for n in nx.dfs_preorder_nodes(G) if G.nodes[n]['_selement'].__class__ == self._target_frame
            ]
            if first_macro:
                targets = list(
                    chain.from_iterable(
                        get_all_macros(G, root=f, data=False, node_id=True)[:1] for f in suitable_frames
                    )
                )
            else:
                targets = list(
                    chain.from_iterable(get_all_macros(G, root=f, data=False, node_id=True) for f in suitable_frames)
                )

            if not add_none:
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
                raise ByronOperatorFailure
            return targets

        def mutate(self, strength: float = 1.0) -> None:
            assert self.is_fastened, f"{PARANOIA_VALUE_ERROR}: node is unfastened"

            # first try
            potential_targets = self.get_potential_targets()
            if strength == 1.0:
                target = rrandom.sigma_choice(potential_targets)
            else:
                target = rrandom.sigma_choice(potential_targets, self.value, strength)
            if target is None:
                new_node_reference = unroll_selement(self._target_frame, self._node_reference.graph)

                parent = NODE_ZERO

                self._node_reference.graph.add_edge(parent, new_node_reference.node, _type=FRAMEWORK)
                initialize_subtree(new_node_reference)

                # second and last try
                if strength == 1.0:
                    target = rrandom.sigma_choice(self.get_potential_targets(add_none=False))
                else:
                    target = rrandom.sigma_choice(self.get_potential_targets(add_none=False), self.value, strength)

            if not target:
                raise ByronOperatorFailure
            self.value = target
            for ccomp in list(nx.weakly_connected_components(self.graph)):
                if NODE_ZERO not in ccomp:
                    self.self.graph.remove_nodes_from(ccomp)

    if isinstance(target_frame, str):
        _patch_class_info(T, f"GlobalReference['{target_frame}']", tag="parameter")
    else:
        _patch_class_info(T, f"GlobalReference[{target_frame.__name__}]", tag="parameter")
    return T


def global_reference(
    target_frame: str | type[SElement], *, creative_zeal=0, first_macro: bool = False
) -> type[ParameterStructuralABC]:
    assert (
        isinstance(creative_zeal, int) or 0.0 <= creative_zeal <= 1.0
    ), f"ValueError: creative zeal is integer or 0 <= float <= 1: found {creative_zeal}"
    return _global_reference(target_frame=target_frame, first_macro=bool(first_macro), creative_zeal=creative_zeal)
