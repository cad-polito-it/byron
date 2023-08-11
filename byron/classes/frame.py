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
# v1 / April 2023 / Squillero (GX)

__all__ = ["FrameABC", "FrameAlternative", "FrameSequence", "FrameMacroBunch"]

from types import NoneType
from abc import abstractmethod
from copy import copy

from byron.user_messages.checks import *

from byron.classes.macro import Macro
from byron.global_symbols import *
from byron.classes.selement import SElement
from byron.classes.paranoid import Paranoid
from byron.classes.value_bag import ValueBag


class FrameABC(SElement, Paranoid):
    _registered_names = set()

    def __init__(self, extra_parameters: dict | None = None) -> None:
        assert check_valid_types(extra_parameters, dict, NoneType)
        super().__init__()
        self._checks = list()
        self._extra_parameters = extra_parameters if extra_parameters is not None else dict()
        # self._values = list()

    @property
    def valid(self) -> bool:
        # TODO!
        return True

    @property
    def extra_parameters(self):
        return copy(self._extra_parameters)

    @property
    @abstractmethod
    def successors(self) -> list[type["SElement"]]:
        pass

    def dump(self, extra_parameters: ValueBag) -> str:
        check_valid_type(extra_parameters, ValueBag)
        return ""

    def run_paranoia_checks(self) -> bool:
        return super().run_paranoia_checks()

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    @staticmethod
    def register_name(name: str) -> bool:
        assert name not in FrameABC._registered_names, f"{PARANOIA_VALUE_ERROR}: Frame name {name!r} already exists"
        FrameABC._registered_names.add(name)
        return True


class FrameSequence:
    r"""Empty class to mark frames of type "Sequence"

    See Also
    --------
    `sequence` factory function
    """
    pass


class FrameAlternative:
    r"""Empty class to mark frames of type "Alternative"

    See Also
    --------
    `altrnative` factory function
    """
    pass


class FrameMacroBunch:
    r"""Empty class to mark frames of type "MacroBunch"

    See Also
    --------
    `bunch` factory function
    """
    pass
