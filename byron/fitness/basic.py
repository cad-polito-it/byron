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
# v1 / May 2023 / Squillero (GX)

__all__ = ["Scalar", "Integer", "Float", "Vector", "Lexicographic", "make_fitness"]

from typing import Sequence, Any

from math import isclose

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.classes.fitness import FitnessABC
from byron.user_messages import *


class Float(FitnessABC, float):
    """A single numeric value -- Larger is better."""

    def __new__(cls, *args, **kw):
        syntax_warning_hint(
            "'Float' fitness values suffer from Floating Point Arithmetic issues and limitations (eg. .1+.1+.1 != .3) — consider using 'Scalar'"
        )
        return float.__new__(cls, *args, **kw)

    def _decorate(self):
        return "ℝ" + str(float(self))


class Integer(FitnessABC, int):
    """A single numeric value -- Larger is better."""

    def __new__(cls, *args, **kw):
        return int.__new__(cls, *args, **kw)

    def _decorate(self):
        return str(int(self))


class Scalar(FitnessABC, float):
    """A single, floating-point value with approximate equality -- Larger is better."""

    def __new__(cls, *args, **kw):
        return float.__new__(cls, *args, **kw)

    def __init__(self, argument, rel_tol: float = 1e-09, abs_tol: float = 0):
        """See the documentation of math.isclose() and PEP485."""
        # super(Scalar, self).__init__()
        self._rel_tol = rel_tol
        self._abs_tol = abs_tol

    def _decorate(self) -> str:
        return format(self, "g")

    def is_distinguishable(self, other: FitnessABC) -> bool:
        assert self.check_comparable(other)
        return not isclose(float(self), float(other), rel_tol=self._rel_tol, abs_tol=self._abs_tol)

    def is_fitter(self, other: FitnessABC) -> bool:
        assert self.check_comparable(other)
        return self != other and float(self) > float(other)

    def check_comparable(self, other: "Scalar"):
        assert super().check_comparable(other)
        assert (
            not isinstance(other, self.__class__) or self._abs_tol == other._abs_tol
        ), f"{PARANOIA_VALUE_ERROR}: Different absolute tolerance: {float(self)}±{self._abs_tol} vs. {float(other)}±{other._abs_tol}"
        assert (
            not isinstance(other, self.__class__) or self._rel_tol == other._rel_tol
        ), f"{PARANOIA_VALUE_ERROR}: Different relative tolerance: {float(self)}±{self._rel_tol}r vs. {float(other)}±{other._rel_tol}r"
        return True


# VECTORS


class Vector(FitnessABC):
    """A vector of fitness values"""

    def __init__(self, values: Sequence[FitnessABC]) -> None:
        self._values = tuple(values)

    def cheeck_comparable(self, other: "Vector"):
        assert len(self._values) == len(
            other._values
        ), f"Can't is_fitter Fitness Vectors of different size ({self} vs. {other})"
        assert all(v1.check_comparable(v2) for v1, v2 in zip(self, other))
        return True

    def is_distinguishable(self, other: "Vector") -> bool:
        assert self.check_comparable(other)
        return any(v1.is_distinguishable(v2) for v1, v2 in zip(self, other))

    def is_fitter(self, other: "Vector") -> bool:
        self.check_comparable(other)
        return list(self) > list(other)

    # def is_dominant(self, other: 'Vector') -> bool:
    #    self.check_comparable(other)
    #    return all(v1 >> v2 for v1, v2 in zip(self, other))

    def _decorate(self) -> str:
        return "(" + ", ".join(e._decorate() for e in self) + ")"

    def __iter__(self):
        return iter(self._values)

    def __hash__(self):
        return hash(self._values)


class Lexicographic(Vector):
    """A generic vector of Fitness values.

    fitness_type is the subtype, **kwargs are passed to fitness init

    Examples:
        f1 = sgx.fitness.Vector([23, 10], fitness_type=Scalar, abs_tol=.1)
        f2 = sgx.fitness.Vector([23, 10], fitness_type=Scalar, abs_tol=.001)

        f1 > sgx.fitness.Vector([23, 9.99], fitness_type=Scalar, abs_tol=.1) is False
        f2 > sgx.fitness.Vector([23, 9.99], fitness_type=Scalar, abs_tol=.001) is True

    """

    def __init__(self, values: Sequence, type_: type[FitnessABC] = Scalar):
        assert check_valid_types(values, Sequence)
        assert values, f"ValueError: Can't convert empty sequence {values} to Lexicographic Fitness"
        fitness_values = [type_(v) for v in values]
        super().__init__(fitness_values)


def make_fitness(data: Any):
    if isinstance(data, int):
        return Integer(data)
    elif isinstance(data, float):
        return Scalar(data)
    elif isinstance(data, Sequence):
        logger.warning(f"{data}")
        return Lexicographic(data)
    else:
        assert (
            isinstance(data, Sequence) or isinstance(data, int) or isinstance(data, float)
        ), f"TypeError: Can't convert {data!r} ({type()}) to Fitness"
