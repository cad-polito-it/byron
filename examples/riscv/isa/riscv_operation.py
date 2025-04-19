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

from .riscv_operation_data import RiscvInstructionFormat, RiscvOperationData


class RiscvOperation(RiscvOperationData, Enum):
    ADDI = ("ADDI", RiscvInstructionFormat.I)
    SLTI = ("SLTI", RiscvInstructionFormat.I)
    SLTIU = ("SLTIU", RiscvInstructionFormat.I)
    ANDI = ("ANDI", RiscvInstructionFormat.I)
    ORI = ("ORI", RiscvInstructionFormat.I)
    XORI = ("XORI", RiscvInstructionFormat.I)

    SLLI = ("SLLI", RiscvInstructionFormat.I_5bit)
    SRLI = ("SRLI", RiscvInstructionFormat.I_5bit)
    SRAI = ("SRAI", RiscvInstructionFormat.I_5bit)

    LUI = ("LUI", RiscvInstructionFormat.U)
    AUIPC = ("AUIPC", RiscvInstructionFormat.U)

    ADD = ("ADD", RiscvInstructionFormat.R)
    SLT = ("SLT", RiscvInstructionFormat.R)
    SLTU = ("SLTU", RiscvInstructionFormat.R)
    AND = ("AND", RiscvInstructionFormat.R)
    OR = ("OR", RiscvInstructionFormat.R)
    XOR = ("XOR", RiscvInstructionFormat.R)
    SLL = ("SLL", RiscvInstructionFormat.R)
    SRL = ("SRL", RiscvInstructionFormat.R)
    SUB = ("SUB", RiscvInstructionFormat.R)
    SRA = ("SRA", RiscvInstructionFormat.R)

    # PSEUDO_NOP = ("NOP", RiscvInstructionFormat.PSEUDO_op)

    JAL = ("JAL", RiscvInstructionFormat.J)
    JALR = ("JALR", RiscvInstructionFormat.I)

    BEQ = ("BEQ", RiscvInstructionFormat.B)
    BNE = ("BNE", RiscvInstructionFormat.B)
    BLT = ("BLT", RiscvInstructionFormat.B)
    BLTU = ("BLTU", RiscvInstructionFormat.B)
    BGE = ("BGE", RiscvInstructionFormat.B)
    BGEU = ("BGEU", RiscvInstructionFormat.B)

    MUL = ("MUL", RiscvInstructionFormat.R)
    MULH = ("MULH", RiscvInstructionFormat.R)
    MULHU = ("MULHU", RiscvInstructionFormat.R)
    MULHSU = ("MULHSU", RiscvInstructionFormat.R)
    DIV = ("DIV", RiscvInstructionFormat.R)
    DIVU = ("DIVU", RiscvInstructionFormat.R)
    REM = ("REM", RiscvInstructionFormat.R)
    REMU = ("REMU", RiscvInstructionFormat.R)

    MULW = ("MULW", RiscvInstructionFormat.R)
    DIVW = ("DIVW", RiscvInstructionFormat.R)
    DIVUW = ("DIVUW", RiscvInstructionFormat.R)
    REMW = ("REMW", RiscvInstructionFormat.R)
    REMUW = ("REMUW", RiscvInstructionFormat.R)

    PSEUDO_J = ("J", RiscvInstructionFormat.PSEUDO_only_label_local)
    PSEUDO_JAL = ("JAL", RiscvInstructionFormat.PSEUDO_only_label_global)
    PSEUDO_JR = ("JR", RiscvInstructionFormat.PSEUDO_only_register)
    PSEUDO_JALR = ("JALR", RiscvInstructionFormat.PSEUDO_only_register)

    def __init__(self, op_name: str, op_format: RiscvInstructionFormat):
        self._op_name = op_name
        self._op_format = op_format

    @property
    def op_name(self):
        return self._op_name

    @property
    def op_format(self):
        return self._op_format
