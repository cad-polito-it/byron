###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import MagicMock

import pytest

import byron as byron


@pytest.fixture
def mock_frame():
    return MagicMock(spec=byron.classes.frame.FrameABC)


@pytest.fixture
def mock_evaluator():
    return MagicMock(spec=byron.classes.evaluator.EvaluatorABC)


@pytest.fixture
def mock_individual():
    return MagicMock(spec=byron.classes.individual.Individual)


@pytest.fixture
def population(mock_frame, mock_evaluator):
    return byron.classes.Population(top_frame=mock_frame, evaluator=mock_evaluator)


def test_mu_setter(population):
    population.mu = 10
    assert population.mu == 10


def test_lambda_setter(population):
    population.lambda_ = 10
    assert population.lambda_ == 10


def test_individuals_property(population):
    assert isinstance(population.individuals, list)


def test_parameters_property(population):
    assert isinstance(population.population_extra_parameters, dict)


def test_evaluate(population, mock_individual):
    population._individuals = [mock_individual]
    population.evaluate()
    assert mock_individual.fitness is not None
