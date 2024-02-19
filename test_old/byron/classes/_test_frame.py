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
from typing import Type
import pytest

import byron as byron


class FrameConcrete(byron.classes.FrameABC):
    _name_counter = {}

    def mutate(self, strength: float = 1.0) -> None:
        pass

    @property
    def successors(self) -> list[Type['byron.classes.FrameABC'] | Type[byron.classes.Macro]]:
        return []


def test_frame_instance_creation():
    frame_instance = FrameConcrete(parameters={'test': 'test'})
    assert frame_instance._parameters == {'test': 'test'}


def test_frame_eq_method():
    frame_instance1 = FrameConcrete()
    frame_instance2 = FrameConcrete()
    assert frame_instance1 == frame_instance2


def test_frame_dump_method():
    frame_instance = FrameConcrete()
    assert frame_instance.dump(byron.classes.ValueBag()) == ''


def test_frame_is_valid():
    frame_instance = FrameConcrete()
    assert frame_instance.is_valid(None) == True
