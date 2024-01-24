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
import byron as byron


def test_integer_parameter():
    param = byron.framework.integer_parameter(1, 10)

    assert issubclass(param, byron.classes.ParameterABC)
    assert param.MIN == 1
    assert param.MAX == 10

    instance = param()
    instance.mutate(0.5)
    assert 1 <= instance.value < 10

    assert not instance.is_valid(10)
    assert not instance.is_valid("2")


def test_float_parameter():
    param = byron.framework.float_parameter(0.0, 1.0)

    assert issubclass(param, byron.classes.ParameterABC)
    assert param.MIN == 0.0
    assert param.MAX == 1.0

    instance = param()
    instance.mutate(0.5)
    assert 0.0 <= instance.value < 1.0

    assert not instance.is_valid(1.5)
    assert not instance.is_valid("0.5")


def test_choice_parameter():
    param = byron.framework.choice_parameter(["A", "B", "C"])

    assert issubclass(param, byron.classes.ParameterABC)
    assert param.ALTERNATIVES == ("A", "B", "C")

    instance = param()
    instance.mutate(0.5)
    assert instance.value in {"A", "B", "C"}

    assert not instance.is_valid("D")


def test_array_parameter():
    param = byron.framework.array_parameter(["0", "1"], 4)

    assert issubclass(param, byron.classes.ParameterABC)
    assert param.DIGITS == ("0", "1")
    assert param.LENGTH == 4

    instance = param()
    initial_value = instance.value
    instance.mutate(1.0)

    assert instance.value != initial_value


def test_integer_parameter():
    param = byron.framework.integer_parameter(1, 10)
    assert isinstance(param, type)
    assert issubclass(param, byron.classes.ParameterABC)
    assert param.MIN == 1
    assert param.MAX == 10
    instance = param()
    assert instance.run_paranoia_checks()
    assert instance.is_valid(5)
    assert not instance.is_valid(11)
    assert instance.mutate(0.5) is None


def test_float_parameter():
    param = byron.framework.float_parameter(1.0, 10.0)
    assert isinstance(param, type)
    assert issubclass(param, byron.classes.ParameterABC)
    assert param.MIN == 1.0
    assert param.MAX == 10.0
    instance = param()
    assert instance.run_paranoia_checks()
    assert instance.is_valid(5.0)
    assert not instance.is_valid(11.0)
    assert instance.mutate(0.5) is None


def test_choice_parameter():
    param = byron.framework.choice_parameter(["A", "B", "C"])
    assert isinstance(param, type)
    assert issubclass(param, byron.classes.ParameterABC)
    assert param.ALTERNATIVES == ("A", "B", "C")
    instance = param()
    assert instance.run_paranoia_checks()
    assert instance.is_valid("A")
    assert not instance.is_valid("D")
    assert instance.mutate(0.5) is None


def test_array_parameter():
    param = byron.framework.array_parameter(["0", "1"], 3)
    assert isinstance(param, type)
    assert issubclass(param, byron.classes.ParameterABC)
    assert param.DIGITS == ("0", "1")
    assert param.LENGTH == 3
    instance = param()
    assert instance.run_paranoia_checks()
    assert instance.is_valid("010")
    assert not instance.is_valid("012")
    assert not instance.is_valid("01")
    assert instance.mutate(1.0) is None
    with pytest.raises(NotImplementedError):
        instance.mutate(0.5)


def test_integer_parameter_range():
    with pytest.raises(byron.user_messages.ByronError):
        byron.framework.integer_parameter(1, 2)


def test_float_parameter_check_valid_type():
    with pytest.raises(byron.user_messages.ByronError):
        byron.framework.float_parameter("invalid", 10.0)


def test_integer_parameter_range():
    with pytest.warns(SyntaxWarning):
        byron.framework.integer_parameter(1, 2)


def test_choice_parameter_check_size():
    with pytest.warns(SyntaxWarning):
        byron.f.parameter.choice_parameter(list(range(1000)))
