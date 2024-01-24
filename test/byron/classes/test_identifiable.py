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
from byron.classes.identifiable import IdentifiableABC


class MockIdentifiable(IdentifiableABC):
    def __init__(self, identity):
        self._id = identity

    @property
    def _identity(self):
        return self._id


# Test cases
def test_identifiable_hash():
    obj = MockIdentifiable('id123')
    assert hash(obj) == hash('id123')


def test_identifiable_equality():
    obj1 = MockIdentifiable('id123')
    obj2 = MockIdentifiable('id123')
    obj3 = MockIdentifiable('id456')
    assert obj1 == obj2
    assert obj1 != obj3


def test_identifiable_equality_with_different_class():
    obj1 = MockIdentifiable('id123')
    obj2 = 'id123'  # Different type
    assert obj1 != obj2


def test_identifiable_equality_with_none():
    obj1 = MockIdentifiable('id123')
    assert obj1 != None


# from abc import ABC, abstractmethod


# class IdentifiableABC(ABC):
#     @property
#     @abstractmethod
#     def _identity(self):
#         pass

#     def __hash__(self):
#         return hash(self._identity)

#     def __eq__(self, other):
#         if other is None or not isinstance(other, self.__class__):
#             return False
#         else:
#             return self._identity == other._identity
