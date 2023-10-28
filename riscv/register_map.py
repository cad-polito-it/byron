from __future__ import annotations
from collections import namedtuple
from enum import Enum
from typing import Sequence

"""
_register_map = {
        "zero": 0,
        "rs": 1,
        "sp": 2,
        "gp": 3,
        "tp": 4,
        "t0": 5,
        "t1": 6,
        "t2": 7,
        "s0": 8,
        "s1": 9,
        "a0": 10,
        "a1": 11,
        "a2": 12,
        "a3": 13,
        "a4": 14,
        "a5": 15,
        "a6": 16,
        "a7": 17,
        "s2": 18,
        "s3": 19,
        "s4": 20,
        "s5": 21,
        "s6": 22,
        "s7": 23,
        "s8": 24,
        "s9": 25,
        "s10": 26,
        "s11": 27,
        "t3": 28,
        "t4": 29,
        "t5": 30,
        "t6": 31,
    }
"""


class RegisterMap:
    class Sets(Enum):
        temp_reg = 1
        saved_reg = 2
        argument_reg = 3

    RegisterSetParameters = namedtuple("RegisterSetParameters", ["name", "len"])
    _register_sets_details = {
        Sets.temp_reg: RegisterSetParameters("t", 7),
        Sets.saved_reg: RegisterSetParameters("s", 12),
        Sets.argument_reg: RegisterSetParameters("a", 8)
    }

    _register_available = (
        "zero", "rs", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6")

    def __init__(self):
        self._register_map = dict()

    def __str__(self):
        return f"Register map: {str(self.register_map)}"

    def include_sets_of_registers(self, registers_sets: Sequence[Sets]):
        for r_set in registers_sets:
            r_set_parameters = self._register_sets_details.get(r_set)
            self._register_map.update(
                {f"{r_set_parameters.name}{i}": i + len(self._register_map) for i in range(r_set_parameters.len) if
                 f"{r_set_parameters.name}{i}" not in self._register_map})

    def include_registers(self, registers: Sequence[str]):
        for reg in registers:
            assert self.check_register_availability(reg), f"Register {reg} not available"
            if reg in self._register_map:
                continue
            self._register_map[reg] = len(self._register_map)

    def check_register_availability(self, reg):
        return reg in self._register_available

    @property
    def register_map(self):
        return self._register_map
