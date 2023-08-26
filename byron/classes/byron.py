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
# v1 / August 2023 / Squillero (GX)

import sys
import platform

import networkx as nx

try:
    import psutil
except ModuleNotFoundError:
    psutil = None

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO


class Byron:
    r"""A lazy, read-only view on internal info"""

    def __str__(self) -> str:
        return f'This is Byron v{__version__} "{__codename__}"'

    def __getattr__(self, item):
        try:
            if item == 'byron' or item == 'version':
                return f'{__version__} "{__codename__}"'
            elif item == 'nx' or item == 'networkx':
                return f'{nx.__version__}'
            elif item == 'python':
                return f'{sys.version}'
            elif item == 'system' or item == 'os':
                return f'{platform.version()}'
            elif item == 'machine':
                desc = f'{platform.machine()} ({platform.processor()})'
                if psutil:
                    desc += f'; {psutil.cpu_count(logical=False)} physical cores ({psutil.cpu_count(logical=True)} logical); {psutil.virtual_memory().total // 2 ** 20:,} MiB RAM'
                return desc
            else:
                raise SyntaxError
        except:
            return f'{{_byron.{item}}}'
