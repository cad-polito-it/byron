# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
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

__all__ = ["FrameABC", "FrameAlternative", "FrameSequence", "FrameMacroBunch"]

from typing import Sequence
from abc import abstractmethod

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.classes.selement import SElement
from byron.classes.paranoid import Paranoid


class FrameABC(SElement, Paranoid):
    def __init__(self):
        super().__init__()
        self._checks = list()

    def __str__(self):
        return self.__class__.__name__

    @property
    def valid(self) -> bool:
        # TODO!
        return True

    @property
    @abstractmethod
    def successors(self) -> list[type["SElement"]]:
        pass

    def run_paranoia_checks(self) -> bool:
        return super().run_paranoia_checks()

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    @property
    def shannon(self) -> list[int]:
        return [hash(self.__class__)]


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
