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
# v1 / May 2023 / Squillero (GX)

"""
Methods and constants to create the framework for the individuals.

Notes:
    * As the framework is composed of classes, methods are class factories.
    * Methods are cached, thus multiple calls with equal or equivalent argument return the `same` class. Ie.
      Python operator ``is`` returns ``True``
"""

from .defaults import *
from .bnf import *
from .framework import *
from .macro import *
from .parameter import *
from .parameter_structural_local import *
from .parameter_structural_global import *
from .shared import *
from .show_element import *

from byron.classes.readymade_macros import *
from byron.classes.readymade_frames import *
