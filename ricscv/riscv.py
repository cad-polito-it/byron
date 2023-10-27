import subprocess
import tempfile
from typing import Sequence, Callable
from collections import namedtuple
import os
from register_map import RegisterMap


class Riscv:
    _wrote_keyword = "-wrote "
    _equals_keyword = " = "

    def __init__(self, covered_register: RegisterMap,
                 evaluation_func: Callable[[Sequence[int]], Sequence[int] | int] | None = None):
        self._covered_register = covered_register.register_map
        self.evaluation_func = evaluation_func if evaluation_func is not None else lambda s: s

    def evaluate_riscv_stdout(self, stdout: str):
        written_registers = [line.split(Riscv._wrote_keyword)[1] for line in stdout.split('\n') if
                             Riscv._wrote_keyword in line]
        registers = [0 for i in range(len(self._covered_register))]
        for write in written_registers:
            parts = write.split(Riscv._equals_keyword)
            if parts[0] not in self._covered_register:
                continue
            registers[self._covered_register[parts[0]]] = int(parts[1], 16)
        return self.evaluation_func(registers)


def sum_evaluator(register: Sequence[int]) -> int:
    return sum(register)


if __name__ == "__main__":
    res = """reg:      0x0100b0                       -wrote a0 = 0x1
reg:      0x0100b4                       -wrote a1 = 0x110b4
reg:      0x0100b8                       -wrote a1 = 0x110e0
reg:      0x0100bc                       -wrote a2 = 0xe
reg:      0x0100c0                       -wrote a7 = 0x40
Hello world!
reg:      0x0100c8                       -wrote a7 = 0x5d
reg:      0x0100cc                       -wrote a0 = 0"""
    reg_map = RegisterMap((RegisterMap.Sets.temp_reg, RegisterMap.Sets.argument_reg))
    print(reg_map)
    riscv = Riscv(reg_map)
    print(riscv.evaluate_riscv_stdout(res))
