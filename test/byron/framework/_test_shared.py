#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron as byron


def test_make_shared_parameter():
    for p in [
        byron.f.integer_parameter(0, 10_000_000),
        byron.f.float_parameter(0, 1.0),
        byron.f.choice_parameter(range(10_000)),
        byron.f.array_parameter("01X", 256),
    ]:
        SharedParameter = byron.f.make_shared_parameter(p)
        shared_param1 = SharedParameter()
        shared_param2 = SharedParameter()

        assert shared_param1.value == shared_param2.value

        tmp = shared_param1.value
        shared_param1.mutate(1)
        assert shared_param1.value == shared_param2.value
        assert shared_param1.value != tmp

        SharedParameter2 = byron.f.make_shared_parameter(p)
        shared_param3 = SharedParameter2()

        tmp2 = shared_param3.value
        shared_param3.mutate()
        assert shared_param3.value != tmp2

        assert shared_param1.value != shared_param3.value
        assert shared_param2.value != shared_param3.value
