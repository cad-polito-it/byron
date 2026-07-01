###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023 Giovanni Squillero and Alberto Tonda
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

import logging

#############################################################################
# While debugging, let's use https://github.com/gruns/icecream

try:
    from icecream import install

    install()
except ModuleNotFoundError:
    pass

from byron import classes as C  # noqa: F401
from byron import classes, ea, framework, operators, sys, user_messages  # noqa: F401
from byron import evaluator_ as evaluator  # noqa: F401
from byron import fitness_ as fit  # noqa: F401
from byron import fitness_ as fitness  # noqa: F401
from byron import framework as f  # noqa: F401
from byron import operators as op  # noqa: F401
from byron.classes.node import NODE_ZERO  # noqa: F401
from byron.fitness_log import *  # noqa: F403
from byron.global_symbols import *  # noqa: F403
from byron.randy import rrandom  # noqa: F401
from byron.registry import *  # noqa: F403
from byron.sys import SYSINFO as sysinfo  # noqa: F401
from byron.tools import checkpoint  # noqa: F401
from byron.tools.graph import fasten_subtree_parameters  # noqa: F401
from byron.tools.providers import *  # noqa: F403
from byron.user_messages.messaging import logger  # noqa: F401

#############################################################################
# Patch names to ease debugging and visualization

# noinspection PyUnresolvedReferences

#############################################################################
# Welcome!


def welcome(level=logging.INFO) -> bool:
    v, d = __version__.rsplit(".", maxsplit=1)
    __welcome__ = (
        f'[bold]This is Byron v{v} "[italic]{__codename__}[/italic]" ({d} @ {__date__})[/]\n'
        + f"[bold]{__copyright__}[/]"
    )

    if notebook_mode:
        from rich.console import Console

        console = Console(highlight=False)
        console.print(__welcome__)
    else:
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
# Welcome
# if main_process and not notebook_mode:
#     welcome(logging.INFO)

#############################################################################
# Warnings

if notebook_mode and logging.getLogger().level <= logging.WARNING and paranoia_mode:
    assert (
        test_mode
        or not main_process
        or user_messages.performance_warning(
            "Paranoia checks are enabled in this notebook: performances can be significantly impaired\n"
            + "[see https://cad-polito-it.github.io/byron/paranoia for details]"
        )
    )
elif not notebook_mode:
    assert (
        test_mode
        or not main_process
        or user_messages.performance_warning(
            "Paranoia checks are enabled: performances can be significantly impaired — consider using '-O'\n"
            + "[see https://cad-polito-it.github.io/byron/paranoia for details]"
        )
    )

if not matplotlib_available:
    user_messages.runtime_warning("No 'matplotlib': plotting of individuals will not be available.")
if not joblib_available:
    user_messages.runtime_warning("No 'joblib': process-based parallel evaluators will not be available.")
if not psutil_available:
    user_messages.runtime_warning("No 'psutil': comprehensive machine information will not be available.")
