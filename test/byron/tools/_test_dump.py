#!/usr/bin/env python3
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
import byron.tools.create_test_individual as byron


class TestObject:
    def __init__(self, key_to_raise=None):
        self.key_to_raise = key_to_raise

    def dump(self, **kwargs):
        if self.key_to_raise and self.key_to_raise not in kwargs:
            raise KeyError(self.key_to_raise)
        else:
            return f"success: {kwargs.get(self.key_to_raise, '')}"


class TestObjectException(Exception):
    pass


class TestObjectWithException:
    def __init__(self, exception):
        self.exception = exception

    def dump(self, **kwargs):
        raise self.exception
