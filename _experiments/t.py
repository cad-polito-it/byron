###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron

reg8 = byron.f.choice_parameter(['ah', 'bh', 'ch', 'dh', 'al', 'bl', 'cl', 'dl'])
reg16 = byron.f.choice_parameter(['ax', 'bx', 'cx', 'dx'])
int8 = byron.f.integer_parameter(0, 2**8)
int16 = byron.f.integer_parameter(0, 2**16)

opcodes2 = byron.f.choice_parameter(['mov', 'add', 'sub', 'or', 'and'])
opcodes1 = byron.f.choice_parameter(['not', 'neg', 'inc', 'dec'])
opcodes0 = byron.f.choice_parameter(['nop', 'hlt'])

inst8rr = byron.f.macro("{op} {r1}, {r2}", op=opcodes2, r1=reg8, r2=reg8)
inst8ri = byron.f.macro("{op} {r}, {i:#x}", op=opcodes2, r=reg8, i=int8)
inst8r = byron.f.macro("{op} {r}", op=opcodes1, r=reg8)
inst16rr = byron.f.macro("{op} {r1}, {r2}", op=opcodes2, r1=reg16, r2=reg16)
inst16ri = byron.f.macro("{op} {r}, {i:#x}", op=opcodes2, r=reg16, i=int16)
inst16r = byron.f.macro("{op} {r}", op=opcodes1, r=reg16)

tests = byron.f.choice_parameter(['jz', 'jnz', 'jc', 'jnc', 'jo', 'jno', 'js', 'jns'])
branch = byron.f.macro("{test} {label}", test=tests, label=byron.f.local_reference())

main_prologue = "section .text\nglobal _start\n_start:"
init = byron.f.macro("mov ax, {v:#x}\nmov bx, {v:#x}\nmov cx, {v:#x}\nmov dx, {v:#x}", v=int16)

sub_entry = byron.f.macro("\nproc {_node} near", _label='')
sub_exit = byron.f.macro("ret")
sub_body = byron.f.bunch([inst16rr, inst16ri, inst16r, inst8rr, inst8ri, inst8r], (2, 10))
sub = byron.f.sequence([sub_entry, sub_body, sub_exit])

call = byron.f.macro("call {proc}", proc=byron.f.global_reference(sub, first_macro=True, creative_zeal=1))

main_body = byron.f.bunch([inst16rr, inst16ri, inst16r, inst8rr, inst8ri, inst8r, branch, call], size=(5, 20))
full_prog = byron.f.sequence([main_prologue, init, main_body])


@byron.fitness_function
def fitness(genotype):
    # print(genotype)
    return genotype.count('proc'), len(genotype)
    # raise Exception("Not implemented")


evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
population = byron.ea.vanilla_ea(full_prog, evaluator, max_generation=1_000, lambda_=20, mu=30)

print(population[0].dump())
