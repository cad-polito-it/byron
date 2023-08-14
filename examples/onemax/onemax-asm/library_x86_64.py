#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0


# NOTE: https://www.scivision.dev/windows-symbolic-link-permission-enable/

import byron

COMMENT = '#'


def define_frame():
    prologue = byron.f.macro(
        """
    .text
    .globl	one_max
one_max:
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
