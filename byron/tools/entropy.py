# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
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

__all__ = ['calculate_entropy', 'calculate_delta_entropy']

from typing import Sequence
import math
from collections import Counter
from functools import reduce


def calculate_entropy(messages: Sequence[Sequence[int]]) -> float:
    cnt = Counter()
    for m in messages:
        cnt.update({k: 1 for k in m})
    tot = cnt.total()
    return -sum(c / tot * math.log(c / tot) for c in cnt.values())


def calculate_delta_entropy(messages: Sequence[Sequence[int]]) -> float:
    messages = [Counter(m) for m in messages]
    big_message = Counter()
    for m in messages:
        big_message.update({k: 1 for k in m})
    total_symbols = big_message.total()

    total_entropy = -sum(c / total_symbols * math.log(c / total_symbols) for c in big_message.values())
    for m in messages:
        big_message -= m
        entropy = -sum(c / total_symbols * math.log(c / total_symbols) for c in big_message.values())
        print(total_entropy, '->', entropy, 'D=', total_entropy - entropy)
        big_message += m
    pass
