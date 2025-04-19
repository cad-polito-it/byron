###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron

asm_instruction = byron.f.macro(
    "{inst} {reg}, 0x{imm:04x}",
    inst=byron.f.choice_parameter(["add", "sub", "and", "or", "xor"]),
    reg=byron.f.choice_parameter(["ax", "bx", "cx", "dx"]),
    imm=byron.f.integer_parameter(0, 2**16),
)

section_proc = byron.f.sequence(
    [byron.f.macro("proc {_node} near:"), byron.f.bunch(asm_instruction, 3), byron.f.macro("ret")], name="zap"
)

asm_call = byron.f.macro("call {target}", target=byron.f.global_reference("zap", creative_zeal=1))

byron.f.as_forest(asm_call)
