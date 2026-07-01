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

from enum import Enum
from typing import Set

from .riscv_registers_data import RiscvRegistersData


class RiscvRegisters(RiscvRegistersData, Enum):
    ZERO = "zero"
    RETURN_ADDRESS = "ra"
    STACK_POINTER = "sp"
    GLOBAL_POINTER = "gp"
    THREAD_POINTER = "tp"
    TEMPORARIES = ("t", 7)
    SAVED = ("s", 12)
    ARGUMENTS = ("a", 8)

    def __init__(self, type: str, count=1):
        self._type = type
        self._count = count

    @property
    def register_set(self) -> Set[str]:
        if self._count == 1:
            return {self._type}
        else:
            return set(f"{self._type}{n}" for n in range(self._count))
