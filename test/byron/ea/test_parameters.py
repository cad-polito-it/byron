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

import logging
import byron


def test_shared():
    # byron.logger.setLevel(logging.WARNING)

    p = byron.f.integer_parameter(0, 10_000_000)
    for p in [
        byron.f.integer_parameter(0, 10_000_000),
        byron.f.float_parameter(0, 1.0),
        byron.f.choice_parameter(range(10_000)),
        byron.f.array_parameter("01X", 256),
    ]:
        s = byron.f.make_shared_parameter(p)

        i1 = s()
        i2 = s()
        assert i1.value == i2.value
        i1.mutate(1)
        assert i1.value == i2.value
        tmp = i1.value
        i2.mutate()
        assert i1.value == i2.value
        assert i1.value == tmp

        s2 = byron.f.make_shared_parameter(p)
        i3 = s2()
        i3.mutate()
        assert i1.value == i2.value
        assert i1.value != i3.value
