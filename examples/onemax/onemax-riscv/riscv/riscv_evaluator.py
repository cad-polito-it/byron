__all__ = ['RiscvEvaluator']

from typing import Sequence, Callable
from .register_map import RegisterMap


class RiscvEvaluator:
    """RISCV evaluator, evaluate the stdout coming from a RISCV program execution with --trace-register enabled"""

    _wrote_keyword = "-wrote "
    _equals_keyword = " = "

    def __init__(
        self,
        covered_register: RegisterMap,
        evaluation_func: Callable[[Sequence[int]], Sequence[int] | int] | None = None,
    ):
        r"""
        Parameters
        ----------
        covered_register
            Register map of the register to evaluate
        evaluation_func
            Callable function to further evaluate the register content
        """
        self._covered_register = covered_register.register_map
        self._evaluation_func = evaluation_func if evaluation_func is not None else lambda s: s

    def evaluate_riscv_int_stdout(self, stdout: str):
        """Collect the last value present in the integer registers defined in the covered_register and evaluate they based on the
        evaluation function
        """
        written_registers = [
            line.split(RiscvEvaluator._wrote_keyword)[1]
            for line in stdout.split('\n')
            if RiscvEvaluator._wrote_keyword in line
        ]
        registers = [0 for i in range(len(self._covered_register))]
        for write in written_registers:
            parts = write.split(RiscvEvaluator._equals_keyword)
            if parts[0] not in self._covered_register:
                continue
            registers[self._covered_register[parts[0]]] = int(parts[1], 16)
        return self._evaluation_func(registers)

    def evaluate_riscv_float_stdout(self, stdout: str):
        """Collect the last value present in the floating registers defined in the covered_register and evaluate they based on the
        evaluation function
        """
        """TODO"""
        raise NotImplementedError
