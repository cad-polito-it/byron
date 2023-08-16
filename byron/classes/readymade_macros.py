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

__all__ = ["MacroZero", "Info"]

import sys
from datetime import datetime
import platform

import networkx as nx

from byron.classes.macro import Macro
from byron.global_symbols import __version__ as version
from byron.tools.names import canonize_name, _patch_class_info
from byron.user_messages import *


class MacroZero(Macro):
    TEXT = (
        "{_comment}"
        + f""" Automagically written by Byron v{version}"""
        + f""" on {datetime.today().strftime('%d-%b-%Y')}"""
        + f""" at {datetime.today().strftime('%H:%M:%S')}"""
    )
    EXTRA_PARAMETERS = dict()
    PARAMETERS = dict()

    @property
    def valid(self) -> bool:
        return True


class Info(Macro):
    TEXT = '''{_comment} * Byron {_byron.byron}
{_comment} * Python {_byron.python}
{_comment} * NetworkX {_byron.nx}
{_comment} * System: {_byron.system}
{_comment} * Machine: {_byron.machine}'''
    PARAMETERS = dict()
    EXTRA_PARAMETERS = dict()

    _parameter_types = dict()

    @property
    def valid(self) -> bool:
        return True


_patch_class_info(
    MacroZero, canonize_name("MacroZero", "Macro", make_unique=False, warn_duplicates=False), tag="framework"
)
_patch_class_info(Info, canonize_name("Info", "Macro", make_unique=False, warn_duplicates=False), tag="framework")
