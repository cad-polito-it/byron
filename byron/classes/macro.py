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

__all__ = ["Macro"]

from collections import defaultdict
from typing import Any
from copy import copy

from byron.user_messages import *

from byron.classes.selement import SElement
from byron.classes.paranoid import Paranoid
from byron.classes.value_bag import USER_PARAMETER
from byron.classes.value_bag import ValueBag
from byron.classes.node_view import NodeView
from byron.classes.parameter import ParameterABC


class Macro(SElement, Paranoid):
    """Base class for all the different Macros."""

    TEXT: str
    PARAMETERS: dict[str, type[ParameterABC]]
    EXTRA_PARAMETERS: dict[str, Any]

    def __init__(self):
        super().__init__()

    def __eq__(self, other: "Macro") -> bool:
        if type(self) != type(other):
            return False
        elif self.text != other.text or self.parameter_types != other.parameter_types:
            return False
        # elif self.text != other.text or self.parameters != other.parameters:
        #    return False
        return True

    # PEDANTIC
    def is_correct(self, nv: Any) -> bool:
        """Checks a NodeView against a macro."""
        return True
        # assert check_valid_type(nv, NodeView)
        # return all(nv.attributes[n].is_correct(nv.attributes[n].value) for n, p in self.PARAMETERS.items())

    @property
    def text(self) -> str:
        return self.TEXT

    @property
    def parameter_types(self) -> dict[str, type[ParameterABC]]:
        return self.PARAMETERS

    # def __getitem__(self, parameter: str) -> Any:
    #    assert Macro.is_name_valid(parameter), \
    #        f"{PARANOIA_VALUE_ERROR}: invalid parameter name: {parameter}"
    #    return self.parameters[parameter]

    def __str__(self):
        # BRACKETS: ⁅ ⁆ 〈 〉❬ ❭
        # return f'Macro❬{self.__class__.__name__}❭'
        return self.__class__.__name__

    def dump(self, extra_parameters: ValueBag) -> str:
        check_valid_type(extra_parameters, ValueBag)
        return self.text.format(**extra_parameters)

    @staticmethod
    def is_name_valid(name: str) -> bool:
        if not isinstance(name, str):
            return False
        return bool(USER_PARAMETER.fullmatch(name))
