#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest
import byron as byron


class TestIdentifiable:
    def test_identity(self):
        class MyIdentifiable(byron.classes.IdentifiableABC):
            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)

        assert obj1._identity == 1
        assert obj2._identity == 2
        assert obj3._identity == 1

    def test_hash(self):
        class MyIdentifiable(byron.classes.IdentifiableABC):
            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)

        assert hash(obj1) != hash(obj2)
        assert hash(obj1) == hash(obj3)

    def test_eq(self):
        class MyIdentifiable(byron.classes.IdentifiableABC):
            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)
        obj4 = None
        obj5 = "not an IdentifiableABC object"

        assert obj1 == obj3
        assert obj1 != obj2
        assert obj1 != obj4
        assert obj1 != obj5
