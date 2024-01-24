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
