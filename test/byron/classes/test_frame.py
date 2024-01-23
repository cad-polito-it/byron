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
from byron.classes.frame import FrameABC, FrameSequence, FrameAlternative, FrameMacroBunch


class TestFrame(FrameABC):
    __test__ = False

    def __init__(self, parameters=None):
        super().__init__()
        self._parameters = parameters if parameters is not None else {}

    @property
    def successors(self) -> list[type["SElement"]]:
        return []


# Test cases for FrameABC
def test_frame_initialization():
    frame = TestFrame()
    assert frame._checks == []


def test_frame_str_representation():
    frame = TestFrame()
    assert str(frame) == frame.__class__.__name__


def test_frame_valid_property():
    frame = TestFrame()
    assert frame.valid == True  # Assuming the default behavior


def test_frame_successors_property():
    frame = TestFrame()
    assert frame.successors == []


def test_frame_run_paranoia_checks():
    frame = TestFrame()
    assert frame.run_paranoia_checks() is True  # Assuming it returns True


def test_frame_name_class_method():
    assert TestFrame.name == "TestFrame"


def test_frame_shannon_property():
    frame = TestFrame()
    assert frame.shannon == [hash(frame.__class__)]


def test_frame_sequence_instantiation():
    assert FrameSequence() is not None


def test_frame_alternative_instantiation():
    assert FrameAlternative() is not None


def test_frame_macro_bunch_instantiation():
    assert FrameMacroBunch() is not None


def test_frame_initialization_with_parameters():
    params = {'param1': 'value1', 'param2': 'value2'}
    frame = TestFrame(parameters=params)
    assert frame._parameters == params


def test_frame_equality():
    frame1 = TestFrame()
    frame2 = TestFrame()
    # Assuming the equality is not defined, they should not be equal
    assert frame1 != frame2


def test_frame_method_output():
    frame = TestFrame()
    assert frame.run_paranoia_checks() == True  # Default behavior


def test_frame_complex_return_type():
    frame = TestFrame()
    # Testing the type of the return value from successors
    assert isinstance(frame.successors, list)


def test_frame_class_attributes():
    # This tests the class method 'name'
    assert TestFrame.name == "TestFrame"
