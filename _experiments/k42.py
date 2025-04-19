# !/usr/bin/env python3
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0


class ByronException(Exception):
    """Base class for exceptions in byron."""

    def __init__(self):
        self.__foo = 0

    def foo(self):
        print(hasattr(self, "__foo"))
        self.__foo += 1
        print(hasattr(self, "__bar"))
        self.__bar += 1


x = ByronException()
x.foo()
