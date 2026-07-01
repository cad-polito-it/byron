#!/usr/bin/env python3
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from isa.riscv_isa_builder import RiscvIsaBuilder, RiscvRegisters
from isa.riscv_isa_custom_operation_set import RiscvIsaCustomOperationSet

import byron

COMMENT = '#'


def define_frame():
    prologue_main = byron.f.macro(
        r"""# [prologue_main]
.global asm_call

.macro push reg
    addi sp, sp, -8
    sd \reg, 0(sp)
.endm

.macro pop reg
    ld \reg, 0(sp)
    addi sp, sp, 8
.endm

.section .text

asm_call: 
#Save return address
    push ra
#Save stack pointer
    #The sw is not abilitated to modify the sp as for now
#Save s register (callee convenction)
    push s0
    push s1
    push s2
    push s3
    push s4
    push s5
    push s6
    push s7
    push s8
    push s9
    push s10
    push s11
#Save the addresses of the return vectors    
    push a0     #saved vector ptr
    push a1     #temporaries vector ptr

#Init temporary at 0
    mv t0, zero
    mv t1, zero
    mv t2, zero
    mv t3, zero
    mv t4, zero
    mv t5, zero
    mv t6, zero
# [end-prologue_main]"""
    )

    epilogue_main = byron.f.macro(
        r"""# [epilogue_main]
#Store temporaries registers
    pop a0
    sd t0, 0(a0)
    sd t1, 8(a0)
    sd t2, 16(a0)
    sd t3, 24(a0)
    sd t4, 32(a0)
    sd t5, 40(a0)
    sd t6, 48(a0)
#Store saved registers
    pop a0
    sd s0, 0(a0)
    sd s1, 8(a0)
    sd s2, 16(a0)
    sd s3, 24(a0)
    sd s4, 32(a0)
    sd s5, 40(a0)
    sd s6, 48(a0)
    sd s7, 56(a0)
    sd s8, 64(a0)
    sd s9, 72(a0)
    sd s10, 80(a0)
    sd s11, 88(a0)

#Restore s register (callee convenction)
    pop s11
    pop s10
    pop s9
    pop s8
    pop s7
    pop s6
    pop s5
    pop s4
    pop s3
    pop s2
    pop s1
    pop s0
#Restore return address
    pop ra
    jr ra
# [end-epilogue_main]"""
    )

    prologue_sub = byron.f.macro(
        r"""
; [prologue_sub]
.globl	{_node}             ; -- Begin function {_node}
{_node}:
push ra
; [end-prologue_sub]""",
        _label='',  # No automatic creation of the label -- it's embedded as "{_node}:"
    )

    epilogue_sub = byron.f.macro(
        r"""; [epilogue_sub]
pull ra
jr ra
; [end-epilogue_sub]"""
    )

    riscv_isa = (
        RiscvIsaBuilder()
        .add_operation_set(RiscvIsaCustomOperationSet.BasicOp32)
        # .add_operation_set(RiscvIsaCustomOperationSet.BasicBranch)
        # .add_operation(RiscvOperation.PSEUDO_J)
        # .add_extension(RiscvIsaExtension.M)
        .add_register_set(RiscvRegisters.ZERO)
        .add_register_set(RiscvRegisters.TEMPORARIES)
        .add_register_set(RiscvRegisters.SAVED)
        .build()
    )
    op_pool = riscv_isa.get_operations_pool()
    op_pool_weight = riscv_isa.get_operations_pool_weight()
    assert len(op_pool) == len(op_pool_weight), "The size of the poll must be equal to the size of the weight"
    #
    # core_sub = byron.framework.bunch(op_pool, size=(1, 5 + 1), weights=op_pool_weight)
    # sub = byron.framework.sequence([prologue_sub, core_sub, epilogue_sub])
    # op_JL_imm = byron.f.macro("jal {label}", label=byron.f.global_reference(sub, creative_zeal=1, first_macro=True))
    # op_JL_reg = byron.f.macro("jalr {reg}")  # Maybe not feasible

    core_main = byron.framework.bunch(
        op_pool,  # + op_JL_imm, op_JL_reg
        size=(2, 4 + 1),
        weights=op_pool_weight,  # +1...
    )

    main = byron.framework.sequence([prologue_main, core_main, epilogue_main])

    return main
