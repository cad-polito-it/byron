#!/usr/bin/env python3
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

# logging.basicConfig(format="[%(asctime)s] %(levelname)s:%(message)s", datefmt="%H:%M:%S", level=logging.INFO)

import byron

r = byron.lib.choice_parameter_instance(["ax", "bx", "cx", "dx"])
v = byron.lib.integer_parameter_instance(0, 256)
t = "mov {reg}, 0x{val:x} // {val}"

m = byron.lib.Macro()
m.text = t
m["reg"] = r
m["val"] = v
logging.info("macro: %s", m)

m2 = byron.lib.Macro("Register:{a} Id1:{_id} Id2:{_id} Unset:{u}", a=r)
logging.info("macro: %s", m2)
