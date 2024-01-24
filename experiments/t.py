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
