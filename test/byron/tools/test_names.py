#!/usr/bin/env python3
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

import byron as byron
import pytest


def test_uncanonize_name():
    assert byron.tools.names.base_name('Jake❰Elwood❱') == 'Elwood'
    assert byron.tools.names.base_name('Jake❬Elwood❭') == 'Elwood'
    assert byron.tools.names.base_name('Jake<Elwood>') == 'Elwood'
    assert byron.tools.names.base_name('Jake❰Elwood#42❱') == 'Elwood'
    assert byron.tools.names.base_name('Jake❬Elwood#42❭') == 'Elwood'
    assert byron.tools.names.base_name('Jake<Elwood#42>') == 'Elwood'

    assert byron.tools.names.base_name('Jake❰Elwood❱', keep_number=True) == 'Elwood'
    assert byron.tools.names.base_name('Jake❬Elwood❭', keep_number=True) == 'Elwood'
    assert byron.tools.names.base_name('Jake<Elwood>', keep_number=True) == 'Elwood'
    assert byron.tools.names.base_name('Jake❰Elwood#42❱', keep_number=True) == 'Elwood#42'
    assert byron.tools.names.base_name('Jake❬Elwood#42❭', keep_number=True) == 'Elwood#42'
    assert byron.tools.names.base_name('Jake<Elwood#42>', keep_number=True) == 'Elwood#42'

    with pytest.raises(ValueError):
        byron.tools.names.base_name('Jake❰Elwood>')
