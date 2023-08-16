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
# v1 / May 2023 / Squillero (GX)

__all__ = ["make_shared_parameter"]

from typing import Any
from byron.classes.parameter import ParameterABC
from byron.tools.names import _patch_class_info

# MAKE KEY (TODO!!!)
_parameters = set()


def make_shared_parameter(parameter: type[ParameterABC]) -> type[ParameterABC]:
    parameter_instance = parameter()

    class T(ParameterABC):
        def __init__(self):
            if parameter_instance.key not in _parameters:
                self._owner = True
                _parameters.add(parameter_instance.key)
            else:
                self._owner = False

        @property
        def value(self):
            return parameter_instance.value

        @value.setter
        def value(self, new_value):
            if self._owner:
                parameter_instance.value = new_value

        def mutate(self, strength: float = 1.0) -> None:
            if self._owner:
                parameter_instance.mutate(strength)

        def is_correct(self, obj: Any) -> bool:
            return parameter_instance.is_correct(obj)

    _patch_class_info(T, f"Shared❬{parameter_instance.__class__.__name__}❭", tag="parameter")
    return T
