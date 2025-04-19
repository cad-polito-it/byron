###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum
from typing import Callable, Collection

import byron
from byron.classes import FrameABC, Macro, ParameterABC, ParameterStructuralABC

from .riscv_instruction_format_data import RiscvInstructionFormatData


class RiscvInstructionFormat(RiscvInstructionFormatData, Enum):
    R = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, r2=registers, r3=registers
        ),
        "{op} {r1}, {r2}, {r3}",
        3,
    )
    I = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, r2=registers, imm=immediate
        ),
        "{op} {r1}, {r2}, {imm:#x}",
        2,
        11,  # Incoherence with the manual that say 12bits
    )
    I_5bit = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, r2=registers, imm=immediate
        ),
        "{op} {r1}, {r2}, {imm:#x}",
        2,
        5,
    )
    S = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, imm=immediate, r2=registers
        ),
        "{op} {r1}, {imm:#x}, {r2}",
        2,
        12,
    )
    B = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, r2=registers, label=label
        ),
        "{op} {r1}, {r2}, {label}",
        2,
        12,
        True,
    )
    U = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, r1=registers, imm=immediate
        ),
        "{op} {r1}, {imm:#x}",
        1,
        20,
    )
    J = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, r1=registers, op=operands, label=label
        ),
        "{op} {r1}, {label}",
        1,
        20,
        False,
    )
    PSEUDO_only_label_local = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, label=label
        ),
        "{op} {label}",
        0,
        20,
        True,
    )
    PSEUDO_only_label_global = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, op=operands, label=label
        ),
        "{op} {label}",
        0,
        20,
        False,
    )
    PSEUDO_only_register = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(
            representation, r1=registers, op=operands
        ),
        "{op} {r1}",
        1,
    )
    PSEUDO_op = (
        lambda representation, operands, registers, immediate, label: byron.f.macro(representation, op=operands),
        "{op}",
        0,
    )

    def __init__(
        self,
        macro_lambda: Callable[
            [
                str,
                type[ParameterABC],
                type[ParameterABC] | None,
                type[ParameterABC] | None,
                type[ParameterStructuralABC] | None,
            ],
            type[Macro],
        ],
        representation: str,
        register_count: int,
        immediate_len: None | int = None,
        is_local_reference: None | bool = None,
    ):
        self._macro_lambda = macro_lambda
        self._representation = representation
        self._register_count = register_count
        self._immediate_len = immediate_len
        self._is_local_reference = is_local_reference

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == self.name

    def __str__(self):
        return f"{self.name}-type"

    def create_operations_pool(
        self,
        operands: Collection[str],
        registers: Collection[str] | None = None,
        sub_bunch: type[FrameABC] | None = None,
    ) -> type[Macro]:
        return self._macro_lambda(
            self._representation,
            byron.f.choice_parameter(operands),
            byron.f.choice_parameter(registers) if registers is not None else None,
            byron.f.integer_parameter(0, 2**self._immediate_len) if self._immediate_len is not None else None,
            None
            if self._is_local_reference is None
            else byron.f.local_reference(backward=True, loop=False, forward=True)
            if self._is_local_reference is True
            else byron.f.global_reference(sub_bunch, creative_zeal=1, first_macro=True),
        )
