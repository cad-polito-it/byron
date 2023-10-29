from __future__ import annotations

__all__ = ['RegisterMap']

from collections import namedtuple
from enum import Enum
from typing import Sequence


class RegisterMap:
    """Register map of selected number of register for RISCV

    The class allow an easy way to convert a subset of the RISCV registers names into a map {register_name: id}
    where id is a monotonically increasing integer (starting from 0)
    """

    class Sets(Enum):
        """Enum of the various subsets of the RISCV registers"""

        temp_reg = 1
        saved_reg = 2
        argument_reg = 3

    RegisterSetParameters = namedtuple("RegisterSetParameters", ["name", "len"])
    _register_sets_details = {
        Sets.temp_reg: RegisterSetParameters("t", 7),
        Sets.saved_reg: RegisterSetParameters("s", 12),
        Sets.argument_reg: RegisterSetParameters("a", 8),
    }

    _register_available = (
        "zero",
        "rs",
        "sp",
        "gp",
        "tp",
        "t0",
        "t1",
        "t2",
        "s0",
        "s1",
        "a0",
        "a1",
        "a2",
        "a3",
        "a4",
        "a5",
        "a6",
        "a7",
        "s2",
        "s3",
        "s4",
        "s5",
        "s6",
        "s7",
        "s8",
        "s9",
        "s10",
        "s11",
        "t3",
        "t4",
        "t5",
        "t6",
    )

    def __init__(self):
        self._register_map = dict()

    def __str__(self):
        return f"Register map: {str(self.register_map)}"

    def include_sets_of_registers(self, registers_sets: Sequence[Sets]):
        """Include one or more subsets of RISCV register in the map"""
        for r_set in registers_sets:
            r_set_parameters = self._register_sets_details.get(r_set)
            self._register_map.update(
                {
                    f"{r_set_parameters.name}{i}": i + len(self._register_map)
                    for i in range(r_set_parameters.len)
                    if f"{r_set_parameters.name}{i}" not in self._register_map
                }
            )

    def include_registers(self, registers: Sequence[str]):
        """Include one or more RISCV register name in the map"""
        for reg in registers:
            assert self.check_register_availability(reg), f"Register {reg} not available"
            if reg in self._register_map:
                continue
            self._register_map[reg] = len(self._register_map)

    def check_register_availability(self, reg):
        """Check if the register name is a correct RISCV register"""
        return reg in self._register_available

    @property
    def register_map(self):
        """Get the register map"""
        return self._register_map
