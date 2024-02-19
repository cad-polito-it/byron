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

import pickle
import byron


class Integer2(byron.classes.FitnessABC, int):
    """A single numeric value -- Larger is better."""

    def __new__(cls, *args, **kw):
        return int.__new__(cls, *args, **kw)

    def _decorate(self):
        return str(int(self))


f = byron.fit.make_fitness(4)
# f = Integer2(4)
print(pickle.dumps(f))
