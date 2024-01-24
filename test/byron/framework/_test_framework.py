# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest
from typing import Type
import byron as byron


class TestAlternative:
    class MockFrame(byron.classes.FrameABC):
        pass

    class MockMacro(byron.classes.Macro):
        pass

    @pytest.fixture
    def mock_frame(self):
        return self.MockFrame

    @pytest.fixture
    def mock_macro(self):
        return self.MockMacro

    def test_alternative_with_valid_input(self, mock_frame, mock_macro):
        result = byron.f.alternative([mock_frame, mock_macro], name="test")
        assert isinstance(result, Type)
        assert issubclass(result, byron.classes.FrameABC)
        assert result.ALTERNATIVES == (mock_frame, mock_macro)

    def some_test(self):
        print(byron.f.alternative(["smth here should be a class"]))

    # def test_alternative_with_invalid_input(self):
    #     with pytest.raises(AssertionError):
    #         alternative(['not a class'])

    # def test_alternative_with_no_input(self):
    #     with pytest.raises(AssertionError):
    #         alternative([])

    def test_alternative_with_only_frame(self, mock_frame):
        result = byron.f.alternative([mock_frame])
        assert isinstance(result, Type)
        assert issubclass(result, byron.classes.FrameABC)
        assert result.ALTERNATIVES == (mock_frame,)

    def test_alternative_with_only_macro(self, mock_macro):
        result = byron.f.alternative([mock_macro])
        assert isinstance(result, Type)
        assert issubclass(result, byron.classes.FrameABC)
        assert result.ALTERNATIVES == (mock_macro,)


# MARCO TEST ON FRAMEWORK


def test_sequence():
    t1 = "abc"
    p1 = byron.f.integer_parameter(0, 4)
    m1 = byron.f.macro("test number {p1}", p1=p1)
    s1 = byron.f.sequence([m1])
    s2 = byron.f.sequence([s1])
    s3 = byron.f.sequence([t1])

    a = s1()
    b = s1()
    c = s2()
    d = s3()
    assert a is not None
    assert len(a.successors) == 1
    assert a == b

    assert a != c
    assert len(c.successors) == 1
    for e in c.successors:
        assert e == s1

    assert a != d
    assert c != d
    assert len(d.successors) == 1
    for e in d.successors:
        assert type(t1) != type(e)
        assert type(e) == type(m1)

    with pytest.raises(byron.user_messages.ByronError):
        byron.f.sequence(12)


def test_bunch():
    p1 = byron.f.integer_parameter(0, 4)
    m1 = byron.f.macro("test number {p1}", p1=p1)
    m2 = byron.f.macro("test number {p2}", p2=p1)
    m3 = byron.f.macro("test number {p3}", p3=p1)
    b1 = byron.f.bunch(m1, (2, 4))
    b2 = byron.f.bunch(m1, (2, 5))
    b3 = byron.f.bunch(m1)
    b4 = byron.f.bunch([m1, m2, m3], (4, 7))

    a = b1()
    b = b1()
    c = b2()
    d = b3()
    e = b4()

    assert a is not None
    assert len(a.successors) in [2, 3]
    assert a.successors[0] == m1
    assert a == b
    assert a != c
    assert len(d.successors) == 1
    assert all(i in [m1, m2, m3] for i in e.successors)

    with pytest.raises(byron.user_messages.ByronError):
        byron.f.bunch(p1)
