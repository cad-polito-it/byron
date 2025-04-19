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
from typing import List

from .riscv_isa_operation_set_data import RiscvIsaOperationSetData, RiscvOperation


class RiscvIsaOperationSet(RiscvIsaOperationSetData, Enum):
    def __init__(self, set_name: str, operations: List[RiscvOperation]):
        self._set_name = set_name
        self._operations = operations

    @property
    def set_name(self):
        return self._set_name

    @property
    def operations(self):
        return self._operations
