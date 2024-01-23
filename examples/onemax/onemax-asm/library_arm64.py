# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron

COMMENT = ';'

# Hacked as a blind monkey using <https://godbolt.org/>


def define_frame():
    register = byron.f.choice_parameter([f"x{n}" for n in range(4)])
    int8 = byron.f.integer_parameter(0, 2**8)
    int16 = byron.f.integer_parameter(0, 2**16)

    # operations_rrr = byron.f.choice_parameter(['add', 'sub', 'and', 'eon', 'eor'])
    operations_rrr = byron.f.choice_parameter(['add', 'sub'])
    operations_rri = byron.f.choice_parameter(['add', 'sub'])
    op_rrr = byron.f.macro('{op} {r1}, {r2}, {r3}', op=operations_rrr, r1=register, r2=register, r3=register)
    op_rri = byron.f.macro('{op} {r1}, {r2}, #{imm:#x}', op=operations_rri, r1=register, r2=register, imm=int8)

    conditions = byron.f.choice_parameter(
        ['eq', 'ne', 'cs', 'hs', 'cc', 'lo', 'mi', 'pl', 'vs', 'vc', 'hi', 'ls', 'ge', 'lt', 'gt', 'le', 'al']
    )
    branch = byron.f.macro(
        'b{cond} {label}', cond=conditions, label=byron.f.local_reference(backward=True, loop=False, forward=True)
    )

    prologue_main = byron.f.macro(
        r"""; [prologue_main]
.section	__TEXT,__text,regular,pure_instructions
.globl	_onemax                         ; -- Begin function onemax
.p2align	2
_onemax:                                ; @onemax
.cfi_startproc
stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
.cfi_def_cfa_offset 16
mov x0, #{init}
mov x1, #{init}
mov x2, #{init}
mov x3, #{init}
add x0, x0, #0
; [end-prologue_main]""",
        init=byron.f.integer_parameter(-15, 16),
    )

    epilogue_main = byron.f.macro(
        r"""; [epilogue_main]
ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
ret
.cfi_endproc
; [end-epilogue_main]"""
    )

    prologue_sub = byron.f.macro(
        r"""
; [prologue_sub]
.globl	{_node}             ; -- Begin function {_node}
.p2align	2
{_node}:
.cfi_startproc
sub	sp, sp, #16
; [end-epilogue_sub]""",
        _label='',  # No automatic creation of the label -- it's embedded as "{_node}:"
    )

    epilogue_sub = byron.f.macro(
        r"""; [epilogue_sub]
str	x8, [sp, #8]
add	sp, sp, #16
ret
.cfi_endproc
; [end-epilogue_sub]"""
    )

    core_sub = byron.framework.bunch(
        [op_rrr, op_rri, branch],
        size=(1, 5 + 1),
        weights=[operations_rrr.NUM_ALTERNATIVES, operations_rri.NUM_ALTERNATIVES, 1],
    )
    sub = byron.framework.sequence([prologue_sub, core_sub, epilogue_sub])
    branch_link = byron.f.macro("bl {label}", label=byron.f.global_reference(sub, creative_zeal=1, first_macro=True))

    core_main = byron.framework.bunch(
        [op_rrr, op_rri, branch, branch_link],
        size=(10, 15 + 1),
        weights=[operations_rrr.NUM_ALTERNATIVES, operations_rri.NUM_ALTERNATIVES, 1, 1],
    )
    main = byron.framework.sequence([prologue_main, core_main, epilogue_main])

    return main
