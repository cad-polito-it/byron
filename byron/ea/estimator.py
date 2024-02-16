# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
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
# v1 / January 2024 / Sacchet (MS)

__all__ = ["Estimator"]

from typing import Callable, Sequence
from math import sqrt, log, ceil

from byron.fitness import make_fitness
from byron.randy import rrandom
from byron.classes.fitness import FitnessABC
from byron.ea.common import take_operators


class Estimator:
    _time: int
    _horizon: int
    _operators: dict
    _rewards: list[float]
    _probabilities: list[tuple]
    _near: FitnessABC | None
    _best: FitnessABC | None
    _temperature: float
    _max_t: float
    _exploit: bool

    class I:
        operator: Callable
        UCB: float
        LCB: float

        def __init__(self, operator: Callable, UCB: float, LCB: float):
            self.operator = operator
            self.UCB = UCB
            self.LCB = LCB

    def __init__(
        self,
        time_horizon: int,
        rewards: list[float] = [0.7, 0.3],
        operators: list[Callable] = None,
        fitness: int | float | Sequence = None,
        temperature: float = 0.85,
    ):
        self._operators = dict([[o.__name__, self.I(o, 0, 0)] for o in take_operators(False, operators)])
        assert time_horizon > 0, f"time_horizon need to be positive integer"
        self._horizon = time_horizon
        self._time = 0
        assert len(rewards) == 2, f"must specify two value for reward"
        self._rewards = rewards
        self._probabilities = [(o, 1 / len(self._operators.keys())) for o in self._operators]
        self._exploit = False
        assert temperature > 0, f"temperature must be greater then 0"
        self._temperature = temperature
        self._max_t = temperature
        self._best = None

        if isinstance(fitness, int):
            self._near = make_fitness(ceil(fitness * temperature))
        elif isinstance(fitness, float):
            self._near = make_fitness(fitness * temperature)
        elif isinstance(fitness, Sequence):
            self._near = make_fitness(
                fitness[: ceil(len(fitness) * temperature)]
                + [i * temperature for i in fitness[ceil(len(fitness) * temperature) :]]
            )
        else:
            self._near = None

    def _compute_confidence_interval(self, op, max_l) -> float:
        if self._operators[op].operator.stats.calls == 0:
            self._operators[op].UCB = 0
            self._operators[op].LCB = 0
            return max_l
        # compute confidenze radius r(a)
        conf_radius = sqrt((2 * log(self._horizon) / self._operators[op].operator.stats.calls))
        # compute mean reward mu(a)
        # creation of a better individual w.r.t. parents is highly reward
        # creation of a correct offspring is also rewarded in order to rapidly rule out operators that are not able of creating a valid individual
        mean_rew = (
            self._operators[op].operator.stats.successes * self._rewards[0]
            + self._operators[op].operator.stats.offspring * self._rewards[1]
        ) / self._operators[op].operator.stats.calls
        self._operators[op].UCB = mean_rew + conf_radius
        self._operators[op].LCB = mean_rew - conf_radius
        if self._operators[op].LCB > max_l:
            return self._operators[op].LCB
        else:
            return max_l

    def update(self):
        self._time += 1

        if self._exploit:
            if self._temperature > self._max_t * 0.15:
                self._temperature *= 0.95
            else:
                self._temperature *= 1.05

        # Successive Elimination Algorithm
        max_l = 0
        for op, _ in self._probabilities:
            max_l = self._compute_confidence_interval(op, max_l)
        # check max LCB against every operator so that, if repeated failures happen between the chosen operators,
        # when LCB decrease, we automatically select also previously excluded operators
        valid_operators = [i for i in self._operators if self._operators[i].UCB > max_l]
        self._probabilities = [(o, 1 / len(valid_operators)) for o in valid_operators]

        # every quarter of the run check again also discarded operators
        if self._time % (self._horizon // 4) == 0:
            self._probabilities = [(o, 1 / len(self._operators.keys())) for o in self._operators]

    def take(self) -> Callable:
        return self._operators[
            rrandom.weighted_choice([p[0] for p in self._probabilities], [p[1] for p in self._probabilities])
        ].operator

    def sigma(self, population, actual_fitness, use_entropy) -> float:
        # check fitness but also check entropy to avoid excessive reduction in diversity in the population
        if (
            self._near is not None
            and actual_fitness > self._near
        ):
            if self._best is None:
                self._best = actual_fitness
            if self._best >= actual_fitness:
                self._exploit = False
            elif use_entropy:
                # if every individual in population is different, entropy == log(len(population)) -> with temperature it's possible to tweak how many individuals (in %) need to be different
                if population.entropy >= log(len(population) * (1 - self._temperature)):
                    self._best = actual_fitness
                    self._exploit = True
            else:
                self._best = actual_fitness
                self._exploit = True
                print(self._temperature)
            return self._temperature
        else:
            return 1
