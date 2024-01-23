#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################

# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda

import byron


def test_framework():
    assert 'framework' == byron.FRAMEWORK


def test_link():
    assert 'link' == byron.LINK


def test_node_zero():
    assert 0 == byron.NODE_ZERO
