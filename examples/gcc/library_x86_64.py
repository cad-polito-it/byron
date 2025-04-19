###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0


# NOTE: https://www.scivision.dev/windows-symbolic-link-permission-enable/

import byron

COMMENT = '#'


def define_frame():
    prologue = byron.f.macro(
        """
    .text
    .globl	onemax
onemax:
    pushq	%rbp
    movq	%rsp, %rbp
        """
    )

    epilogue = byron.f.macro(
        """
	popq	%rbp
	ret
        """
    )

    op = byron.f.macro("	movl	${val:#x}, %eax", val=byron.f.integer_parameter(0, 2**32))

    core = byron.framework.bunch(op, size=(10, 50 + 1))
    return byron.framework.sequence([prologue, core, epilogue])
