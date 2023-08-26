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
# v1 / May 2023 / Squillero

__all__ = [
    'EvaluatorABC',
    'PythonEvaluator',
    'MakefileEvaluator',
    'ParallelScriptEvaluator',
    'ScriptEvaluator',
]

from typing import Callable, Sequence
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import zip_longest

import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO

if joblib_available:
    import joblib

from byron.user_messages import *
from byron.classes.fitness import FitnessABC
from byron.fitness import make_fitness
from byron.classes.population import Population
from byron.registry import *
from byron.global_symbols import *
from byron.classes.node import NODE_ZERO


@dataclass(kw_only=True, slots=True)
class DebugInfo:
    cmdline: str
    stdout: str
    stderr: str
    returncode: int
    cwd: str


class EvaluatorABC(ABC):
    r"""Base abstract class for Evaluator

    The `Evaluator` classes evaluate individuals in the population without a valid fitness values and update them.

    All *evaluators* implement the function `evaluate_population`, that evaluates all individuals without a valid
    fitness and updates them. The ``EvaluatorABC`` implements the ``__call__`` method, instances can be used as
    functions to execute the `evaluate_population`.

    >>> evaluator = byron.evaluator.PythonEvaluator(fitness)
    >>> evaluator(population)
    >>> print(evaluator.fitness_calls)

    *   **strip_phenotypes**: In all Evaluators, set option `strip_phenotypes` to convert the phenotype into a
        single-line string: the header is removed; leading and trailing spaces in each line are removed; empty lines
        are ignored; the final newline is removed; newlines are converted into spaces. Eg.:

        | ``; Automagically written by Byron⏎``
        | ``000⏎``
        | ``⏎``
        | ``XX      ⏎``
        | ``111⏎``

        is transfomed into the string ``'000 XX 111'``

    *   **max_workers**: If the Evaluator supports some form of paralellism, use option `max_workers` to set the
        maximum number of concurrent *workers* (threads, processes, or others). If set to ``None`` (the default),
        then a *reasonable* number is used, usually chosen considering the CPU cores or other characteristics of the
        system.

    Attributes
    ----------
    fitness_calls
        Number of fitness calls required so far.
    """

    _fitness_calls: int = 0
    _max_workers: int | None = None
    cook: Callable[[str], str]

    def __init__(self, strip_phenotypes: bool = False, max_workers: int | None = None):
        r"""
        Parameters
        ----------
        strip_phenotypes
            ``True`` to transform into single-line strings
        max_workers
            Maximum number of concurrent workers (``None`` for a *reasonable* number)
        """
        if strip_phenotypes:
            self.cook = lambda g: EvaluatorABC.strip_phenotypes(g)
        else:
            self.cook = lambda g: g
        assert max_workers is None or check_value_range(max_workers, 1)
        self._max_workers = max_workers

    @abstractmethod
    def evaluate_population(self, population: Population) -> None:
        r"""Evaluate individuals without a fitness value"""
        raise NotImplementedError

    @property
    def fitness_calls(self) -> int:
        r"""Number of fitness evaluations so far"""
        return self._fitness_calls

    def __call__(self, population: Population) -> None:
        r"""Call `evaluate_population`: evaluate individuals without a fitness value"""
        self.evaluate_population(population)

    @staticmethod
    def strip_phenotypes(raw_dump: str) -> str:
        r"""Transform the phenotype into a one-line string

        Convert the phenotype into a single-line string: the header is removed; leading and trailing spaces in each
        line are removed; empty lines are ignored; the final newline is removed; newlines are converted into spaces.
        Eg.:

        | ``; Automagically written by Byron⏎``
        | ``000⏎``
        | ``⏎``
        | ``XX      ⏎``
        | ``111⏎``

        is transfomed into the string ``'000 XX 111'``
        """
        lines = list()
        for l in raw_dump.split('\n')[1:]:
            if not l.strip():
                continue
            lines.append(l.strip())
        return "\n".join(lines)


class PythonEvaluator(EvaluatorABC):
    r"""An  `Evaluator` based on a Python function.

    The `PythonEvaluator` uses a Python function to calculate the fitness values of individuals. The phenotype is a
    string; it is passed as the only argument to the function. The function has been registered as fitness function
    using the decorator ``@byron.fitness``.

    `PythonEvaluators` allow a simplistic form of parallelism:

    *   thread-based (builtin): Multiple functions are evaluated in different threads. Threads are lightweight,
        but due to the GIL [1]_, this method is likely to be useful only if the fitness function accesses external
        resources (eg. files, REST APIs, databases, external tools).

    *   process-based (based on `joblib` [2]_): Multiple functions are evaluated in different processes.
        Processes-based paralelism does not suffer from the GIL limitation [1]_, but starting/stopping them
        introduces considerable overhead, thus this method is likely to be useful only when the fitness function
        is computationally intensive.

    The `backend` parameters select the type of parallelism: ``None`` for sequential evaluation, ```thread_pool```
    for threads, ``'joblib'`` for processes.

    Use option `strip_phenotypes` (see :py:class:`byron.classes.evaluator.EvaluatorABC`) to convert the phenotype into a
    single-line string.

    Use option `max_workers` (see :py:class:`byron.classes.evaluator.EvaluatorABC`) to set the maximum number of concurrent
    threads or processes.

    Examples
    --------
    Use as many threads as reasonably possible, strip (cleanup) the phenotype before calling the function

    >>> byron.evaluator.PythonEvaluator(fitness, backend='thread_pool', strip_phenotypes=True)

    Notes
    -----
    The fitness function must have been declared with the ``@fitness`` decorator.

    References
    ----------
    .. [1] https://docs.python.org/3/glossary.html#term-global-interpreter-lock
    .. [2] https://joblib.readthedocs.io/en/stable/
    """

    _function: Callable
    _function_name: str

    def __init__(self, fitness_function: Callable[[str], FitnessABC], backend: str | None = None, **kwargs) -> None:
        r"""
        Notes
        -----
        See :py:class:`byron.classes.evaluator.PythonEvaluator` for more information

        Parameters
        ----------
        fitness_function
            The Python function for calculating the fitness
        backend
            Parallelization backend. Possible values are ``None`` or `'thread_pool'` or `'joblib'`
        kwargs
            Extra parameters for :class:`byron.classes.evaluator.EvaluatorABC` (ie. `strip_phenotypes`, `max_workers`)
        """

        super().__init__(**kwargs)
        assert (
            get_byron_type(fitness_function) == FITNESS_FUNCTION
        ), f"TypeError: {fitness_function} has not be registered as a MicgroGP fitness function"

        if not backend or (self._max_workers is not None and self._max_workers < 2):
            backend = ''
            self._max_workers = 1

        self._fitness_function = fitness_function
        self._backend = backend
        self._fitness_function_name = fitness_function.__qualname__

    def __str__(self):
        if not self._backend:
            return f"{self.__class__.__name__}❬{self._fitness_function_name}❭"
        elif self._backend == 'thread_pool':
            return f"{self.__class__.__name__}/ThreadPool❬{self._fitness_function_name}❭"
        elif self._backend == 'joblib':
            return f"{self.__class__.__name__}/JobLib❬{self._fitness_function_name}❭"
        else:
            raise NotImplementedError

    def evaluate_population(self, population: Population) -> None:
        individuals = [
            (i, I, self.cook(population.dump_individual(i))) for i, I in population.not_finalized_individuals
        ]
        if not individuals:
            logger.debug(f"PythonEvaluator: All individuals in the population have already been finalized")
            return

        if self._max_workers == 1 or not self._backend:
            # Simple, sequential, Python evaluator
            for _, I, P in individuals:
                self._fitness_calls += 1
                I.fitness = self._fitness_function(P)
        elif self._backend == 'thread_pool':
            with ThreadPoolExecutor(
                max_workers=self._max_workers, thread_name_prefix=self._fitness_function_name
            ) as pool:
                for I, f in zip(
                    (I for _, I, _ in individuals), pool.map(self._fitness_function, (P for _, _, P in individuals))
                ):
                    self._fitness_calls += 1
                    I.fitness = f
        elif self._backend == 'joblib':
            jobs = list(joblib.delayed(self._fitness_function)(P) for _, _, P in individuals)
            values = joblib.Parallel(n_jobs=self._max_workers if self._max_workers else -1, return_as="generator")(jobs)
            for I, f in zip((I for _, I, _ in individuals), values):
                self._fitness_calls += 1
                I.fitness = f
        else:
            raise NotImplementedError(self._backend)


class MakefileEvaluator(EvaluatorABC):
    r"""A parallel `Evaluator` exploiting the good old `make` [1]_.

    The `MakefileEvaluator` simplify the use of an external `make` command. For each individual to be evaluated: it
    creates a temporary directory; puts in the directory the `Makefile` and all other necessary files; dumps the
    phenotype of the individual; enters the directory (chdir) and calls `make`; gets the result from the standard
    output; and eventually destroys the temporary directory.

    Different individuals are evaluated in parallel by different threads. The GIL [2]_ creates no problem as each
    thread calls a `subprocess.run` and then waits for its completion.

    Most of the parameters can be configured:

    *   `filename`: The name of the phenotype. Usually also the prerequisite of some rule in the Makefile
    *   `required_files`: Additional files required to make the program that must be added to the temporary
        directory. The `makefile` is added by default. Files are added creating a symlink [3]_ (**note**: on Windows it
        may be necessary to give the user additional permission)
    *   `make_command`: How make should be invoked in the current system
    *   `make_flags`: Flags for make. Default is just ``'-s'`` (be quiet)
    *   `makefile`: Name of the Makefile itself
    *   `timeout`: Number of seconds to wait for make completion (default: 60, use ``None`` to wait indefinitely)

    Use option `strip_phenotypes` (see :py:class:`byron.classes.evaluator.EvaluatorABC`) to convert the phenotype into a
    single-line string.

    Use option `max_workers` (see :py:class:`byron.classes.evaluator.EvaluatorABC`) to set the maximum number of concurrent
    threads or processes.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Make_%28software%29
    .. [2] https://docs.python.org/3/glossary.html#term-global-interpreter-lock
    .. [3] https://en.wikipedia.org/wiki/Symbolic_link

    """

    _filename: str
    _make_command: str
    _make_flags: tuple[str]
    _makefile: str
    _required_files: tuple[str]
    _byron_base_dir: str
    _timeout: int | None

    def __init__(
        self,
        filename: str,
        *,
        required_files: Sequence[str] = (),
        make_command='make',
        make_flags: Sequence[str] = ('-s',),
        makefile='Makefile',
        timeout: int | None = 60,
        **kwargs,
    ) -> None:
        r"""
        Parameters
        ----------
        filename
            Name of the file containing the phenotype
        make_command
            Name of the make command.
        make_flags
            Flags for the make command
        makefile
            Name of the makefile
        required_files
            Files that need to be present for the makefile to work in addition to `makefile` and `filename`
        timeout
            Seconds to wait for make completion (``None`` indefinitely)
        kwargs
            Extra parameters for :class:`byron.classes.evaluator.EvaluatorABC` (ie. `strip_phenotypes`, `max_workers`)
        """
        super().__init__(**kwargs)
        self._filename = filename
        self._make_command = make_command
        self._make_flags = tuple(make_flags)
        self._makefile = makefile
        self._required_files = tuple(required_files)
        self._timeout = timeout
        self._byron_base_dir = os.getcwd()

        for f in self._required_files:
            if not os.path.exists(f):
                subprocess.run(
                    [self._make_command, *self._make_flags, f],
                    shell=False,
                    universal_newlines=True,
                    check=True,
                    text=True,
                    timeout=self._timeout,
                    capture_output=True,
                )

    def __str__(self):
        return f"{self.__class__.__name__}❬{self._filename}❭"

    def _evaluate(self, phenotype: str):
        with tempfile.TemporaryDirectory(prefix="byron_", ignore_cleanup_errors=True) as tmp_dir:
            for f in [self._makefile, *self._required_files]:
                assert os.path.exists(
                    f
                ), f"FileNotFoundError (paranoia check): No such file or directory: '{f}' (cwd was '{self._byron_base_dir}')"
                os.symlink(os.path.join(self._byron_base_dir, f), os.path.join(tmp_dir, f))
            with open(os.path.join(tmp_dir, self._filename), "w") as dump:
                dump.write(phenotype)
            result = subprocess.run(
                [self._make_command, *self._make_flags],
                cwd=tmp_dir,
                universal_newlines=True,
                shell=False,
                check=True,
                text=True,
                timeout=self._timeout,
                capture_output=True,
            )

            if result is None or not result.stdout:
                raise ChildProcessError(
                    f"MakefileEvaluator:evaluate: Command '{' '.join([self._make_command, *self._make_flags])}' in {tmp_dir} returned empty stdout"
                    + (f" and stderr '{result.stderr}')" if result.stderr else "")
                )
        return result

    def evaluate_population(self, population: Population) -> None:
        indexes = list()
        phenotypes = list()
        for i, g in population:
            if not g.finalized:
                indexes.append(i)
                phenotypes.append(self.cook(population.dump_individual(i)))
        if not indexes:
            logger.debug(f"MakefileEvaluator: All individuals in the population have already been finalized")
            return

        with ThreadPoolExecutor(max_workers=self._max_workers, thread_name_prefix="byron$") as pool:
            for i, result in zip(indexes, pool.map(self._evaluate, phenotypes)):
                self._fitness_calls += 1
                if result is None:
                    raise RuntimeError(f"Thread failed (returned None)")
                else:
                    value = [float(r) for r in result.stdout.split()]
                    if len(value) == 1:
                        value = value[0]
                    fitness = make_fitness(value)
                    population[i].fitness = fitness


class ScriptEvaluator(EvaluatorABC):
    r"""An `Evaluator` calling a shell script.

    The `ScriptEvaluator` allows using an external script as an external evaluator.
    All individual phenotypes requiring evaluation are dumped in the current directory, then the script
    is called passing the filenames as arguments.

    *   `script_name`: The name of the script. Must be *executable* by a shell, thus it may require the ``+x``
        permission on un*x/macos systems, and it may require the specification of the path (eg. ``./fitness.sh``).
    *   `args`: Arguments required by the script before the filenames of the phenotypes.
    *   `filename_format`: F-string [1]_ with the filenames of the phenotypes. Variable ``i`` is number of the
        individual. Default is "phenotype_{i:x}.txt"
    *   `timeout`: Maximum number of seconds to wait for the script. Use ``None`` to disable timeout.

    Use option `strip_phenotypes` (see :py:class:`byron.classes.evaluator.EvaluatorABC`) to convert the phenotype into a
    single-line string.

    Use option `max_workers` (see :py:class:`byron.classes.evaluator.EvaluatorABC`) to set the maximum number of concurrent
    threads or processes.

    References
    ----------
    .. [1] https://docs.python.org/3/reference/lexical_analysis.html#f-strings

    """

    _file_name: str
    _script_name: str

    def __init__(
        self,
        script_name: str,
        args: Sequence[str] | None = None,
        *,
        filename_format: str = 'phenotype_{i:x}.txt',
        timeout: int | None = 60,
        **kwargs,
    ) -> None:
        r"""
        Parameters
        ----------
        script_name
            Name of the script (eg. ``'./fitness.sh'``)
        args
            Optional arguments before the list of files with phenotypes
        filename_format
            F-string for building phenotype file names
        kwargs
            Extra parameters for :class:`byron.classes.evaluator.EvaluatorABC` (ie. `strip_phenotypes`, `max_workers`)
        """
        super().__init__(**kwargs)
        self._script_name = script_name
        self._script_options = args if args else list()
        self._file_name = filename_format
        self._timeout = timeout

    def __str__(self):
        return f"{self.__class__.__name__}❬{self._script_name}❭"

    def evaluate_population(self, population: Population) -> None:
        individuals = population.not_finalized_individuals
        if not individuals:
            logger.debug(f"ScriptEvaluator: All individuals in the population have already been finalized")
            return
        files = list()
        for idx, ind in individuals:
            self._fitness_calls += 1
            files.append(self._file_name.format(i=population.individuals[idx].id))
            with open(files[-1], "w") as dump:
                dump.write(self.cook(population.dump_individual(idx)))

        result = subprocess.run(
            [self._script_name, *self._script_options, *files],
            universal_newlines=True,
            check=True,
            text=True,
            timeout=self._timeout,
            capture_output=True,
        )

        if result is None:
            raise RuntimeError("Process failed (returned None)")
        elif not result.stdout:
            raise RuntimeError(f"Process returned empty stdout (stderr: '{result.stderr}')")
        else:
            results = list(filter(lambda s: bool(s), result.stdout.split("\n")))
            assert len(results) == len(
                individuals
            ), f"{PARANOIA_VALUE_ERROR}: Number of results and number of individual mismatch: found {len(results)} expected {len(individuals)}"
            for ind, line in zip_longest(individuals, results):
                value = [float(r) for r in line.split()]
                if len(value) == 1:
                    value = value[0]
                fitness = make_fitness(value)
                ind[1].fitness = fitness

        for f in files:
            os.unlink(f)


class ParallelScriptEvaluator(EvaluatorABC):
    r"""A parallel `Evaluator` based on shell script.

    The `MakefileEvaluator` simplify the use of an external `make` command. For each individual to be evaluated: it
    creates a temporary directory; puts in the directory the `Makefile` and all other necessary files; dumps the
    phenotype of the individual; enters the directory (chdir) and calls `make`; gets the result from the standard
    output; and eventually destroys the temporary directory.

    Different individuals are evaluated in parallel by different threads. The GIL [2]_ creates no problem as each
    thread calls a `subprocess.run` and then waits for its completion.

    Most of the parameters can be configured:

    *   `filename`: The name of the phenotype. Usually also the prerequisite of some rule in the Makefile
    *   `required_files`: Additional files required to make the program that must be added to the temporary
        directory. The `makefile` is added by default. Files are added creating a symlink [3]_ (**note**: on Windows it
        may be necessary to give the user additional permission)
    *   `make_command`: How make should be invoked in the current system
    *   `make_flags`: Flags for make. Default is just ``'-s'`` (be quiet)
    *   `makefile`: Name of the Makefile itself
    *   `timeout`: Number of seconds to wait for make completion (default: 60, use ``None`` to wait indefinitely)

    Use option `strip_phenotypes` (see :py:class:`byron.classes.evaluator.EvaluatorABC`) to convert the phenotype into a
    single-line string.

    Use option `max_workers` (see :py:class:`byron.classes.evaluator.EvaluatorABC`) to set the maximum number of concurrent
    threads or processes.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Make_%28software%29
    .. [2] https://docs.python.org/3/glossary.html#term-global-interpreter-lock
    .. [3] https://en.wikipedia.org/wiki/Symbolic_link

    """

    _script: str
    _filename: str
    _flags: tuple[str]
    _other_required_files: tuple[str]
    _byron_base_dir: str
    _timeout: int | None

    def __init__(
        self,
        script: str,
        filename: str,
        *,
        other_required_files: Sequence[str] = (),
        flags: Sequence[str] = tuple(),
        timeout: int | None = 60,
        default_result: str = '',
        **kwargs,
    ) -> None:
        r"""
        Parameters
        ----------
        filename
            Name of the file containing the phenotype
        make_command
            Name of the make command.
        make_flags
            Flags for the make command
        makefile
            Name of the makefile
        other_required_files
            Files that need to be present for the makefile to work in addition to `makefile` and `filename`
        timeout
            Seconds to wait for make completion (``None`` indefinitely)
        default_result
            Default result if the script returns non-zero exit status
        kwargs
            Extra parameters for :class:`byron.classes.evaluator.EvaluatorABC` (ie. `strip_phenotypes`, `max_workers`)
        """
        super().__init__(**kwargs)
        self._script = script
        self._filename = filename
        self._flags = tuple(flags)
        self._other_required_files = tuple(other_required_files)
        self._timeout = timeout
        self._default_result = default_result
        self._byron_base_dir = os.getcwd()

    def __str__(self):
        return f"{self.__class__.__name__}❬{self._filename}❭"

    def _evaluate(self, phenotype: str) -> DebugInfo:
        with tempfile.TemporaryDirectory(prefix="byron_", ignore_cleanup_errors=True) as tmp_dir:
            for f in [*self._other_required_files]:
                assert os.path.exists(
                    f
                ), f"FileNotFoundError (paranoia check): No such file or directory: '{f}' (cwd was '{self._byron_base_dir}')"
                os.symlink(os.path.join(self._byron_base_dir, f), os.path.join(tmp_dir, f))
            with open(os.path.join(tmp_dir, self._filename), "w") as dump:
                dump.write(phenotype)
            result = subprocess.run(
                [self._script, *self._flags, self._filename, *self._other_required_files],
                cwd=tmp_dir,
                universal_newlines=True,
                shell=False,
                check=False,
                text=True,
                timeout=self._timeout,
                capture_output=True,
            )

        return DebugInfo(
            cmdline=' '.join([self._script, *self._flags, self._filename, *self._other_required_files]),
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            cwd=tmp_dir,
        )

    def evaluate_population(self, population: Population) -> None:
        indexes = list()
        phenotypes = list()
        for i, g in population:
            if not g.finalized:
                indexes.append(i)
                phenotypes.append(self.cook(population.dump_individual(i)))
        if not indexes:
            logger.debug(f"ParallelScriptEvaluator: All individuals in the population have already been finalized")
            return

        with ThreadPoolExecutor(max_workers=self._max_workers, thread_name_prefix="byron$") as pool:
            for i, result in zip(indexes, pool.map(self._evaluate, phenotypes)):
                self._fitness_calls += 1
                if result.returncode and self._default_result:
                    logger.info(
                        f"ParallelScriptEvaluator: failed to evaluate {population[i]} (exit status: [red]{result.returncode}[/red])"
                    )
                    logger.debug(
                        f"ParallelScriptEvaluator: command \"{result.cmdline}\" exit status: {result.returncode}"
                        + f"\n[red]---[/red]\n{result.stderr}\n[red]---[/red]"
                    )
                    result.stdout = self._default_result + '\n'
                elif not self._default_result:
                    logger.error(f"ParallelScriptEvaluator: failed to evaluate {population[i]}")
                    logger.error(
                        f"command \"{result.cmdline}\" exit status: {result.returncode}"
                        + f"\n[red]---[/red]\n{result.stderr}\n[red]---[/red]"
                    )
                    raise ValueError(
                        "ParallelScriptEvaluator: {population[i]}: ParallelScriptEvaluator: script returned non-zero exit status"
                    )
                value = [float(r) for r in result.stdout.split()]
                if len(value) == 1:
                    value = value[0]
                fitness = make_fitness(value)
                population[i].fitness = fitness
