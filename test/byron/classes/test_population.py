# -*- coding: utf-8 -*-
#################################|###|##################################
#  _____                         |   |                                 #
# |  __ \--.--.----.-----.-----. |===| This file is part of Byron      #
# |  __ <  |  |   _|  _  |     | |___| Evolutionary optimizer & fuzzer #
# |____/ ___  |__| |_____|__|__|  ).(  v0.8a1 "Don Juan"               #
#       |_____|                   \|/                                  #
################################## ' ###################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest
from byron.classes.population import Population
from byron.classes.individual import Individual
from byron.classes.selement import SElement
from byron.classes.fitness import FitnessABC


class MockFitness(FitnessABC):
    def __init__(self, value=0):
        self.value = value

    def is_fitter(self, other):
        return self.value > other.value

    def is_distinguishable(self, other):
        return self.value != other.value


class MockSElement(SElement):
    pass


class MockLineage:
    def __init__(self):
        self.parents = []


# Update the MockIndividual to use MockLineage
class MockIndividual(Individual):
    def __init__(self, fitness=None):
        super().__init__(MockSElement)
        self._lineage = MockLineage()
        self.fitness = fitness if fitness is not None else MockFitness()


def test_not_finalized_individuals(mock_population):
    mock_population._individuals = [MockIndividual(MockFitness()), MockIndividual(MockFitness(1))]


@pytest.fixture
def mock_population():
    return Population(MockSElement)


def test_population_initialization(mock_population):
    assert isinstance(mock_population, Population)
    assert mock_population.top_frame == MockSElement


def test_individuals_access(mock_population):
    mock_population._individuals = [MockIndividual(), MockIndividual()]
    assert len(mock_population.individuals) == 2
    assert all(isinstance(ind, MockIndividual) for ind in mock_population.individuals)


def test_extra_parameters(mock_population):
    mock_population._population_extra_parameters = {'param': 'value'}
    assert mock_population.population_extra_parameters == {'param': 'value'}


def test_generation_property(mock_population):
    mock_population.generation = 5
    assert mock_population.generation == 5


def test_iteration(mock_population):
    mock_population._individuals = [MockIndividual(), MockIndividual()]
    for idx, (index, individual) in enumerate(mock_population):
        assert isinstance(individual, MockIndividual)


# def test_not_finalized_individuals(mock_population):
#     # Make sure MockFitness is used correctly
#     mock_population._individuals = [MockIndividual(MockFitness()), MockIndividual(MockFitness(1))]
#     not_finalized = mock_population.not_finalized_individuals
#     assert len(not_finalized) == 1  # Update logic in Population class if necessary


# def test_finalized_individuals(mock_population):
#     # Ensure fitness objects are of the right type
#     mock_population._individuals = [MockIndividual(MockFitness(1)), MockIndividual()]
#     finalized = mock_population.finalized_individuals
#     assert len(finalized) == 1


def test_entropy(mock_population):
    mock_population._individuals = [MockIndividual(), MockIndividual()]
    assert isinstance(mock_population.entropy, float)


def test_getitem_and_len(mock_population):
    mock_population._individuals = [MockIndividual(), MockIndividual()]
    assert len(mock_population) == 2
    assert isinstance(mock_population[0], MockIndividual)


# def test_add_and_remove_individuals(mock_population):
#     individual = MockIndividual()
#     mock_population += [individual]
#     assert individual in mock_population._individuals
#     mock_population -= [individual]
#     assert individual not in mock_population._individuals


def test_string_representation(mock_population):
    mock_population._individuals = [MockIndividual(), MockIndividual()]
    result_str = str(mock_population)
    assert "Population" in result_str
    assert "MockSElement" in result_str


# def test_individual_dump(mock_population):
#     individual = MockIndividual()
#     mock_population += [individual]
#     dump_str = mock_population.dump_individual(0)
#     assert isinstance(dump_str, str)

# def test_sort(mock_population):
#     ind1 = MockIndividual(fitness=2)
#     ind2 = MockIndividual(fitness=1)
#     mock_population += [ind1, ind2]
#     mock_population.sort()
#     assert mock_population._individuals[0].fitness >= mock_population._individuals[1].fitness


# # def check_valid_types(obj, *valid_types: type, subclass: bool = False) -> bool:
# #     for valid in valid_types:
# #         if (not subclass and isinstance(obj, valid)) or (subclass and isinstance(obj, type) and issubclass(obj, valid)):
# #             return True

# #     expected_types = " or ".join([f"{v.__name__}" for v in valid_types])
# #     actual_type = type(obj).__name__
# #     logger.error(f"TypeError: invalid type {actual_type} for {repr(obj)}: expected {expected_types}")
# #     raise ByronError(PARANOIA_TYPE_ERROR)


if __name__ == "__main__":
    pytest.main()
