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
from byron.classes.macro import Macro, ValueBag, NodeView
import math
import random


def test_macro_init():
    m = Macro()
    assert isinstance(m, Macro)


def test_macro_text():
    m = Macro()
    m.TEXT = "Sample text"
    assert m.text == "Sample text"


def test_macro_parameter_types():
    m = Macro()
    m.PARAMETERS = {"param1": int, "param2": str}
    assert m.parameter_types == {"param1": int, "param2": str}


def test_macro_dump():
    m = Macro()
    m.TEXT = "Hello, {name}"
    parameters = ValueBag({'name': 'World'})
    assert m.dump(parameters) == "Hello, World"


def test_macro_is_correct_valid():
    m = Macro()
    ref = object()
    nv = NodeView(ref)
    assert m.is_correct(nv) == True


def test_macro_shannon():
    m = Macro()
    assert isinstance(m.shannon, list)


def test_macro_is_name_valid_true():
    assert Macro.is_name_valid("valid_name123") == True


def test_macro_is_name_valid_false():
    assert Macro.is_name_valid("123Invalid") == False


def test_macro_handle_complex_parameter_types():
    m = Macro()
    m.PARAMETERS = {"param1": list, "param2": dict}
    assert m.parameter_types == {"param1": list, "param2": dict}


def test_macro_shannon_complexity():
    m = Macro()
    m.TEXT = "More {complex} example"
    parameters = ValueBag({'complex': 'complex_value'})
    complexity = calculate_shannon_index(m.dump(parameters))
    assert complexity > 0  # Shannon index should be greater than zero for non-trivial strings


def test_macro_output_regularity_and_randomness():
    m = Macro()
    m.TEXT = "Random {value}"
    outputs = set()
    for _ in range(100):  # Generate a number of outputs
        parameters = ValueBag({'value': random.randint(0, 100)})  # Generate random values
        outputs.add(m.dump(parameters))
    assert len(outputs) > 1  # Check for multiple unique outputs


def calculate_shannon_index(text):
    probability_dict = {char: float(text.count(char)) / len(text) for char in set(text)}
    shannon_index = -sum(p * math.log(p, 2) for p in probability_dict.values())
    return shannon_index


def test_macro_error_on_incorrect_formatting():
    m = Macro()
    m.TEXT = "This is a {broken} example"
    with pytest.raises(KeyError):  # Correct exception type for missing keys in format
        m.dump(ValueBag({}))


if __name__ == "__main__":
    pytest.main()
