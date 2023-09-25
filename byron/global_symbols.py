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
    '__version__',
    '__date__',
    '__author__',
    '__copyright__',
    '__codename__',
    'LOGGING_DEBUG',
    'LOGGING_INFO',
    'LOGGING_WARNING',
    'LOGGING_ERROR',
    'FRAMEWORK',
    'LINK',
    'FRAME_NODE',
    'MACRO_NODE',
    'BYRON_TAG',
    'GENETIC_OPERATOR',
    'FITNESS_FUNCTION',
    'test_mode',
    'notebook_mode',
    'debug_mode',
    'main_process',
    'joblib_available',
    'matplotlib_available',
    'psutil_available',
    'paranoia_mode',
    'PARANOIA_TYPE_ERROR',
    'PARANOIA_VALUE_ERROR',
    'PARANOIA_SYSTEM_ERROR',
    'DEFAULT_EXTRA_PARAMETERS',
    'DEFAULT_OPTIONS',
    'LOG_LAPSES',
]

import logging
import sys
from collections import defaultdict
import multiprocessing

__version__ = "0.8a1.dev30"
__date__ = "25-09-2023"
__codename__ = "Don Juan"
__author__ = "Giovanni Squillero and Alberto Tonda"
__copyright__ = "Copyright (c) 2023 Giovanni Squillero and Alberto Tonda"

#####################################################################################################################
# Auto-detected "modes"

test_mode = 'pytest' in sys.modules
main_process = multiprocessing.current_process().name == "MainProcess"

notebook_mode = False
if any('jupyter' in k for k in sys.modules.keys()):
    notebook_mode = True
elif any('google.colab' in k for k in sys.modules.keys()):
    notebook_mode = True
else:
    try:
        if 'zmqshell' in str(type(get_ipython())):
            notebook_mode = True
    except NameError:
        pass

joblib_available = False
try:
    import joblib

    joblib_available = True
except ModuleNotFoundError:
    pass

matplotlib_available = False
try:
    import matplotlib

    matplotlib_available = True
except ModuleNotFoundError:
    pass

psutil_available = False
try:
    import psutil

    psutil_available = True
except ModuleNotFoundError:
    pass

debug_mode = __debug__


#############################################################################
# PARANOID MODE


def _check_assert():
    global paranoia_mode
    paranoia_mode = True


paranoia_mode = False
assert _check_assert() or True

#####################################################################################################################
# "Global" constants

LOGGING_DEBUG = logging.DEBUG
LOGGING_INFO = logging.INFO
LOGGING_WARNING = logging.WARNING
LOGGING_ERROR = logging.ERROR

# NODE_ZERO = Node(0) defined in class.node
FRAMEWORK = 'framework'
LINK = 'link'
FRAME_NODE = 'frame'
MACRO_NODE = 'macro'
SEQUENCE_FRAME = 'sequence'
ALTERNATIVE_FRAME = 'alternative'
MACRO_BUNCH_FRAME = 'bunch'
BNF_FRAME = 'bunch'
BYRON_TAG = 'To have joy, one must share it'
GENETIC_OPERATOR = 'genetic_operator'
FITNESS_FUNCTION = 'fitness_function'
PARANOIA_TYPE_ERROR = 'TypeError (paranoia check)'
PARANOIA_VALUE_ERROR = 'ValueError (paranoia check)'
PARANOIA_SYSTEM_ERROR = 'SystemError (paranoia check)'


DEFAULT_OPTIONS = {
    '$dump_node_info': False,
}
DEFAULT_EXTRA_PARAMETERS = {
    '_comment': ';',
    '_label': '{_node}:\n',
    '_text_before_macro': '',
    '_text_after_macro': '\n',
    '_text_before_frame': '',
    '_text_after_frame': '',
    '_text_before_node': '',
    '_text_after_node': '',
}

LOG_LAPSES = defaultdict(float)

#####################################################################################################################
