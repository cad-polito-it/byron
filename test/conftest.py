# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest

from collections import defaultdict


def pytest_addoption(parser):
    parser.addoption("--all", action="store_true", default=False, help="run all tests (including 'avoidable' ones)")


def pytest_configure(config):
    config.addinivalue_line("markers", "avoidable: mark test as avoidable (require --all)")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--all"):
        return
    skip_avoidable = pytest.mark.skip(reason="need --all option to run")
    for item in items:
        if "avoidable" in item.keywords:
            item.add_marker(skip_avoidable)


@pytest.fixture(scope='module')
def individuals():
    _individuals = defaultdict(list)
    yield _individuals
