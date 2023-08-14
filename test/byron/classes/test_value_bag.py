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


def test_valuebag_init():
    vb = byron.classes.ValueBag()
    assert dict(vb) == {}

    vb = byron.classes.ValueBag({"a": 1, "b": 2, "$c": 3})
    assert dict(vb) == {"a": 1, "b": 2}

    vb = byron.classes.ValueBag(a=1, b=2, c=3)
    assert dict(vb) == {"a": 1, "b": 2, "c": 3}


def test_valuebag_readonly():
    vb = byron.classes.ValueBag({"a": 1, "b": 2, "$c": 3})
    with pytest.raises(NotImplementedError):
        vb["d"] = 4

    with pytest.raises(NotImplementedError):
        del vb["a"]

    with pytest.raises(NotImplementedError):
        vb.d = 4

    with pytest.raises(NotImplementedError):
        del vb.a


def test_valuebag_missing():
    vb = byron.classes.ValueBag({"a": 1, "b": 2, "$c": 3})
    assert vb["d"] is None

    assert vb["$d"] is False


def test_valuebag_safe_keys():
    vb = byron.classes.ValueBag({"a": 1, "b": 2, "$c": 3})
    assert vb.a == 1
    assert vb.b == 2

    assert vb.d is None

    assert vb["$e"] is False


def test_valuebag_key_filtering():
    vb = byron.classes.ValueBag({"a": 1, "b": 2, "$c": 3, "$d": 4, "e": 5})
    assert set(vb.keys()) == {"a", "b", "e"}
    assert set(vb.values()) == {1, 2, 5}
    assert set(vb.items()) == {("a", 1), ("b", 2), ("e", 5)}

    assert set(vb._keys()) == {"a", "b", "$c", "$d", "e"}
    assert set(vb._values()) == {1, 2, 3, 4, 5}
    assert set(vb._items()) == {("a", 1), ("b", 2), ("$c", 3), ("$d", 4), ("e", 5)}
