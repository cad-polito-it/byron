# !/usr/bin/env python3
# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
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
