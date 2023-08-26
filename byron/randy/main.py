# -*- coding: utf-8 -*-
# ______________   ______   __
# |____/|____|| \  ||   \\_/
# |R  \_|A   ||N \_||D__/ |Y
#
#    @..@    古池や
#   (----)    蛙飛び込む
#  ( >__< )    水の音
#
# https://github.com/squillero/randy
# Copyright 2023 Giovanni Squillero.
# SPDX-License-Identifier: 0BSD

import math
from functools import lru_cache
from typing import Any
from collections.abc import Sequence, Iterable

import numpy as np
from scipy.stats import truncnorm

from byron.user_messages import *
from byron.global_symbols import *
from byron.classes.node import NODE_ZERO

__all__ = ["Randy"]


class Randy:
    """Safe, reproducible random numbers for EA applications."""

    SMALL_NUMBER = 1e-15
    LOG_FILENAME = 'randy.log'

    __slots__ = ['_generator', '_calls', '_saved_state']

    def __getstate__(self):
        return self._generator.__getstate__(), self._calls

    def __setstate__(self, state):
        self._generator.__setstate__(state[0])
        _calls = state[1]
        assert self._save_state()

    def __init__(self, seed: Any = None) -> None:
        self._generator = np.random.default_rng(seed)
        self._calls = 0
        # with open(Randy.LOG_FILENAME, 'a') as fout:
        #    fout.write(f"Created new Randy: {self}\n")
        self._save_state()

    def __str__(self) -> str:
        description = ", ".join(f"{a}={b!r}" for a, b in self._generator.__getstate__().items())
        return f"Randy @ {hex(id(self))} (calls={self._calls}, {description})"

    def __bool__(self):
        return self.boolean()

    @property
    def state(self):
        return self._generator.bit_generator.state

    @state.setter
    def state(self, state):
        self._generator.bit_generator.state = state
        assert self._save_state()

    def _get_current_state(self) -> dict:
        return self._generator.bit_generator.state

    def _save_state(self) -> bool:
        self._saved_state = self._get_current_state()
        return True

    def _save_state_log(self) -> bool:
        self._saved_state = self._get_current_state()
        with open(Randy.LOG_FILENAME, 'a') as fout:
            fout.write(f"{self!r}: {self._saved_state}\n")
        return True

    def _get_saved_state(self) -> dict:
        return self._saved_state

    def _check_saved_state(self) -> bool:
        assert (
            self._get_current_state() == self._get_saved_state()
        ), "State Error (paranoia check): internal generator has been modified"
        return True

    def seed(self, seed: Any = None) -> None:
        assert (
            seed is not None
            or notebook_mode
            or messaging.syntax_warning_hint(
                "Random seed is None: results will not be reproducible (generally a bad idea when debugging)"
            )
        )
        self._generator = np.random.default_rng(seed)
        # with open(Randy.LOG_FILENAME, 'a') as fout:
        #    fout.write(f"New seed: {self}\n")
        assert self._save_state()

    @staticmethod
    def _check_parameters(a, b, *, loc: float | None = None, scale: float | None = None, sigma: float | None = None):
        assert a <= b, "ValueError (paranoia check): 'a' must precede 'b': found ({a}, {b})"
        assert not (
            scale is not None and sigma is not None
        ), "ValueError (paranoia check): 'scale' and 'sigma' cannot be both specified"
        assert (
            sigma is None or 0 <= sigma <= 1
        ), f"ValueError (paranoia check): strength (σ) should be in [0, 1]. Found {sigma}"
        assert loc is None or a <= loc <= b, "ValueError (paranoia check): 'loc' not in [{a}, {b}]"
        assert scale is None or scale >= 0, "ValueError (paranoia check): scale must be positive. Found {scale}"

        assert (loc is None and sigma is None and scale is None) or (
            loc is not None and (sigma is not None or scale is not None)
        ), "ValueError (paranoia check): 'loc' and 'scale'/'strength' not specified together"
        return True

    @staticmethod
    def get_truncnorm_parameters(
        a: float, b: float, *, loc: float, scale: float | None = None, sigma: float | None = None
    ) -> dict:
        r"""Returns the 'a', 'b', 'loc', and 'scale' to be passed to 'truncnorm'"""
        if sigma is not None:
            x = sigma / 2 + 0.5
            x = min(x, 1 - Randy.SMALL_NUMBER)
            scale = math.log(x / (1 - x))
            if math.isclose(scale, 0):
                scale = Randy.SMALL_NUMBER
        return {'a': (a - loc) / scale, 'b': (b - loc) / scale, 'loc': loc, 'scale': scale}

    def random_float(
        self,
        a: float | None = 0,
        b: float | None = 1,
        *,
        loc: float | None = None,
        scale: float | None = None,
        sigma: float | None = None,
    ) -> float:
        """A value from a standard normal truncated to [a, b) with mean = 'loc' and standard deviation = 'scale'."""
        self._calls += 1
        assert self._check_saved_state()
        assert Randy._check_parameters(a, b, loc=loc, scale=scale, sigma=sigma)
        if loc is None:
            val = self._generator.random() * (b - a) + a
        else:
            val = truncnorm.ppf(
                self._generator.random(), **Randy.get_truncnorm_parameters(a, b, loc=loc, scale=scale, sigma=sigma)
            )
        assert self._save_state()
        return val

    def random_int(self, a, b, **kwargs) -> int:
        """A value from a standard normal truncated to [a, b) with mean = 'loc' and standard deviation = 'scale'."""
        val = self.random_float(a - 0.5, b - 0.5, **kwargs)
        return round(val)

    def choice(self, seq: Sequence[Any], loc: int | None = None, sigma: float | None = None) -> Any:
        """Returns a random element from seq by perturbing index loc with a given strength."""
        index = self.random_int(0, len(seq), loc=loc, sigma=sigma)
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

    def shuffle(self, seq: Sequence) -> None:
        """Shuffle list x in place, and return None."""
        assert self._check_saved_state()
        self._generator.shuffle(seq)
        assert self._save_state()
