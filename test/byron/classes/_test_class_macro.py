#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest
import byron as byron


@pytest.fixture
def macro():
    class TestMacro(byron.classes.Macro):
        TEXT = "test"
        PARAMETERS = {}
        EXTRA_PARAMETERS = {}

    return TestMacro()


@pytest.fixture
def parameter_abc():
    class TestParameterABC(byron.classes.ParameterABC):
        def mutate(self, strength: float = 1.0) -> None:
            pass

    return TestParameterABC()


@pytest.fixture
def node_view():
    class TestNodeView(byron.classes.NodeView):
        def __init__(self):
            pass

    return TestNodeView()


def test_macro_initialization(macro):
    assert isinstance(macro, byron.classes.Macro)
    assert isinstance(macro, byron.classes.EvolvableABC)
    assert isinstance(macro, byron.classes.Checkable)
    assert macro.parameters == {}


def test_macro_eq(macro):
    same_macro = macro
    assert macro == same_macro

    different_macro = byron.classes.Macro()
    assert macro != different_macro


def test_macro_is_valid(macro, node_view):
    assert macro.is_valid(node_view)


def test_macro_text(macro):
    assert macro.text == "test"


def test_macro_extra_parameters(macro):
    assert macro.extra_parameters == {}


def test_macro_parameter_types(macro):
    assert macro.parameter_types == {}


def test_macro_str(macro):
    assert str(macro) == "TestMacro"


def test_macro_dump(macro):
    extra_parameters = byron.classes.ValueBag({"test": "value"})
    assert macro.dump(extra_parameters) == "test"


def test_macro_mutate(macro, parameter_abc):
    macro.parameters = {"test": parameter_abc}
    macro.mutate(0.5)


def test_macro_is_name_valid():
    assert byron.classes.Macro.is_name_valid("test")
    assert not byron.classes.Macro.is_name_valid(123)
