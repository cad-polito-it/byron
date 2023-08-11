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
# v1 / May 2023 / Squillero (GX)

__all__ = ["cook_sequence"]

from collections import abc
from byron.user_messages import *
from byron.classes.selement import SElement
from byron.classes.frame import FrameABC
from byron.classes.parameter import ParameterABC
from byron.classes.macro import Macro
from byron.framework.macro import macro


def cook_sequence(raw_sequence: list[type[SElement] | type[ParameterABC] | str]) -> list[type[SElement]]:
    assert check_valid_type(raw_sequence, abc.Sequence)

    cooked_seq = list()
    for e in raw_sequence:
        if isinstance(e, str):
            cooked_seq.append(macro(e))
        elif isinstance(e, abc.Sequence):
            assert check_valid_length(e, 2, 2 + 1)
            cooked_seq.extend([e[0]] * e[1])
        else:
            cooked_seq.append(e)
    raw_sequence = cooked_seq
    cooked_seq = list()

    for e in raw_sequence:
        assert isinstance(e, str) or check_valid_types(e, FrameABC, Macro, ParameterABC, subclass=True)
        if isinstance(e, str):
            e = macro(e)
        elif issubclass(e, ParameterABC):
            e = macro("{p}", p=e)
        cooked_seq.append(e)

    return cooked_seq
