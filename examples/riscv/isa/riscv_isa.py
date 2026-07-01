###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Collection, Dict, Sequence

from byron.classes import FrameABC, Macro

from .riscv_instruction_format import RiscvInstructionFormat


class RiscvIsa:
    def __init__(self, operations: Dict[RiscvInstructionFormat, Collection[str]], registers: Collection[str]):
        assert len(registers) > 0, "No registers initialized"
        # self._registers = byron.f.choice_parameter(registers)
        self._registers = registers

        self._operations = {}
        for instruction_format, ops in operations.items():
            assert len(ops) > 0, f"{instruction_format} format defined with no instructions"
            # self._operations[instruction_format] = byron.f.choice_parameter(ops)
            self._operations[instruction_format] = ops

    def get_operations_from_format(
        self, instruction_format: RiscvInstructionFormat
    ) -> Collection[str]:  # type[ParameterABC]:
        assert instruction_format in self._operations, f"No {instruction_format} instructions initialized"
        return self._operations[instruction_format]

    @property
    def registers(self) -> Collection[str]:  # type[ParameterABC]:
        return self._registers

    def get_operations_pool(self, sub_bunch: type[FrameABC] | None = None) -> Sequence[type[Macro]]:
        out_sequence = []
        for instruction_format, ops in self._operations.items():
            out_sequence.append(instruction_format.create_operations_pool(ops, self.registers, sub_bunch))
        return out_sequence

    def get_operations_pool_weight(self) -> Sequence[int]:
        out_weight = []
        for instruction_format, ops in self._operations.items():
            # if instruction_format is instruction_format.B:
            #     out_weight.append(len(ops) * 4)
            # else:
            out_weight.append(len(ops))
        return out_weight
