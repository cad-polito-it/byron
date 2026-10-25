# ______________   ______   __
# |____/|____|| \  ||   \\_/
# |R  \_|A   ||N \_||D__/ |Y
#
#    @..@    古池や
#   (----)    蛙飛び込む
#  ( >__< )    水の音
#
# https://github.com/squillero/randy
# Copyright 2023-24 Giovanni Squillero.
# SPDX-License-Identifier: 0BSD

import math
import random
from collections.abc import Sequence
from typing import Any, MutableSequence

from byron.global_symbols import *
from byron.user_messages import *

__all__ = ["Randy"]


class Randy:
    """Safe, reproducible random numbers for EA applications."""

    SMALL_NUMBER = 1e-15
    LOG_FILENAME = 'randy.log'

    __slots__ = ['_generator', '_calls', '_saved_state']

    def __getstate__(self):
        return self.state

    def __setstate__(self, state):
        self.state = state

    def __init__(self, seed: Any = 42) -> None:
        self._generator = random.Random(seed)
        self._calls = 0
        # with open(Randy.LOG_FILENAME, 'a') as fout:
        #    fout.write(f"Created new Randy: {self}\n")
        assert self.__save_state()

    def __str__(self) -> str:
        return f"Randy @ {hex(id(self))} (state={self.state})"

    def __bool__(self):
        return self.boolean()

    @property
    def state(self):
        return self._generator.getstate(), self._calls

    @state.setter
    def state(self, state):
        self._generator.setstate(state[0])
        self._calls = state[1]
        assert self.__save_state()

    def __save_state(self) -> bool:
        self._saved_state = self.state
        return True

    def __check_saved_state(self) -> bool:
        return self._saved_state == self.state

    def seed(self, seed: Any = None) -> None:
        assert (
            seed is not None
            or notebook_mode
            or messaging.syntax_warning_hint(
                "Random seed is None: results will not be reproducible (generally a bad idea when debugging)"
            )
        )
        self._generator = random.Random(seed)
        # with open(Randy.LOG_FILENAME, 'a') as fout:
        #    fout.write(f"New seed: {self}\n")
        assert self.__save_state()

    @staticmethod
    def _check_parameters(a, b, *, loc: float | None = None, strength: float | None = None):
        assert a <= b, f"ValueError (paranoia check): 'a' must precede 'b': found ({a}, {b})"
        assert strength is None or 0 <= strength <= 1, (
            f"ValueError (paranoia check): strength (σ) should be in [0, 1]. Found {strength}"
        )
        assert loc is None or a <= loc <= b, f"ValueError (paranoia check): 'loc' ({loc}) not in [{a}, {b}]"
        if strength is None:
            strength = 1.0
        assert strength == 1.0 or loc is not None, "ValueError (paranoia check): 'loc' not specified"
        return True

    @staticmethod
    def _strength_to_scale(strength: float) -> float:
        if strength > 0.999:
            return 50
        else:
            return math.sqrt(1 / (1 - strength) - 1)

    def random_float(
        self,
        a: float | None = 0,
        b: float | None = 1,
        *,
        loc: float | None = None,
        strength: float = 1.0,
    ) -> float:
        """A value from between [a, b) by permutating 'loc' with a give 'strength'."""
        assert self.__check_saved_state(), (
            "SystemError (paranoia check): Randy the Random internal state has been modified"
        )
        assert Randy._check_parameters(a, b, loc=loc, strength=strength)
        self._calls += 1
        if loc is None or strength == 1.0:
            val = self._generator.random() * (b - a) + a
        else:
            scale = Randy._strength_to_scale(strength) * (b - a)
            offset = self._generator.gauss(0, scale)
            val = loc + offset
            if not a <= val < b:
                val = self._generator.random() * (b - a) + a
        assert self.__save_state()
        return val

    def random_int(
        self,
        a: int,
        b: int,
        *,
        loc: int | None = None,
        strength: float = 1.0,
    ) -> int:
        """A value from between [a, b) by permutating 'loc' with a give 'strength'."""
        assert self.__check_saved_state(), (
            "SystemError (paranoia check): Randy the Random internal state has been modified"
        )
        assert Randy._check_parameters(a, b, loc=loc, strength=strength)
        self._calls += 1
        if loc is None or strength == 1.0:
            val = self._generator.randint(a, b - 1)
        else:
            scale = Randy._strength_to_scale(strength) * (b - a) / 2
            offset = round(self._generator.gauss(0, scale))
            # ic(offset)
            val = loc + offset
            if not a <= val < b:
                val = self._generator.randint(a, b - 1)
        assert self.__save_state()
        return val

    def choice(self, seq: Sequence[Any], loc: int | None = None, strength: float | None = None) -> Any:
        """Returns a random element from seq by perturbing index loc with a given strength."""
        assert loc is None or strength == 1 or 0 <= loc < len(seq), (
            f"ValueError (paranoia check): loc ({loc}) out of range"
        )
        index = self.random_int(0, len(seq), loc=loc, strength=strength)
        return seq[index]

    def boolean(self, p_true: float | None = None, p_false: float | None = None) -> bool:
        """Returns a boolean value with the given probability."""
        assert (
            (p_true is None or 0 <= p_true <= 1)
            and (p_false is None or 0 <= p_false <= 1)
            and (p_true is None or p_false is None or math.isclose(p_true + p_false, 1))
        ), f"ValueError (paranoia check): incorrect p_true/p_false: found {p_true}, {p_false}"

        if p_true is None and p_false is None:
            p_true = 0.5
        elif p_true is None and p_false is not None:
            p_true = 1 - p_false
        return self.random_float(0, 1) < p_true

    def shuffle(self, seq: MutableSequence) -> None:
        """Shuffle list x in place, and return None."""
        assert self.__check_saved_state(), (
            "SystemError (paranoia check): Randy the Random internal state has been modified"
        )
        self._generator.shuffle(seq)
        assert self.__save_state()

    def weighted_choice(self, seq: Sequence[Any], p: Sequence[float]) -> Any:
        """Returns a random element from seq using the probabilities in p."""
        assert len(seq) == len(p), "ValueError: different number of elements in seq and weight"
        assert math.isclose(sum(p), 1), "ValueError: weights sum not 1"
        r = self.random_float()
        return next(val for val, cp in ((v, sum(p[0 : i + 1])) for i, v in enumerate(seq)) if cp >= r)
