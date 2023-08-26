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

# NOTE[GX]: This file contains code that some programmer may find upsetting

__all__ = ["Statistics", "fitness_function", "genetic_operator", "get_byron_type"]

from typing import Callable
from dataclasses import dataclass

from functools import wraps
import weakref

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.user_messages import *
from byron.classes.individual import Individual, Lineage
from byron.classes.frame import FrameABC
from byron.classes.fitness import *
from byron import fitness
from byron.fitness_log import *
from byron.classes import monitor

FAMILYTREE_FILENAME = 'genealogy.db'
FITNESS_LOG_FILENAME = 'fitness.db'


def _genetic_operator_mutation_proto(parent: Individual, strength=1.0) -> list[Individual] | None:
    """Example of signature for a mutation genetic operator"""
    raise NotImplementedError


def _genetic_operator_xover_proto(p1: Individual, p2: Individual) -> list[Individual] | None:
    """Example of signature for a crossover genetic operator"""
    raise NotImplementedError


def _genetic_operator_initializer_proto(top_frame: FrameABC) -> list[Individual] | None:
    """Example of signature for an initializer genetic operator"""
    raise NotImplementedError


def get_byron_type(object):
    if not hasattr(object, '_byron_') or object._byron_ != BYRON_TAG or not hasattr(object, "type"):
        return None
    return object.type


@dataclass
class Statistics:
    """Class for keeping stats of a genetic operator."""

    calls: int = 0
    aborts: int = 0
    offspring: int = 0
    failures: int = 0
    successes: int = 0

    @staticmethod
    def nice(number, tag):
        if number == 0:
            return f"no {tag}s"
        elif number == 1:
            return f"1 {tag}"
        else:
            return f"{number:,} {tag}s"

    def __str__(self):
        return (
            Statistics.nice(self.calls, "call")
            + "; "
            + Statistics.nice(self.aborts, "abort")
            + "; "
            + Statistics.nice(self.offspring, "new individual")
            + (f" (👍{self.successes:,} 👎{self.failures:,})" if self.successes or self.failures else "")
        )


def fitness_function(
    func: Callable[..., FitnessABC] | None = None, /, *, type_: type[FitnessABC] = None, backend: str | None = 'list'
):
    if type_ is None:
        type_ = lambda f: fitness.make_fitness(f)
    log_ = FitnessLog(backend)

    @wraps(func)
    def wrapper(*args, log=log_, **kwargs):
        result = type_(func(*args, **kwargs))
        log += result
        return result

    wrapper._byron_ = BYRON_TAG
    wrapper.type = FITNESS_FUNCTION

    if func is None:
        # called with args... let's roll again
        return lambda f: fitness_function(f, type_=type_, backend=backend)
    else:
        return wrapper


def genetic_operator(*, num_parents: int = 1):
    r"""Register a function as a "genetic operator"

    A genetic operator creates individual. A genetic operators is given `num_parents` individual and produces a list
    of new individuals (the offspring). If the operator return an empty list or `None`, or if it raises a
    `GeneticOperatorFailure` exception, it is considered to have aborted.

    Genetic operators gets any number of parents as arguments and the `strength` as mandatory keyword argument. That is:

    >>> def custom_operator(*, strength=1.0) -> list[Individual] | None:

    Historically, genetic operators are classified either as *mutation operators*, when `num_parents == 1`,
    or *recombination operators*, when `num_parents >= 2`. byron handles a third class: the *initializers*,
    when `num_parent == None`. Initializers are called before the first generation, when the population is empty,
    and gets as argument only the `top_frame` of individuals (that is: no *parent* is needed, as there are none
    available, yet). Also, the `strength` is missing. That is:

    >>> def initializer(top_frame) -> list[Individual] | None:

    If an operator does not require a parent, but it is supposed to be called after initialization, set `num_parents
    = 0`. It will be called with an empty individual as argument (ie. only NODE_ZERO)
    """

    assert num_parents is None or check_value_range(num_parents, 1)

    def decorator(func):
        @monitor.failure_rate
        @wraps(func)
        def wrapper(*args: Individual | FrameABC, **kwargs):
            assert all(
                i.__class__ == args[0].__class__ for i in args
            ), f"{PARANOIA_VALUE_ERROR}: Can't mate different objects: {args}"
            assert all(
                not isinstance(i, Individual) or i.top_frame == args[0].top_frame for i in args
            ), f"{PARANOIA_VALUE_ERROR}: Can't mate individuals with different top_frame: {args}"

            wrapper.stats.calls += 1

            try:
                offspring = func(*args, **kwargs)
            except ByronOperatorFailure:
                offspring = list()
            else:
                if offspring is None:
                    offspring = []

            assert all(
                isinstance(i, Individual) for i in offspring
            ), f"TypeError: offspring {offspring!r}: expected list['Individual']"
            offspring = [i for i in offspring if i.valid]
            for i in offspring:
                i._lineage = Lineage(wrapper, tuple(weakref.proxy(a) for a in args))
                i.discard_useless_components()
            if offspring:
                wrapper.stats.offspring += len(offspring)
            else:
                wrapper.stats.aborts += 1
            return offspring

        wrapper._byron_ = BYRON_TAG
        wrapper.type = GENETIC_OPERATOR
        wrapper.num_parents = num_parents
        wrapper.stats = Statistics()

        return wrapper

    return decorator
