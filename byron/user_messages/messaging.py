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

__all__ = [
    'logger',
    'performance_warning',
    'runtime_warning',
    'user_warning',
    'syntax_warning',
    'deprecation_warning',
    'syntax_warning_hint',
]

import logging
import sys
import time
import warnings

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO

BASE_STACKLEVEL = 3


class ByronPerformanceWarning(RuntimeWarning):
    pass


class ByronFriendlyWarning(SyntaxWarning):
    pass


def _indent_msg(message):
    return "\n  " + message.replace("\n", "\n  ")


def performance_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", ByronPerformanceWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def runtime_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", RuntimeWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def user_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", UserWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def syntax_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", SyntaxWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def deprecation_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", DeprecationWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def syntax_warning_hint(message: str, stacklevel_offset: int = 0) -> bool:
    if logger.level <= logging.INFO and not test_mode:
        warnings.warn(
            f"{_indent_msg(message)}",
            ByronFriendlyWarning,
            stacklevel=BASE_STACKLEVEL + stacklevel_offset,
        )
        DEBUG_FRIENDLY_SUGGESTIONS = (
            "\n  Friendly suggestions are only shown if code is not optimized and logging level is DEBUG"
        )
        if not notebook_mode:
            warnings.warn(DEBUG_FRIENDLY_SUGGESTIONS, ByronFriendlyWarning)
    return True


#############################################################################
# CUSTOMIZATIONS

assert "logger" not in globals(), f"SystemError (paranoia check): byron logger already initialized"
logging.basicConfig()  # Initialize logging
logger = logging.getLogger('byron')
logger.propagate = False

assert 'logger' in globals(), f"SystemError (paranoia check): byron logger not initialized"

if test_mode:
    logger.setLevel(logging.WARNING)
elif notebook_mode:
    logger.setLevel(logging.DEBUG)
elif __debug__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Alternative symbols: ⍄ ┊

from rich import logging as rich_logging
from rich import highlighter as rich_highlighter


# console_handler = logging.StreamHandler()
# console_handler.setFormatter(console_formatter)
if notebook_mode:
    console_handler = logging.StreamHandler()
    # console_formatter = logging.Formatter('%(asctime)s ▷ %(levelname)s ▷ %(name)s::%(message)s', datefmt='%H:%M:%S')
    console_formatter = logging.Formatter('%(levelname)s ▷ %(message)s')
else:
    console_handler = rich_logging.RichHandler(
        log_time_format='%H:%M:%S',  # '%H:%M:%S.%f'
        omit_repeated_times=False,
        show_path=False,
        markup=True,
        highlighter=rich_highlighter.NullHighlighter(),
        keywords=['▷'],
    )
    console_formatter = logging.Formatter('▷ %(message)s')
console_handler.setFormatter(console_formatter)
logger.handlers = [console_handler]
# logger.handlers = []

# file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s::%(message)s', datefmt="%Y-%m-%d %H:%M:%S,uuu")
# file_handler = logging.FileHandler('debug.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# Avoid excessive warnings...
if not sys.warnoptions:
    warnings.filterwarnings('once', category=ByronPerformanceWarning, module='byron')
    warnings.filterwarnings('once', category=ByronFriendlyWarning, module='byron')
    # warnings.filterwarnings('once', category=SyntaxWarning, module='byron')


def hesitant_log(lapse: float, level: int, *args, **kwargs):
    now = time.time()
    if now - LOG_LAPSES[level] >= lapse:
        logger.log(level, *args, **kwargs)
        LOG_LAPSES[level] = now


assert (
    getattr(logger, '__dict__') and 'hesitant_log' not in logger.__dict__
), f"PANIC: {logger} has already the attribute 'hesitant_log'"
logger.hesitant_log = hesitant_log
assert (
    getattr(logger, '__dict__') and 'hesitant_log' in logger.__dict__
), f"PANIC: cannot register attribute 'hesitant_log' in {logger}"
