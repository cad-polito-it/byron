#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron as byron
import pytest


def test_canonize_name():
    assert byron.tools.names.canonize_name('foo', 'bar') == 'bar❬foo#1❭'
    assert byron.tools.names.canonize_name('foo', 'bar') == 'bar❬foo#2❭'
    assert byron.tools.names.canonize_name('baz', 'qux') == 'qux❬baz#1❭'

    assert byron.tools.names.canonize_name('foo', 'pippo', user=True) == 'pippo<foo>'

    assert byron.tools.names.canonize_name('thing', 'some', make_unique=False) == 'some❬thing❭'
    assert byron.tools.names.canonize_name('tag', 'some', make_unique=False) == 'some❬tag❭'

    assert byron.tools.names.canonize_name('foo', 'bar', user_space=True) == 'bar<foo#3>'
    assert byron.tools.names.canonize_name('foo', 'bar', user_space=True) == 'bar<foo#4>'


# user <>
# else ❬❭
def test_uncanonize_name():
    assert byron.tools.names.uncanonize_name("foo❬bar❭") == "bar"
    assert byron.tools.names.uncanonize_name("foo❬bar#1❭") == "bar"
    assert byron.tools.names.uncanonize_name("foo❬bar#1❭", keep_number=True) == "bar#1"
    assert byron.tools.names.uncanonize_name("foo<bar>", user=True) == "bar"
    assert byron.tools.names.uncanonize_name("foo<bar#1>") == "bar"
    assert byron.tools.names.uncanonize_name("foo<bar#1>", user=True, keep_number=True) == "bar#1"
    assert byron.tools.names.uncanonize_name("foo<smth>", user=True) == "smth"

    assert byron.tools.names.uncanonize_name("foo❬bar❭", user=False) == "bar"
    assert byron.tools.names.uncanonize_name("foo<bar>", user=False) == "foo<bar>"
    assert byron.tools.names.uncanonize_name("foo<bar#1>", user=False) == "foo<bar#1>"
    assert byron.tools.names.uncanonize_name("foo❬bar#3❭", user=False, keep_number=True) == "bar#3"
