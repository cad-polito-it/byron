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

__all__ = ["FitnessABC"]

from abc import ABC, abstractmethod
from functools import wraps, cache

# from byron.classes.paranoid import Paranoid
from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.user_messages import *


# class FitnessABC(Paranoid, ABC):
class FitnessABC(ABC):
    """Fitness of a phenotype, handle multiple formats (eg. scalar, tuple).

    The class also redefines the relational operator in order to handle different types of optimization
    (eg. maximization, minimization) and to provide limited support to more complex scenarios
    (eg. multi-objective optimization)

    Equalities ('==' and '!=') are based on `is_distinguishable`.

    Single angular-bracket operators ('>', '<', '>=', and '<=') are based on `is_fitter` and may be randomized
    (ie. the result may not be reproducible).

    Double angular-bracket operators ('>>' and '<<') are based on `is_dominant` and the result is stable. By default,
    `is_dominant` is defined as `is_fitter`.

    When subclassing, one should only redefine `is_fitter`, and optionally `is_distinguishable` and `is_dominant`;
    `is_dominant` **must** be changed if `is_fitter` is randomized, making the result not reproducible.

    Additional sanity checks should be added to `check_comparable
    `. Subclasses may redefine the `decorate` method to
    change the value appearance.
    """

    @abstractmethod
    def is_fitter(self, other: "FitnessABC") -> bool:
        """Check whether fitter than the other (result may be accidental)."""
        assert self.check_comparable(other)
        return super().__gt__(other)

    def is_dominant(self, other: "FitnessABC") -> bool:
        """Check whether dominates the other (result is certain)."""
        return self.is_fitter(other)

    def is_distinguishable(self, other: "FitnessABC") -> bool:
        """Check whether some differences from the other Fitness may be perceived."""
        assert self.check_comparable(other)
        return super().__ne__(other)

    def check_comparable(self, other: "FitnessABC"):
        assert (
            self.__class__ == other.__class__
        ), f"{PARANOIA_TYPE_ERROR}: Different Fitness types: {self.__class__} and {other.__class__}."
        return True

    def _decorate(self) -> str:
        """Represent the individual fitness value with a nice string."""
        return f"{super().__str__()}"

    # FINAL/WARNINGS

    def __eq__(self, other) -> bool:
        return not self.is_distinguishable(other)

    def __ne__(self, other) -> bool:
        return self.is_distinguishable(other)

    def __gt__(self, other) -> bool:
        return self.is_fitter(other)

    def __lt__(self, other) -> bool:
        return other.is_fitter(self)

    def __ge__(self, other) -> bool:
        return not self.__lt__(other)

    def __le__(self, other) -> bool:
        return not self.__gt__(other)

    def __rshift__(self, other) -> bool:
        return self.is_dominant(other)

    def __lshift__(self, other) -> bool:
        return other.is_dominant(self)

    def __str__(self):
        # Double parentheses: ⸨ ⸩  (U+2E28, U+2E29)
        # White parentheses: ⦅ ⦆  (U+2985, U+2986)
        # Fullwidth white parentheses:｟ ｠ (U+FF5F, U+FF60)
        # Math white square parentheses: ⟦ ⟧ (U+27E6, U+27E7)
        # Z notation binding bracket: ⦉ ⦊
        # Curved angled bracket: ⧼ ⧽
        return self._decorate() + "Ƒ"

    def __repr__(self):
        return f"<{self.__class__.__module__}.{self.__class__.__name__} @ {hex(id(self))}>"

    def __hash__(self) -> int:
        return super().__hash__()

    def run_paranoia_checks(self) -> bool:
        return super().run_paranoia_checks()
