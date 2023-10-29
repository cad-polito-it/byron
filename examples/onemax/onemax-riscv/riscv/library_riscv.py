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

COMMENT = '#'

def define_frame():
    register = byron.f.choice_parameter([f"t{n}" for n in range(4)])
    int8 = byron.f.integer_parameter(0, 2 ** 8)

    operations_rrr = byron.f.choice_parameter(['add', 'sub'])
    operations_rri = byron.f.choice_parameter(['addi'])
    op_rrr = byron.f.macro('{op} {r1}, {r2}, {r3}', op=operations_rrr, r1=register, r2=register, r3=register)
    op_rri = byron.f.macro('{op} {r1}, {r2}, {imm:#x}', op=operations_rri, r1=register, r2=register, imm=int8)

    conditions = byron.f.choice_parameter(
        ['eq', 'ne', 'ge', 'lt', 'geu', 'ltu']
    )
    branch = byron.f.macro(
        'b{cond} {r1}, {r2}, {label}', cond=conditions, r1=register, r2=register, label=byron.f.local_reference(backward=True, loop=False, forward=True)
    )
    jump = byron.f.macro(
        'j {label}', label=byron.f.local_reference(backward=True, loop=False, forward=True)
    )

    prologue_main = byron.f.macro(
        r"""# [prologue_main]
.global _start
.equ sys_exit, 93

.section .text
_start:
# [end-prologue_main]"""
    )

    epilogue_main = byron.f.macro(
        r"""# [epilogue_main]
li a7, sys_exit
li a0, 0
ecall
# [end-epilogue_main]"""
    )

    core_main = byron.framework.bunch(
        [op_rrr, op_rri],
        size=(10, 15 + 1),
        weights=[operations_rrr.NUM_ALTERNATIVES, operations_rri.NUM_ALTERNATIVES],
    )

    main = byron.framework.sequence([prologue_main, core_main, epilogue_main])

    return main