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
from byron.classes.value_bag import ValueBag


def test_valuebag_init():
    vb = ValueBag()
    assert isinstance(vb, ValueBag)


def test_valuebag_read_only():
    vb = ValueBag()
    with pytest.raises(NotImplementedError):
        vb['key'] = 'value'

    with pytest.raises(NotImplementedError):
        del vb['key']


def test_valuebag_missing():
    vb = ValueBag()
    assert vb.__missing__("$flag") is False
    assert vb.__missing__("normal_key") is None


def test_valuebag_safe_keys():
    vb = ValueBag({"safe_key": "value", "_private": "hidden"})
    assert "safe_key" in vb.keys()
    assert "_private" in vb.keys()


def test_valuebag_attr_access():
    vb = ValueBag({"safe_key": "value"})
    assert vb.safe_key == "value"


def test_valuebag_or_ior():
    vb1 = ValueBag({"key1": "value1"})
    vb2 = ValueBag({"key2": "value2"})
    vb3 = vb1 | vb2
    assert "key1" in vb3 and "key2" in vb3
    vb1 |= vb2
    assert "key2" in vb1


def test_valuebag_getattr_invalid():
    vb = ValueBag()
    assert vb.invalid_key is None


def test_valuebag_flag_keys():
    vb = ValueBag()
    assert vb["$missing_flag"] is False


def test_valuebag_update_or():
    vb1 = ValueBag({"key1": "value1"})
    vb2 = {"key2": "value2"}
    vb1 |= vb2
    assert "key2" in vb1


# todo add __hash__(self) in the value_bag
def test_valuebag_hashable():
    vb = ValueBag({"key": "value"})
    assert isinstance(hash(vb), int), "ValueBag should be hashable"


def test_valuebag_repr():
    vb = ValueBag({"key": "value"})
    assert isinstance(repr(vb), str)


def test_valuebag_iter():
    vb = ValueBag({"key1": "value1", "key2": "value2"})
    keys = [k for k in vb]
    assert "key1" in keys and "key2" in keys
