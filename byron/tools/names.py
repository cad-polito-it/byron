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
# v1 / April 2023 / Squillero (GX)

__all__ = ["canonize_name", "uncanonize_name", "FRAMEWORK_DIRECTORY"]

from collections import Counter
import re

from byron.global_symbols import *

_name_counter = Counter()
_used_names = set()


def canonize_name(
    name: str,
    tag: str,
    user: bool | None = None,
    make_unique: bool = True,
    user_space: bool = False,
    warn_duplicates: bool = True,
) -> str:
    assert re.fullmatch(
        r'[a-z_][a-z_0-9]*', name, re.IGNORECASE
    ), f"{PARANOIA_VALUE_ERROR}: Illegal character in name: {name}."

    if user is True:
        user_space = True
    elif make_unique:
        _name_counter[(tag, name)] += 1
        name += f"#{_name_counter[(tag, name)]}"

    if user_space:
        canonic_name = f"{tag}<{name}>"
    else:
        # NOTE[GX]: These "fancy" brackets are difficult to enter ;-)
        canonic_name = f"{tag}❬{name}❭"

    if user_space:
        assert (
            not warn_duplicates or name not in _used_names
        ), f"{PARANOIA_VALUE_ERROR}: User name '{name}' has already been used."
        _used_names.add(name)
    else:
        assert (
            not warn_duplicates or canonic_name not in _used_names
        ), f"{PARANOIA_VALUE_ERROR}: Name '{canonic_name}' has already been used."
        _used_names.add(canonic_name)

    return canonic_name


def uncanonize_name(name: str, keep_number: bool = False, user: bool | None = None) -> str:
    if user is None:
        user = "❬" not in name and "❭" not in name
    if user and "<" in name:
        tag = name[0 : name.index("<")]
    elif not user and "❬" in name:
        tag = name[0 : name.index("❬")]
    else:
        return name

    tlen = len(tag)
    assert (name[tlen] == "❬" and name[-1] == "❭") or (
        name[tlen] == "<" and name[-1] == ">"
    ), f"{PARANOIA_VALUE_ERROR}: not a canonic name: '{name}'."
    stripped = name[tlen + 1 : -1]
    if "#" in stripped and not keep_number:
        stripped, num = stripped.split("#")
    return stripped


def _patch_class_info(obj: type, name: str | None, tag: str | None = None) -> None:
    if name:
        obj.__name__ = name
    obj.__qualname__ = obj.__name__
    obj.__module__ = "byron"

    if tag is not None:
        obj.__module__ += f".{tag}"


class SElementsDirectory:
    _data: dict

    def __init__(self):
        self._data = dict()

    def __len__(self):
        return len(self._data)

    def __setitem__(self, key, value):
        assert key not in self._data, f"{PARANOIA_VALUE_ERROR}: duplicate name '{key}'."
        self._data[key] = value

    def __getitem__(self, key):
        assert key in self._data, f"{PARANOIA_VALUE_ERROR}: unknown frame '{self._target_frame}'."
        return self._data[key]


assert "FRAMEWORK_DIRECTORY" not in globals(), f"SystemError (paranoia check): FRAMEWORK_DIRECTORY already initialized."
FRAMEWORK_DIRECTORY: SElementsDirectory = SElementsDirectory()
assert "FRAMEWORK_DIRECTORY" in globals(), f"SystemError (paranoia check): FRAMEWORK_DIRECTORY not initialized."
