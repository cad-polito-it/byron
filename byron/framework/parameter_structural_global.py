# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
import functools

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
from functools import cache, lru_cache
from numbers import Number

import networkx as nx

from byron.user_messages import *
from byron.randy import rrandom
from byron.global_symbols import *
from byron.classes.node import NODE_ZERO

from byron.classes.parameter import ParameterStructuralABC
from byron.operators.graph_tools import *
from byron.classes.selement import SElement
from byron.tools.graph import *

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

        def __init__(self):
            super().__init__()
            # NOTE[GX] if target_frame is a string it works thanks to selement string magic!
            self._target_frame = target_frame

        def get_potential_targets(self, add_none=True):
            parent_frames = get_parent_frame_dictionary(self._node_reference.graph)
            if first_macro:
                # TODO: This code sucks
                targets = list()
                first_macros = set()
                for n, p in parent_frames.items():
                    if p[:-1] not in first_macros:
                        targets.append(n)
            else:
                targets = list(n for n, p in parent_frames.items() if target_frame in p)

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
            assert self.is_fastened, f"{PARANOIA_VALUE_ERROR}: Node is unfastened"

            # first try
            potential_targets = self.get_potential_targets()
            if strength == 1.0:
                target = rrandom.choice(potential_targets)
            else:
                target = rrandom.choice(potential_targets, self.value, sigma=strength)
            if target is None:
                # get_all_macros(G, root=f, data=False, node_id=True)
                new_node = unroll_selement(self._target_frame, self._node_reference.graph)
                self._node_reference.graph.add_edge(NODE_ZERO, new_node.node, _type=FRAMEWORK)
                initialize_subtree(new_node)
                if first_macro:
                    target = get_all_macros(new_node.graph, root=new_node.node, data=False, node_id=True)[0]
                    # TODO[GX]: Use the new get_dfs_subtree
                else:
                    target = new_node.node

            if not target:
                raise ByronOperatorFailure
            self.value = target
            for ccomp in tuple(nx.weakly_connected_components(self.graph)):
                if NODE_ZERO not in ccomp:
                    self.self.graph.remove_nodes_from(ccomp)

    if isinstance(target_frame, str):
        T._patch_info(name=f"GlobalReference['{target_frame}']")
    else:
        T._patch_info(name=f"GlobalReference[{target_frame}]")
    return T


def global_reference(
    target_frame: str | type[SElement], *, creative_zeal=0, first_macro: bool = False
) -> type[ParameterStructuralABC]:
    assert (
        isinstance(creative_zeal, int) or 0.0 <= creative_zeal <= 1.0
    ), f"ValueError: creative zeal is integer or 0 <= float <= 1: found {creative_zeal}"
    return _global_reference(target_frame=target_frame, first_macro=bool(first_macro), creative_zeal=creative_zeal)
