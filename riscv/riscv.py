from typing import Sequence, Callable
from register_map import RegisterMap


class Riscv:
    _wrote_keyword = "-wrote "
    _equals_keyword = " = "

    def __init__(self, covered_register: RegisterMap,
                 evaluation_func: Callable[[Sequence[int]], Sequence[int] | int] | None = None):
        self._covered_register = covered_register.register_map
        self.evaluation_func = evaluation_func if evaluation_func is not None else lambda s: s

    def evaluate_riscv_int_stdout(self, stdout: str):
        written_registers = [line.split(Riscv._wrote_keyword)[1] for line in stdout.split('\n') if
                             Riscv._wrote_keyword in line]
        registers = [0 for i in range(len(self._covered_register))]
        for write in written_registers:
            parts = write.split(Riscv._equals_keyword)
            if parts[0] not in self._covered_register:
                continue
            registers[self._covered_register[parts[0]]] = int(parts[1], 16)
        return self.evaluation_func(registers)
