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
# v1 / April 2023 / Squillero (GX)

__all__ = [
    'ATTRIBUTE_PROVIDERS',
    'ATTRIBUTE_SELEMENT',
    'BYRON_TAG',
    'DEFAULT_EXTRA_PARAMETERS',
    'DEFAULT_OPTIONS',
    'FITNESS_FUNCTION',
    'FRAME',
    'FRAMEWORK',
    'FRAME_IS_ALTERNATIVE',
    'FRAME_IS_BNF',
    'FRAME_IS_MACRO_BUNCH',
    'FRAME_IS_SEQUENCE',
    'GENETIC_OPERATOR',
    'LINK',
    'LOGGING_DEBUG',
    'LOGGING_ERROR',
    'LOGGING_INFO',
    'LOGGING_WARNING',
    'LOG_LAPSES',
    'MACRO',
    'PARANOIA_SYSTEM_ERROR',
    'PARANOIA_TYPE_ERROR',
    'PARANOIA_VALUE_ERROR',
    'SE_DIRECTORY',
    '__author__',
    '__codename__',
    '__copyright__',
    '__date__',
    '__version__',
    'debug_mode',
    'joblib_available',
    'main_process',
    'matplotlib_available',
    'notebook_mode',
    'paranoia_mode',
    'psutil_available',
    'test_mode',
]

import logging
import multiprocessing
import sys
from collections import defaultdict

__version__ = "0.8a1.dev67"
__date__ = "01-07-2026"
__codename__ = "Don Juan"
__author__ = "Giovanni Squillero and Alberto Tonda"
__copyright__ = "Copyright (c) 2023-24 Giovanni Squillero and Alberto Tonda"

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
ATTRIBUTE_PROVIDERS = '_providers'
ATTRIBUTE_SELEMENT = '_selement'
BYRON_TAG = 'To have joy, one must share it'
FITNESS_FUNCTION = 'fitness_function'
FRAMEWORK = 'framework'
FRAME_IS_ALTERNATIVE = 'alternative'
FRAME_IS_BNF = 'bunch'
FRAME_IS_MACRO_BUNCH = 'bunch'
FRAME_IS_SEQUENCE = 'sequence'
GENETIC_OPERATOR = 'genetic_operator'
LINK = 'link'
FRAME = 'frame'
MACRO = 'macro'
PARANOIA_SYSTEM_ERROR = 'SystemError (paranoia check)'
PARANOIA_TYPE_ERROR = 'TypeError (paranoia check)'
PARANOIA_VALUE_ERROR = 'ValueError (paranoia check)'

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

assert "SE_DIRECTORY" not in globals(), f"{PARANOIA_SYSTEM_ERROR}: SElement Directory already initialized"
SE_DIRECTORY = set()
assert "SE_DIRECTORY" in globals(), f"{PARANOIA_SYSTEM_ERROR}: SElement Directory not initialized"
