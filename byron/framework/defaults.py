# -*- coding: utf-8 -*-
#############################################################################
#           __________                                                      #
#    __  __/ ____/ __ \__ __   This file is part of MicroGP v4!2.0          #
#   / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer  #
#  / /_/ / /_/ / ____/ // /_   https://github.com/microgp/microgp4          #
#  \__  /\____/_/   /__  __/                                                #
#    /_/ --MicroGP4-- /_/      You don't need a big goal, be μ-ambitious!   #
#                                                                           #
#############################################################################

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

__all__ = ['set_global_parameter', 'set_global_option']

from typing import Any
import re

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.global_symbols import DEFAULT_EXTRA_PARAMETERS, DEFAULT_OPTIONS


def set_global_parameter(key: str, value: Any) -> None:
    r"""Set the global default for a framework parameter

    Parameters name always start with underscore. The are f-strings and may contain variables (eg.
    ``"This is {_node}"``). Parameter may be modified locally in `SElements` (`Macros` and `Frames`) using
    ``extra_parameters={'_foo': 'bar'}``.

    *   `_comment`: What is recognized as the beginning of a *line comment* (default ``';'``)
    *   `_label`: Dumped before the node if the node is the target of some structural parameters
        (default ``'{_node}:\n'`),
    *   `_text_before_node`: Dumped before all nodes (default ``''``)
    *   `_text_after_node`: Dumped after all nodes (default ``''``)
    *   `_text_before_macro`: Dumped before a node that encodes a macro (default ``''``)
    *   `_text_after_macro`: Dumped after a node that encodes a macro (default ``'\n'``)
    *   `_text_before_frame`: Dumped before a node that encodes a frame (default ``''``)
    *   `_text_after_frame`: Dumped after a node that encodes a frame (default ``''``)

    See `byron.DEFAULT_EXTRA_PARAMETERS` for the complete list of default parameters.
    """
    assert re.fullmatch(r'_[a-z_0-9]+', key), f"{PARANOIA_VALUE_ERROR}: Invalid key name {key}"
    DEFAULT_EXTRA_PARAMETERS[key] = value


def set_global_option(key: str, value: Any) -> None:
    r"""Set the global default for a framework option

    Options name always start with dollar ``$``. They are boolean. The default for options is ``False``.

    *   `$dump_node_info`: Dump after each node a valid *line comment* with some information (useful for debug)

    See `byron.DEFAULT_OPTIONS` for the complete list of default parameters.
    """

    assert re.fullmatch(r'\$[a-z_0-9]+', key), f"{PARANOIA_VALUE_ERROR}: Invalid option name {key}"
    DEFAULT_OPTIONS[key] = value
