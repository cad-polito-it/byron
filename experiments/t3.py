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

import byron

byte = byron.f.integer_parameter(0, 256)
reg = byron.f.choice_parameter(["ax", "bx", "cx"])
macro1 = byron.f.macro("{reg} = {val:#x}  ; hey {reg}", reg=reg, val=byte)
macro2 = byron.f.macro("jmp {target}", target=byron.f.local_reference(backward=False, loop=False))
sub = byron.f.bunch([macro1], size=(5, 11), name="xxx")
macro3 = byron.f.macro("call {target}", target=byron.f.global_reference("xxx"))
prog = byron.f.bunch([macro1, macro2, macro3], size=20)
pop = byron.classes.Population(prog, None)
pop.add_random_individual()
pop.individuals[0]
