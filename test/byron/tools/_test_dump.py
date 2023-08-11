#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest
import byron.tools.dump as byron


class TestObject:
    def __init__(self, key_to_raise=None):
        self.key_to_raise = key_to_raise

    def dump(self, **kwargs):
        if self.key_to_raise and self.key_to_raise not in kwargs:
            raise KeyError(self.key_to_raise)
        else:
            return f"success: {kwargs.get(self.key_to_raise, '')}"


def test_safe_dump():
    obj = TestObject()
    assert byron.safe_dump(obj) == "success: "

    obj = TestObject("key")
    assert byron.safe_dump(obj) == "success: {key}"

    obj = TestObject("key")
    assert byron.safe_dump(obj, key="value") == "success: value"


class TestObjectException(Exception):
    pass


class TestObjectWithException:
    def __init__(self, exception):
        self.exception = exception

    def dump(self, **kwargs):
        raise self.exception


def test_safe_dump_with_general_exception():
    obj = TestObjectWithException(TestObjectException())
    with pytest.raises(TestObjectException):
        byron.safe_dump(obj)


def test_safe_dump_with_key_error_exception():
    obj = TestObjectWithException(KeyError("key"))
    with pytest.raises(KeyError):
        byron.safe_dump(obj)
