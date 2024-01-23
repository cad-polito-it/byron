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

import byron


def silly_check(nr):
    values = list()
    for s in nr.children:
        values.append(s.p.num)  # lazy fingers: s.p.num
    return sorted(values, reverse=True) == values


foo = byron.f.macro('foo {num}', num=byron.f.integer_parameter(-1000, +1000))
sorted_bunch = byron.f.bunch([foo], size=7)
sorted_bunch.add_node_check(silly_check)
byron.f.as_text(sorted_bunch)
