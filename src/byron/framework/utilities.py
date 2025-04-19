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
# v1 / May 2023 / Squillero (GX)

__all__ = ["cook_selement_list"]

from collections import abc
from typing import Sequence

from byron.classes.frame import FrameABC
from byron.classes.macro import Macro
from byron.classes.parameter import ParameterABC
from byron.classes.selement import SElement
from byron.framework.macro import macro
from byron.user_messages import *


def cook_selement_list(raw_se_list: Sequence[type[SElement] | type[ParameterABC] | str]) -> list[type[SElement]]:
    assert check_valid_type(raw_se_list, abc.Sequence)

    cooked_se_list = list()
    for e in raw_se_list:
        assert isinstance(e, str) or check_valid_types(e, FrameABC, Macro, ParameterABC, subclass=True)
        if isinstance(e, str):
            e = macro(e, _invalid_target=True)
        elif issubclass(e, ParameterABC):
            e = macro("{p}", p=e)
        cooked_se_list.append(e)

    return cooked_se_list
