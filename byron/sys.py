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
# v1 / June 2023 / Squillero (GX)

"""Information about the current system.
Mostly useful in interactive environments such as a Jupyter Notebook.
"""

__all__ = ['get_operators', 'log_operators', 'SYSINFO']

import inspect
from pprint import pformat
from byron.operators import *


class View:
    def __init__(self, data: dict):
        try:
            self._data = dict(sorted(data.items()))
        except TypeError:
            self._data = dict(sorted(data.items(), key=lambda k: str(k)))

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, item):
        if item not in self._data:
            raise KeyError(item)
        return self._data[item]

    def __repr__(self):
        return "⟦" + pformat(self._data)[1:-1] + "⟧"

    def __str__(self):
        return "⟦" + ", ".join(k for k in self._data.keys()) + "⟧"

    def items(self):
        return tuple(self._data.items())

    def keys(self):
        return tuple(self._data.keys())

    def values(self):
        return tuple(self._data.values())


class SysInfo:
    def __init__(self):
        pass

    @property
    def genetic_operators(self):
        """Shows all genetic operators available in the current namespace"""
        ops = dict()
        snapshot = inspect.currentframe().f_globals
        for k, v in snapshot.items():
            if hasattr(v, '_byron_') and v.type == GENETIC_OPERATOR:
                ops[k] = v
        return View(ops)

    @property
    def fitness_functions(self):
        """Shows all fitness functions available in the current namespace"""
        ops = dict()
        snapshot = inspect.currentframe().f_globals
        for k, v in snapshot.items():
            if hasattr(v, '_byron_') and v.type == FITNESS_FUNCTION:
                ops[k] = v
        return View(ops)

    def show(self, object):
        """Gives some information about a byron object. The name (string) can be used"""

        if isinstance(object, str):
            if object not in inspect.currentframe().f_globals:
                raise KeyError(object)
            object = inspect.currentframe().f_globals[object]

        if hasattr(object, '_byron_') and object.type == GENETIC_OPERATOR:
            print(f"Genetic operator: {object}")
            print(f"  {object.stats}")
        else:
            print(f"Python object: {type(object)}")


def get_operators():
    snapshot = inspect.currentframe().f_globals
    return [o for o in snapshot.values() if hasattr(o, '_byron_') and o.type == GENETIC_OPERATOR]


def log_operators():
    all_ops = sorted(get_operators(), key=lambda o: (o.num_parents if o.num_parents is not None else -1, o.__name__))

    descr = {None: 'init', 1: 'mut', 2: 'xover'}

    logger.info(f"[b]GENETIC OPERATORS[/b]")
    for op in all_ops:
        name = f'{op.__name__} ({descr[op.num_parents]})'
        logger.info(f"[blue]*[/blue] {name:.<50s}: {op.stats}")


assert "SYSINFO" not in globals(), f"SystemError (paranoia check): SYSINFO already initialized."
SYSINFO = SysInfo()
assert "SYSINFO" in globals(), f"SystemError (paranoia check): SYSINFO not initialized."
