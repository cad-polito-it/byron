#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest

import byron as byron


class MutableValueBag(byron.classes.ValueBag):
    def __setitem__(self, key, value):
        self.__dict__[key] = value


def test_macro_zero():
    mz = byron.classes.readymade_macros.MacroZero()
    assert isinstance(mz, byron.classes.readymade_macros.MacroZero)
    assert hasattr(mz, "TEXT")
    assert hasattr(mz, "EXTRA_PARAMETERS")
    assert hasattr(mz, "_parameter_types")
    assert mz.TEXT.startswith("{_comment} Automagically generated by byron")
    assert mz.EXTRA_PARAMETERS == dict()
    assert mz._parameter_types == dict()


def test_info():
    info = byron.classes.readymade_macros.Info()
    assert isinstance(info, byron.classes.readymade_macros.Info)
    assert hasattr(info, "TEXT")
    assert hasattr(info, "EXTRA_PARAMETERS")
    assert hasattr(info, "_parameter_types")
    assert info.TEXT.startswith("{_comment} [INFO] NOW: ")
    assert info.EXTRA_PARAMETERS == dict()
    assert info._parameter_types == dict()


def test_macro_zero_creation():
    mz = byron.classes.readymade_macros.MacroZero()
    assert isinstance(mz, byron.classes.readymade_macros.MacroZero)


def test_info_creation():
    info = byron.classes.readymade_macros.Info()
    assert isinstance(info, byron.classes.readymade_macros.Info)


def test_macro_equality():
    mz1 = byron.classes.readymade_macros.MacroZero()
    mz2 = byron.classes.readymade_macros.MacroZero()
    assert mz1 == mz2

    info1 = byron.classes.readymade_macros.Info()
    info2 = byron.classes.readymade_macros.Info()
    assert info1 == info2

    assert mz1 != info1
