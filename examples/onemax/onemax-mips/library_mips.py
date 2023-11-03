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
    register = byron.f.choice_parameter([f"${x}" for x in range(4,27)])
    int8 = byron.f.integer_parameter(0, 2**8)

    operations_rrr = byron.f.choice_parameter(['add', 'sub', 'addu', 'subu'])
    operations_rri = byron.f.choice_parameter(['addi', 'addiu'])

    op_rrr = byron.f.macro('{op} {r1}, {r2}, {r3}', op=operations_rrr, r1=register, r2=register, r3=register)
    op_rri = byron.f.macro('{op} {r1}, {r2}, {imm}', op=operations_rri, r1=register, r2=register, imm=int8)

    conditions = byron.f.choice_parameter(
        ['eq', 'ne', 'ge', 'lt', 'gt', 'le']
    )
    branch = byron.f.macro(
        'b{cond} {r1}, {r2}, {label}',cond=conditions, r1=register, r2=register, label=byron.f.local_reference(backward=True, loop=False, forward=True)
    )
    prologue_main = byron.f.macro(
        r"""# [prologue main]
.text
.global onemax
onemax:
sw $31, $3
# [end-prologue main]
"""
    )
    epilogue_main = byron.f.macro(
        r"""# [epilogue main]
lw $31, $3
jr $ra
# [end-epilogue main]
"""
    )

    prologue_sub = byron.f.macro(
        r"""# [prologue sub]
addiu   $sp,$sp,-8
sw      $fp,4($sp)
move    $fp,$sp
# [end-prologue sub]
"""
    )
    epilogue_sub = byron.f.macro(
        r"""# [epilogue sub]
move    $sp,$fp
lw      $fp,4($sp)
addiu   $sp,$sp,8
jr      $31
# [end-epilogue sub]
"""
    )
    core_sub = byron.framework.bunch(
        [op_rrr, op_rri, branch],
        size=(1, 5 + 1),
        weights=[operations_rrr.NUM_ALTERNATIVES, operations_rri.NUM_ALTERNATIVES, 1],
    )
    sub = byron.framework.sequence([prologue_sub, core_sub, epilogue_sub])

    jump = byron.f.macro(
        'jal {label}', label=byron.f.global_reference(sub, creative_zeal=1, first_macro=True)
    )

    core_main = byron.framework.bunch(
        [op_rrr, op_rri, branch, jump],
        size=(10, 15 + 1),
        weights=[operations_rrr.NUM_ALTERNATIVES, operations_rri.NUM_ALTERNATIVES, 1, 1],
    )
    main = byron.framework.sequence([prologue_main, core_main, epilogue_main])

    return main
