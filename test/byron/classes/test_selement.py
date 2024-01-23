# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest
import logging
from byron.classes.selement import SElement


class TestSElement:
    def test_instantiation(self):
        element = SElement()
        assert isinstance(element, SElement)

    def test_equality(self):
        element1 = SElement()
        element2 = SElement()
        assert element1 != element2
        assert element1 == element1

    def test_representation(self):
        element = SElement()
        expected_repr = f"<SElement at {hex(id(element))}>"
        assert repr(element) == expected_repr

    def test_hash(self):
        element = SElement()
        assert hash(element) == id(element)

    def test_add_node_check(self):
        def dummy_check(node):
            return True

        SElement.add_node_check(dummy_check)
        assert dummy_check in SElement.NODE_CHECKS

    def test_is_valid(self):
        def always_true_check(node):
            return True

        SElement.add_node_check(always_true_check)
        element = SElement()
        assert element.is_valid(None) is True


@pytest.fixture
def cleanup_node_checks():
    yield
    SElement.NODE_CHECKS = []


@pytest.mark.usefixtures("cleanup_node_checks")
class TestSElementWithCleanup(TestSElement):
    pass
