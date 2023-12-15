#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron

byron.rrandom.seed()
var = byron.f.macro("{v}", v=byron.f.choice_parameter("abcde"))
num = byron.f.macro("{n}", n=byron.f.integer_parameter(0, 100 + 1))
terminal = byron.f.alternative([var, num])
open = byron.f.macro("(")
close = byron.f.macro(")")
operations = byron.f.macro("{op}", op=byron.f.choice_parameter("+-*/"))

bnf = byron.f.bnf(
    [[terminal], [open, byron.f.SELF, operations, byron.f.SELF, close]], extra_parameters={"_text_after_macro": ""}
)

SEED = 59
byron.rrandom.seed(SEED)
P = byron.classes.Population(top_frame=bnf, fitness_function=None)
P.add_random_individual()
print(P.dump_individual(len(P.individuals) - 1))

exit()

zap = list()
P = byron.Population(top_frame=bnf, fitness_function=None)
for x in tqdm(range(10)):
    byron.rrandom.seed(SEED)
    P.add_random_individual()
    txt = P.dump_individual(
        len(P.individuals) - 1, extra_parameters={"$dump_node_info": False, "_text_after_macro": " "}
    )
    zap.append(txt)

assert all(i == zap[0] for i in zap)

pass
