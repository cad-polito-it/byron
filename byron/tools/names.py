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

__all__ = ["base_name"]

from collections import Counter

_name_counter = Counter()
_used_names = set()


def base_name(name: str, keep_number: bool = False) -> str:
    if '❰' in name and '❱' in name:
        base = name[name.index('❰') + 1 : name.index('❱')]
    elif '❬' in name and '❭' in name:
        base = name[name.index('❬') + 1 : name.index('❭')]
    elif '<' in name and '>' in name:
        base = name[name.index('<') + 1 : name.index('>')]
    else:
        raise ValueError(name)
    if '#' in base and not keep_number:
        base = base[: base.index('#')]
    return base
