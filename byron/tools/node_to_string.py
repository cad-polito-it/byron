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
# v1 / August 2023 / Squillero (GX)

__all__ = ['node_to_str']

from byron.global_symbols import *
from byron.classes.node_reference import NodeReference
from byron.classes.node_view import NodeView
from byron.classes.value_bag import ValueBag


def node_to_str(nr: NodeReference) -> str:
    extra_parameters = DEFAULT_EXTRA_PARAMETERS | nr.graph.nodes[nr.node]
    extra_parameters |= {'_node': NodeView(nr)}
    dumped = None
    while dumped is None:
        try:
            dumped = nr.graph.nodes[nr.node]['_selement'].dump(ValueBag(extra_parameters))
        except KeyError as k:
            if k.args[0] in extra_parameters:
                return '?'
            extra_parameters[k.args[0]] = "{" + k.args[0] + "}"
        except Exception as e:
            return f'{e}'
    return dumped
