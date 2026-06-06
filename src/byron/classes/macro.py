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
# v1 / April 2023 / Squillero (GX)

__all__ = ["Macro"]

import re
from typing import Any

from byron.classes.parameter import ParameterABC
from byron.classes.paranoid import Paranoid
from byron.classes.selement import SElement
from byron.classes.value_bag import USER_PARAMETER, ValueBag
from byron.user_messages import *


class Macro(SElement, Paranoid):
    """Base class for all the different Macros."""

    TEXT: str
    PARAMETERS: dict[str, type[ParameterABC]]
    EXTRA_PARAMETERS: dict[str, Any]
    SAFE_FORMAT: bool = False  # If True, use safe substitution that ignores unknown {placeholders}

    def __init__(self):
        super().__init__()

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

    @property
    def shannon(self) -> list[int]:
        return [hash(self.__class__)]

    def dump(self, parameters: ValueBag) -> str:
        assert check_valid_type(parameters, ValueBag)
        
        if self.SAFE_FORMAT:
            # Use regex-based substitution to only replace valid parameter placeholders
            # This avoids KeyError when text contains literal braces (e.g., JSON content)
            def replace_param(match):
                key = match.group(1)
                if key in parameters:
                    return str(parameters[key])
                # Not a known parameter, return the original brace expression unchanged
                return match.group(0)
            
            # Match {identifier} patterns where identifier is a valid Python identifier
            pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'
            return re.sub(pattern, replace_param, self.text)
        else:
            # Standard Python str.format() - raises KeyError on unknown placeholders
            return self.text.format(**parameters)

    @staticmethod
    def is_name_valid(name: str) -> bool:
        if not isinstance(name, str):
            return False
        return bool(USER_PARAMETER.fullmatch(name))
