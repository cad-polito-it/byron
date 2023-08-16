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

from typing import Sequence
import byron as byron
import pytest

PARANOIA_TYPE_ERROR = "TypeError (paranoia check)"
PARANOIA_VALUE_ERROR = "ValueError (paranoia check)"


def test_check_valid_type():
    assert byron.user_messages.check_valid_type(404, int) == True
    my_sequence: Sequence[int] = [1, 2, 3, 4, 5]
    assert byron.user_messages.check_valid_type(my_sequence, Sequence) == True
    try:
        byron.user_messages.check_valid_type("303", int)
    except byron.user_messages.exception.ByronError as e:
        assert str(e) == PARANOIA_TYPE_ERROR

    class someClass:
        pass

    class someSubClass(someClass):
        pass

    assert byron.user_messages.check_valid_type(someClass, object, False) == True


def test_check_valid_types():
    assert byron.user_messages.check_valid_types(42, int) == True
    assert byron.user_messages.check_valid_types("hello", str) == True
    assert byron.user_messages.check_valid_types([1, 2, 3], list) == True
    assert byron.user_messages.check_valid_types((1, 2, 3), tuple) == True
    assert byron.user_messages.check_valid_types({"a": 1, "b": 2}, dict) == True
    assert byron.user_messages.check_valid_types({1, 2, 3}, set) == True
    assert byron.user_messages.check_valid_types(3.14, (int, float)) == True
    assert byron.user_messages.check_valid_types("world", (str, list)) == True

    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_types(42, str)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_types("hello", int)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_types([1, 2, 3], tuple)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_types((1, 2, 3), list)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_types({"a": 1, "b": 2}, set)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_types({1, 2, 3}, dict)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_types(3.14, int)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_types("world", int)


def test_check_value_range():
    assert byron.user_messages.check_value_range(42, 0, 100) == True
    assert byron.user_messages.check_value_range(3.14, 0, 3.1416) == True
    assert byron.user_messages.check_value_range(-10, -100, 0) == True
    assert byron.user_messages.check_value_range(0, None, 10) == True
    assert byron.user_messages.check_value_range(10, 10, None) == True

    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_value_range(-10, 0, 100)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_value_range(3.14, 0, 3.0)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_value_range(100, -100, 0)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_value_range(10, None, 5)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_value_range(-10, -5, 0)


def test_check_valid_length():
    assert byron.user_messages.check_valid_length([1, 2, 3], 1, 4) == True
    assert byron.user_messages.check_valid_length("hello", 1, 6) == True
    assert byron.user_messages.check_valid_length([], None, 10) == True
    assert byron.user_messages.check_valid_length([1, 2, 3], 3, None) == True

    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_length([1, 2, 3], 4, None)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_length("hello", None, 3)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_length([], 1, 10)
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_valid_length([1, 2, 3], None, 2)


def test_check_no_duplicates():
    assert byron.user_messages.check_no_duplicates([1, 2, 3]) == True
    assert byron.user_messages.check_no_duplicates("helo") == True
    assert byron.user_messages.check_no_duplicates([[1, 2], [1, 4]]) == True
    assert byron.user_messages.check_no_duplicates([]) == True

    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_no_duplicates([1, 2, 3, 2])
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_no_duplicates("hello world")
    with pytest.raises(byron.user_messages.exception.ByronError):
        byron.user_messages.check_no_duplicates([1, 2, 3, 3, 4])
