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

from math import sqrt
import pytest

import byron as byron


def test_simple():
    if byron.paranoia_mode:
        with pytest.raises(AssertionError):
            # TypeError: different types of fitness
            assert byron.fit.Scalar(13) <= byron.fit.Float(13)

    # SCALAR
    # nb. sqrt(2)**2 = 2.0000000000000004
    assert not byron.fit.Float(2) == byron.fit.Float(sqrt(2) ** 2)
    assert byron.fit.Float(2) != byron.fit.Float(sqrt(2) ** 2)
    assert not byron.fit.Float(2) > byron.fit.Float(sqrt(2) ** 2)
    assert not byron.fit.Float(2) >= byron.fit.Float(sqrt(2) ** 2)
    assert byron.fit.Float(2) < byron.fit.Float(sqrt(2) ** 2)
    assert byron.fit.Float(2) <= byron.fit.Float(sqrt(2) ** 2)
    #
    assert not byron.fit.Float(13) == byron.fit.Float(17)
    assert byron.fit.Float(13) != byron.fit.Float(17)
    assert not byron.fit.Float(13) > byron.fit.Float(17)
    assert not byron.fit.Float(13) >= byron.fit.Float(17)
    assert byron.fit.Float(13) < byron.fit.Float(17)
    assert byron.fit.Float(13) <= byron.fit.Float(17)

    # INTEGER
    assert byron.fit.Integer(13) == byron.fit.Integer(13)
    assert byron.fit.Integer(13) == byron.fit.Integer(13 + 0.01)
    assert byron.fit.Integer(13) != byron.fit.Integer(13 - 0.01)
    assert byron.fit.Integer(17) > byron.fit.Integer(13)
    assert byron.fit.Integer(17) >= byron.fit.Integer(13)
    assert not byron.fit.Integer(17) < byron.fit.Integer(13)
    assert not byron.fit.Integer(17) <= byron.fit.Integer(13)

    # SCALAR / APPROXIMATE
    # nb. sqrt(2)**2 = 2.0000000000000004
    assert byron.fit.Scalar(2) == byron.fit.Scalar(sqrt(2) ** 2)
    assert not byron.fit.Scalar(2) != byron.fit.Scalar(sqrt(2) ** 2)
    assert not byron.fit.Scalar(2) > byron.fit.Scalar(sqrt(2) ** 2)
    assert byron.fit.Scalar(2) >= byron.fit.Scalar(sqrt(2) ** 2)
    assert not byron.fit.Scalar(2) < byron.fit.Scalar(sqrt(2) ** 2)
    assert byron.fit.Scalar(2) <= byron.fit.Scalar(sqrt(2) ** 2)
    #
    assert not byron.fit.Scalar(13) == byron.fit.Scalar(17)
    assert byron.fit.Scalar(13) != byron.fit.Scalar(17)
    assert not byron.fit.Scalar(13) > byron.fit.Scalar(17)
    assert not byron.fit.Scalar(13) >= byron.fit.Scalar(17)
    assert byron.fit.Scalar(13) < byron.fit.Scalar(17)
    assert byron.fit.Scalar(13) <= byron.fit.Scalar(17)

    # REVERSE FITNESS (the smaller, the better -- ie. 2 > 3)
    rev_scalar = byron.fit.reverse_fitness(byron.fit.Float)
    assert not rev_scalar(2) == rev_scalar(sqrt(2) ** 2)
    assert rev_scalar(2) != rev_scalar(sqrt(2) ** 2)
    assert rev_scalar(2) > rev_scalar(sqrt(2) ** 2)
    assert rev_scalar(2) >= rev_scalar(sqrt(2) ** 2)
    assert not rev_scalar(2) < rev_scalar(sqrt(2) ** 2)
    assert not rev_scalar(2) <= rev_scalar(sqrt(2) ** 2)
    assert not rev_scalar(13) == rev_scalar(17)
    assert rev_scalar(13) != rev_scalar(17)
    assert rev_scalar(13) > rev_scalar(17)
    assert rev_scalar(13) >= rev_scalar(17)
    assert not rev_scalar(13) < rev_scalar(17)
    assert not rev_scalar(13) <= rev_scalar(17)
    #
    rev_approximate = byron.fit.reverse_fitness(byron.fit.Scalar)
    assert rev_approximate(2) == rev_approximate(sqrt(2) ** 2)
    assert not rev_approximate(2) != rev_approximate(sqrt(2) ** 2)
    assert not rev_approximate(2) > rev_approximate(sqrt(2) ** 2)
    assert rev_approximate(2) >= rev_approximate(sqrt(2) ** 2)
    assert not rev_approximate(2) < rev_approximate(sqrt(2) ** 2)
    assert rev_approximate(2) <= rev_approximate(sqrt(2) ** 2)
    assert not rev_approximate(13) == rev_approximate(17)
    assert rev_approximate(13) != rev_approximate(17)
    assert rev_approximate(13) > rev_approximate(17)
    assert rev_approximate(13) >= rev_approximate(17)
    assert not rev_approximate(13) < rev_approximate(17)
    assert not rev_approximate(13) <= rev_approximate(17)
    #
    if byron.paranoia_mode:
        with pytest.raises(AssertionError):
            # TypeError: different types of fitness
            assert rev_approximate(13) <= rev_scalar(13)

    # VECTOR of Scalars
    assert byron.fit.Lexicographic([23, 2], byron.fit.Float) == byron.fit.Lexicographic([23, 2], byron.fit.Float)
    assert not byron.fit.Lexicographic([23, 2], byron.fit.Float) != byron.fit.Lexicographic([23, 2], byron.fit.Float)
    assert not byron.fit.Lexicographic([23, 2], byron.fit.Float) == byron.fit.Lexicographic(
        [23, sqrt(2) ** 2], byron.fit.Float
    )
    assert byron.fit.Lexicographic([23, 2], byron.fit.Float) != byron.fit.Lexicographic(
        [23, sqrt(2) ** 2], byron.fit.Float
    )
    assert byron.fit.Lexicographic([23, 10], byron.fit.Float) == byron.fit.Lexicographic([23, 10], byron.fit.Float)
    assert not byron.fit.Lexicographic([23, 10], byron.fit.Float) == byron.fit.Lexicographic([10, 23], byron.fit.Float)
    assert byron.fit.Lexicographic([23, 10], byron.fit.Float) != byron.fit.Lexicographic([10, 23], byron.fit.Float)
    assert byron.fit.Lexicographic([23, 10], byron.fit.Float) > byron.fit.Lexicographic([10, 23], byron.fit.Float)
    assert byron.fit.Lexicographic([23, 10], byron.fit.Float) >= byron.fit.Lexicographic([10, 23], byron.fit.Float)
    assert not byron.fit.Lexicographic([23, 10], byron.fit.Float) < byron.fit.Lexicographic([10, 23], byron.fit.Float)
    assert not byron.fit.Lexicographic([23, 10], byron.fit.Float) <= byron.fit.Lexicographic([10, 23], byron.fit.Float)

    # VECTOR of Scalar
    assert byron.fit.Lexicographic([23, 2], byron.fit.Scalar) == byron.fit.Lexicographic([23, 2], byron.fit.Scalar)
    assert not byron.fit.Lexicographic([23, 2], byron.fit.Scalar) != byron.fit.Lexicographic([23, 2], byron.fit.Scalar)
    assert byron.fit.Lexicographic([23, 2], byron.fit.Scalar) == byron.fit.Lexicographic(
        [23, sqrt(2) ** 2], byron.fit.Scalar
    )
    assert not byron.fit.Lexicographic([23, 2], byron.fit.Scalar) != byron.fit.Lexicographic(
        [23, sqrt(2) ** 2], byron.fit.Scalar
    )
    assert not byron.fit.Lexicographic([23, 2], byron.fit.Scalar) == byron.fit.Lexicographic(
        [sqrt(2) ** 2, 23], byron.fit.Scalar
    )
    assert byron.fit.Lexicographic([23, 2], byron.fit.Scalar) != byron.fit.Lexicographic(
        [sqrt(2) ** 2, 23], byron.fit.Scalar
    )
    assert byron.fit.Lexicographic([23, 2], byron.fit.Scalar) > byron.fit.Lexicographic(
        [sqrt(2) ** 2, 23], byron.fit.Scalar
    )
    assert byron.fit.Lexicographic([23, 2], byron.fit.Scalar) >= byron.fit.Lexicographic(
        [sqrt(2) ** 2, 23], byron.fit.Scalar
    )
    assert not byron.fit.Lexicographic([23, 2], byron.fit.Scalar) < byron.fit.Lexicographic(
        [sqrt(2) ** 2, 23], byron.fit.Scalar
    )
    assert not byron.fit.Lexicographic([23, 2], byron.fit.Scalar) <= byron.fit.Lexicographic(
        [sqrt(2) ** 2, 23], byron.fit.Scalar
    )

    f1 = byron.fit.Vector([byron.fit.Float(2), byron.fit.Float(sqrt(2) ** 2)])
    f2 = byron.fit.Vector([byron.fit.Float(sqrt(2) ** 2), byron.fit.Float(2)])
    assert f1 != f2
    assert f1 < f2
    f1 = byron.fit.Vector([byron.fit.reverse_fitness(byron.fit.Float)(2), byron.fit.Float(sqrt(2) ** 2)])
    f2 = byron.fit.Vector([byron.fit.reverse_fitness(byron.fit.Float)(sqrt(2) ** 2), byron.fit.Float(2)])
    assert f1 != f2
    assert f1 > f2

    f1 = byron.fit.reverse_fitness(byron.fit.Vector)([byron.fit.Float(2), byron.fit.Float(sqrt(2) ** 2)])
    f2 = byron.fit.reverse_fitness(byron.fit.Vector)([byron.fit.Float(sqrt(2) ** 2), byron.fit.Float(2)])
    assert f1 != f2
    assert f1 > f2
