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

from .riscv_isa_operation_set import RiscvIsaOperationSet, RiscvOperation


class RiscvIsaExtension(RiscvIsaOperationSet):
    pass
    M = (
        "Extension for Integer Multiplication and Division",
        [
            RiscvOperation.MUL,
            RiscvOperation.MULH,
            RiscvOperation.MULHU,
            RiscvOperation.MULHSU,
            RiscvOperation.DIV,
            RiscvOperation.DIVU,
            RiscvOperation.REM,
            RiscvOperation.REMU,
        ],
    )
    M_64 = (
        M[0],
        [
            *M[1],
            *[
                RiscvOperation.MULW,
                RiscvOperation.DIVW,
                RiscvOperation.DIVUW,
                RiscvOperation.REMW,
                RiscvOperation.REMUW,
            ],
        ],
    )
    # A = ("", [])
    # F = ("", [])
    # D = ("", [])
