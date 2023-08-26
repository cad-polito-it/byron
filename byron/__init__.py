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

import logging

# noinspection PyUnresolvedReferences
from byron import sys

# noinspection PyUnresolvedReferences
from byron.functions import *

# noinspection PyUnresolvedReferences
from byron.global_symbols import *
from byron.classes.node import NODE_ZERO

# noinspection PyUnresolvedReferences
from byron.classes.node import NODE_ZERO

# noinspection PyUnresolvedReferences
from byron import user_messages

# noinspection PyUnresolvedReferences
from byron import user_messages

##from _byron.user_messages.exception import *
### noinspection PyUnresolvedReferences

# noinspection PyUnresolvedReferences
from byron import classes

# noinspection PyUnresolvedReferences
from byron import classes as C

# noinspection PyUnresolvedReferences
from byron import framework

# noinspection PyUnresolvedReferences
from byron import framework as f

# noinspection PyUnresolvedReferences
from byron import ea

# noinspection PyUnresolvedReferences
from byron import operators

# noinspection PyUnresolvedReferences
from byron import operators as op

# noinspection PyUnresolvedReferences
from byron import evaluator_ as evaluator

# noinspection PyUnresolvedReferences
from byron import fitness_ as fitness

# noinspection PyUnresolvedReferences
from byron import fitness_ as fit

# noinspection PyUnresolvedReferences
from byron.randy import rrandom

# noinspection PyUnresolvedReferences
from byron.user_messages.messaging import logger

# noinspection PyUnresolvedReferences
from byron.registry import *

# noinspection PyUnresolvedReferences
from byron.fitness_log import *

# noinspection PyUnresolvedReferences
from byron.sys import SYSINFO as sysinfo

# noinspection PyUnresolvedReferences
from byron.tools.graph import fasten_subtree_parameters

# noinspection PyUnresolvedReferences
from byron.tools.entropy import *


#############################################################################
# Patch names to ease debugging and visualization

# noinspection PyUnresolvedReferences

#############################################################################
# Welcome!

# __welcome__ = (
#     f'This is Byron v{__version__} "{__codename__}"\n' + f"(c) 2023 G. Squillero & A. Tonda — Licensed under Apache-2.0"
# )

__welcome__ = (
    f'[bold]This is Byron v{__version__.rsplit(".", maxsplit=1)[0]} "[italic]{__codename__}[/italic]"[/]\n'
    + f"[bold](c) 2023 G. Squillero & A. Tonda — Licensed under Apache-2.0[/]"
)


def welcome(level=logging.DEBUG):
    from sys import stderr, stdout

    stderr.flush()
    stdout.flush()
    lines = __welcome__.split("\n")
    for m in lines:
        # stars: ⚝ ⭐// feathers: 🖋
        # user_messages.logger.log(level, f"🖋: {m}")
        user_messages.logger.log(level, f"{m}")
    stderr.flush()
    stdout.flush()
    return True


#############################################################################
# Warning

if notebook_mode and logging.getLogger().level <= logging.WARNING and paranoia_mode:
    assert (
        test_mode
        or not main_process
        or user_messages.performance_warning(
            "Paranoia checks are enabled in this notebook: performances can be significantly impaired\n"
            + "[see https://github.com/cad-polito-it/byron/blob/alpha/docs/paranoia.md for details]"
        )
    )
elif not notebook_mode:
    assert (
        test_mode
        or not main_process
        or user_messages.performance_warning(
            "Paranoia checks are enabled: performances can be significantly impaired — consider using '-O'\n"
            + "[see https://github.com/cad-polito-it/byron/blob/alpha/docs/paranoia.md for details]"
        )
    )

#############################################################################
# Welcome

if main_process and not notebook_mode:
    welcome(logging.INFO)

#############################################################################
# Warnings

if not matplotlib_available:
    user_messages.runtime_warning("No 'matplotlib': plotting of individuals will not be available.")
if not joblib_available:
    user_messages.runtime_warning("No 'joblib': process-based parallel evaluators will not be available.")
if not psutil_available:
    user_messages.runtime_warning("No 'psutil': comprehensive machine information will not be available.")
