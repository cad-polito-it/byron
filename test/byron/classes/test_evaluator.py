# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest
from byron.classes.evaluator import EvaluatorABC, PythonEvaluator
from byron.classes.fitness import FitnessABC
from byron.fitness import Scalar


# Mock classes for testing purposes
class MockIndividual:
    def __init__(self, fitness=None):
        self.fitness = fitness


class MockPopulation:
    def __init__(self, individuals):
        self.individuals = individuals

    def __iter__(self):
        return iter(self.individuals)


class MockEvaluator(EvaluatorABC):
    def evaluate_population(self, population: MockPopulation) -> None:
        for individual in population:
            if individual.fitness is None:
                individual.fitness = 1  # a dummy fitness value
        self._fitness_calls += len(population.individuals)


# Tests for EvaluatorABC


def test_evaluator_with_strip_phenotypes_true():
    evaluator = MockEvaluator(strip_phenotypes=True)
    raw_dump = "; Header\n000\n\nXX\n111\n"
    expected_cooked = "000\nXX\n111"  # Corrected expected string
    assert evaluator.cook(raw_dump) == expected_cooked


def test_evaluator_with_strip_phenotypes_false():
    evaluator = MockEvaluator(strip_phenotypes=False)
    raw_dump = "; Header\n000\n\nXX\n111\n"
    assert evaluator.cook(raw_dump) == raw_dump


def test_call_method():  # check the __call__
    evaluator = MockEvaluator()
    mock_population = MockPopulation([MockIndividual(fitness=None) for _ in range(5)])
    evaluator(mock_population)
    assert all(individual.fitness is not None for individual in mock_population)


def test_fitness_calls_increment():  # check fittness calls
    evaluator = MockEvaluator()
    mock_population = MockPopulation([MockIndividual(fitness=None) for _ in range(5)])
    initial_calls = evaluator.fitness_calls
    evaluator(mock_population)
    assert evaluator.fitness_calls == initial_calls + len(mock_population.individuals)


def test_strip_phenotypes():
    raw_dump = "; Header\n000\n\nXX\n111\n"
    expected_result = "000\nXX\n111"
    assert MockEvaluator.strip_phenotypes(raw_dump) == expected_result


def test_not_implemented_evaluate_population():
    with pytest.raises(TypeError):
        evaluator = EvaluatorABC()


@pytest.fixture
def mock_population():
    return MockPopulation([MockIndividual(fitness=None) for _ in range(5)])


# Use the fixture in tests
def test_call_method_with_fixture(mock_population):
    evaluator = MockEvaluator()
    evaluator(mock_population)
    assert all(individual.fitness is not None for individual in mock_population)


def test_fitness_calls_increment_with_fixture(mock_population):
    evaluator = MockEvaluator()
    initial_calls = evaluator.fitness_calls
    evaluator(mock_population)
    assert evaluator.fitness_calls == initial_calls + len(mock_population.individuals)


# todo ask about the fitness implementation
# # Second part:) Mock fitness function not doing well
# def mock_fitness_function(phenotype: str) -> FitnessABC:
#     # Assuming a simple fitness measure based on the length of the phenotype string
#     fitness_value = len(phenotype)
#     return Scalar(fitness_value)


# class MockIndividual:
#     def __init__(self, phenotype, fitness=None):
#         self.phenotype = phenotype
#         self.fitness = fitness


# class MockPopulation:
#     def __init__(self, individuals):
#         self.individuals = individuals

#     def not_finalized_individuals(self):
#         return [(idx, ind) for idx, ind in enumerate(self.individuals) if ind.fitness is None]

#     def dump_individual(self, idx):
#         return self.individuals[idx].phenotype
#     def __iter__(self):
#         return iter(self.individuals)

# def test_python_evaluator_initialization():
#     evaluator = PythonEvaluator(mock_fitness_function, backend='thread_pool', strip_phenotypes=True)
#     assert evaluator._fitness_function == mock_fitness_function
#     assert evaluator._backend == 'thread_pool'

# def test_sequential_evaluation():
#     population = MockPopulation([MockIndividual("abc"), MockIndividual("abcd")])
#     evaluator = PythonEvaluator(mock_fitness_function, backend=None)
#     evaluator(population)
#     assert all(individual.fitness == len(individual.phenotype) for individual in population.individuals)

# def test_thread_pool_evaluation():
#     population = MockPopulation([MockIndividual("abc"), MockIndividual("abcd")])
#     evaluator = PythonEvaluator(mock_fitness_function, backend='thread_pool', max_workers=2)
#     evaluator(population)
#     assert all(individual.fitness == len(individual.phenotype) for individual in population.individuals)

# def test_joblib_evaluation():
#     population = MockPopulation([MockIndividual("abc"), MockIndividual("abcd")])
#     evaluator = PythonEvaluator(mock_fitness_function, backend='joblib', max_workers=2)
#     evaluator(population)
#     assert all(individual.fitness == len(individual.phenotype) for individual in population.individuals)

# def test_fitness_calls_increment():
#     population = MockPopulation([MockIndividual("abc"), MockIndividual("abcd")])
#     evaluator = PythonEvaluator(mock_fitness_function, backend=None)
#     initial_calls = evaluator.fitness_calls
#     evaluator(population)
#     assert evaluator.fitness_calls == initial_calls + len(population.not_finalized_individuals())

# def test_invalid_backend():
#     with pytest.raises(NotImplementedError):
#         PythonEvaluator(mock_fitness_function, backend='invalid_backend')


if __name__ == "__main__":
    pytest.main()
