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
    _register_sets = {
        Sets.temp_reg: RegisterSetParameters("t", 7),
        Sets.saved_reg: RegisterSetParameters("s", 12),
        Sets.argument_reg: RegisterSetParameters("a", 8)
    }

    def __init__(self, register_sets: Sequence[Sets]):
        self._register_map = dict()
        current_len = 0
        for r_set in register_sets:
            r_set_parameters = self._register_sets.get(r_set)
            self._register_map.update({f"{r_set_parameters.name}{i}": i + current_len for i in range(r_set_parameters.len)})
            current_len += r_set_parameters.len

    def __str__(self):
        return f"Register map: {str(self.register_map)}"

    def check_available_set(self, set_name: str):
        return set_name in self._register_sets

    @property
    def register_map(self):
        return self._register_map