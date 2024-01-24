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

import warnings
import pytest

import byron
import byron as byron


def test_messaging():
    with pytest.deprecated_call():
        byron.user_messages.deprecation_warning("This feature is deprecated.")

    with pytest.warns(UserWarning):
        byron.user_messages.user_warning("This code may have unexpected behavior for end users.")

    with pytest.warns(RuntimeWarning):
        byron.user_messages.performance_warning("This code may be slow.")

    with pytest.warns(RuntimeWarning):
        byron.user_messages.runtime_warning("This code may have unexpected behavior.")

    with pytest.warns(SyntaxWarning):
        byron.user_messages.syntax_warning("This code may have syntax errors or other issues.")
