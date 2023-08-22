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

__all__ = ['integer_parameter', 'float_parameter', 'choice_parameter', 'array_parameter', 'counter_parameter']

from collections.abc import Collection
from functools import cache
from numbers import Number
from typing import Any, Hashable, SupportsInt

from byron.user_messages import *
from byron.classes.parameter import *
from byron.randy import rrandom


@cache
def _numeric(*, type_, min_, max_):
    class T(ParameterNumericABC):
        f"""An {type_} parameter in half-open range [{min_}, {max_})."""

        __slots__ = []  # Preventing the automatic creation of __dict__

        MIN = min_
        MAX = max_

        def __init__(self):
            super().__init__()

        def run_paranoia_checks(self) -> bool:
            assert self.is_correct(self.value), f"TypeError: not a {type_} in range {min_}-{max_}"
            return super().run_paranoia_checks()

        def is_correct(self, obj: Any) -> bool:
            return isinstance(obj, type_) and min_ <= obj < max_

        if type_ == int:

            def mutate(self, strength: float = 1.0) -> None:
                if strength == 1.0:
                    self.value = rrandom.random_int(min_, max_)
                else:
                    self.value = rrandom.random_int(min_, max_, loc=self._value, strength=strength)

        elif type_ == float:

            def mutate(self, strength: float = 1.0) -> None:
                if strength == 1.0:
                    self.value = rrandom.random_float(min_, max_)
                else:
                    self.value = rrandom.random_float(min_, max_, loc=self._value, strength=strength)

    if type_ == int and min_ == 0 and any(max_ == 2**n for n in range(4, 128 + 1)):
        p = next(n for n in range(4, 128 + 1) if max_ == 2**n)
        T._patch_info(name=f'{type_.__name__.title()}[{p}bit]')
    elif type_ == int:
        T._patch_info(name=f'{type_.__name__.title()}[{min_}..{max_ - 1}]')
    else:
        T._patch_info(name=f'{type_.__name__.title()}[{min_}–{max_})')
    return T


def integer_parameter(min_: int, max_: int) -> type[ParameterABC]:
    r"""An Int parameter: an integer number in the half-open range [min_, max_)."""

    def check_range():
        if max_ - min_ == 1:
            syntax_warning_hint(
                f"Parameter ranges are half-open: the value can only be {min_:,} — did you mean '({min_}, {max_+1})'?",
                stacklevel_offset=1,
            )
        elif any(max_ - min_ + 1 == 10**n for n in range(1, 10)):
            syntax_warning_hint(
                f"Parameter ranges are half-open: the maximum value is {max_-1} (ie. a range of {max_-min_:,} possible values) — did you mean '({min_}, {max_+1})'?",
                stacklevel_offset=1,
            )
        elif any(max_ - min_ == 2**n - 1 for n in range(6, 128 + 1)):
            p = next(n for n in range(128 + 1) if max_ - min_ == 2**n - 1)
            syntax_warning_hint(
                f"Parameter ranges are half-open: the maximum value is {max_ - 1:,} (ie. a range of 2**{p}-1 possible values)",
                stacklevel_offset=1,
            )
        elif any(max_ - min_ == 2**n + 1 for n in range(6, 128 + 1)):
            p = next(n for n in range(128 + 1) if max_ - min_ == 2**n + 1)
            syntax_warning_hint(
                f"Parameter ranges are half-open: the maximum value is {max_:,} (ie. a range of 2**{p}+1 possible values)",
                stacklevel_offset=1,
            )
        return True

    assert check_valid_type(min_, int)
    assert check_valid_type(max_, int)
    assert check_range()

    return _numeric(type_=int, min_=int(min_), max_=int(max_))


def float_parameter(min_: float, max_: float) -> type[ParameterABC]:
    r"""A Float parameter: a floating point number in the half-open range [min_, max_)."""
    assert check_valid_type(min_, Number)
    assert check_valid_type(max_, Number)
    return _numeric(type_=float, min_=float(min_), max_=float(max_))


@cache
def _choice_parameter(alternatives: tuple[Hashable]) -> type[ParameterABC]:
    class T(ParameterABC):
        __slots__ = []  # Preventing the automatic creation of __dict__

        ALTERNATIVES: tuple[Hashable] = alternatives
        NUM_ALTERNATIVES: int = len(alternatives)

        def __init__(self):
            super().__init__()

        def is_correct(self, obj: Any) -> bool:
            return obj in alternatives

        def run_paranoia_checks(self) -> bool:
            assert self.is_correct(self.value), f"ValueError: {self.value} not in alternative list: {alternatives}"
            return super().run_paranoia_checks()

        def mutate(self, strength: float = 1.0) -> None:
            if strength == 1.0:
                self.value = rrandom.choice(alternatives)
            else:
                self.value = rrandom.choice(alternatives, loc=alternatives.index(self._value), sigma=strength)

    # NOTE[GX]: alternative symbol: – (not a minus!)
    T._patch_info(name='Choice[' + '┊'.join(str(a) for a in alternatives) + ']')
    return T


def choice_parameter(alternatives: Collection[Hashable]) -> type[ParameterABC]:
    r"""A Choice parameter: an element from a fixed list of alternatives."""

    def check_size():
        if len(alternatives) > 999:
            syntax_warning_hint(
                f"Choice parameters with many alternatives impair performances — why not using an integer parameter [0-{len(alternatives):})?",
                stacklevel_offset=1,
            )
        return True

    assert check_valid_type(alternatives, Collection)
    assert check_valid_length(alternatives, 1)
    assert all(check_valid_type(e, Hashable) for e in alternatives)
    assert check_no_duplicates(alternatives)
    assert all(check_valid_type(e, type(alternatives[0])) for e in alternatives)
    assert check_size()

    try:
        alternatives_sorted = sorted(alternatives)
    except TypeError:
        # Yeuch, can't sort it directly
        alternatives_sorted = sorted(alternatives, key=lambda e: str(e))

    return _choice_parameter(tuple(alternatives_sorted))


@cache
def _array_parameter(symbols: tuple[str], length: int) -> type[ParameterABC]:
    class T(ParameterArrayABC):
        __slots__ = []  # Preventing the automatic creation of __dict__

        DIGITS = tuple(symbols)
        LENGTH = length

        def __init__(self):
            super().__init__()

        def is_correct(self, obj: Any) -> bool:
            if len(obj) != length:
                return False
            return all(e in set(symbols) for e in obj)

        def run_paranoia_checks(self) -> bool:
            # TODO: improve message
            assert self.is_correct(self.value), f"ValueError: {self.value} not a valid array"
            return super().run_paranoia_checks()

        def mutate(self, strength: float = 1.0) -> None:
            if strength == 1:
                new_value = [rrandom.choice(symbols) for _ in range(length)]
            else:
                new_value = [rrandom.choice(symbols) if rrandom.boolean(strength) else old for old in self._value]
            self.value = "".join(new_value)

    T._patch_info(name="Array[" + "".join(str(a) for a in symbols) + f"ｘ{length}]")
    return T


def array_parameter(symbols: Collection[str], length: SupportsInt) -> type[ParameterABC]:
    r"""An Array parameter: a fixed-length array of symbols."""

    assert check_valid_type(symbols, Collection)
    assert check_valid_length(symbols, 1)
    assert all(check_valid_type(d, str) for d in symbols)
    assert check_no_duplicates(symbols)
    assert all(check_valid_length(d, 1, 2) for d in symbols)
    assert check_valid_type(length, SupportsInt)
    assert check_value_range(int(length), 1)

    return _array_parameter(tuple(sorted(symbols)), int(length))


@cache
def counter_parameter() -> type[ParameterABC]:
    r"""A simple counter, increments at each mutation"""

    class T(ParameterABC):
        __slots__ = []  # Preventing the automatic creation of __dict__
        COUNTER = 0

        def __init__(self):
            super().__init__()

        def is_correct(self, obj: Any) -> bool:
            return True

        def mutate(self, strength: float = 1.0) -> None:
            T.COUNTER += 1
            self.value = T.COUNTER

    T._patch_info(name='Counter[]')
    return T
