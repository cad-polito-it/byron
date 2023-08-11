#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
#   __                          (`/\                                        #
#  |  |--.--.--.----.-----.-----`=\/\   This file is part of byron v0.1     #
#  |  _  |  |  |   _|  _  |     |`=\/\  An evolutionary optimizer & fuzzer  #
#  |_____|___  |__| |_____|__|__| `=\/  https://github.com/squillero/byron  #
#        |_____|                     \                                      #
#############################################################################
# Copyright 2022-23 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import warnings
import pytest

import byron
import byron as byron


def test_messaging():
    with pytest.deprecated_call():
        byron.user_messages.deprecation("This feature is deprecated.")

    with pytest.warns(UserWarning):
        byron.user_messages.user_warning("This code may have unexpected behavior for end users.")

    with pytest.warns(RuntimeWarning):
        byron.user_messages.performance("This code may be slow.")

    with pytest.warns(RuntimeWarning):
        byron.user_messages.runtime_warning("This code may have unexpected behavior.")

    with pytest.warns(SyntaxWarning):
        byron.user_messages.syntax_warning("This code may have syntax errors or other issues.")
