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
# v1 / August 2023 / Squillero (GX)

__all__ = ['provide_tags']

import networkx as nx

from byron.classes.node import NODE_ZERO
from byron.global_symbols import ATTRIBUTE_PROVIDERS
from byron.tools.graph import get_structure
from byron.user_messages.checks import PARANOIA_VALUE_ERROR


def calculate_paths(G: nx.MultiDiGraph):
    T = get_structure(G)
    for node, path in nx.single_source_dijkstra_path(T, NODE_ZERO).items():
        G.nodes[node]['_path'] = tuple(G.nodes[n]['_selement'] for n in path)
        G.nodes[node]['_typepath'] = tuple(G.nodes[n]['_selement'].__class__ for n in path)


KNOWN_PROVIDERS = {
    '_path': calculate_paths,
    '_typepath': calculate_paths,
}


def provide_tags(G: nx.MultiDiGraph, *desired_tags: str, force: bool = False) -> bool:
    result = True

    for tag in desired_tags:
        assert tag in KNOWN_PROVIDERS, f"{PARANOIA_VALUE_ERROR}: No provider for tag '{tag}'"
        provider = KNOWN_PROVIDERS[tag]
        if force or provider not in G.graph[ATTRIBUTE_PROVIDERS]:
            provider(G)
            G.graph[ATTRIBUTE_PROVIDERS].add(provider)
            result = False

    return result
