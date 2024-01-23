# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron


def framework():
    byron.f.set_global_parameter('_comment', '//')
    byron.f.set_global_option('$dump_node_info', False)

    # The parameter '{_byron}' can be used to get information on the current system. Available fields are:
    # 'version', 'system', 'machine', 'python', and 'networkx'
    # To get all information use the macro 'byron.f.Info'

    int64 = byron.f.integer_parameter(0, 2**64)
    math_op = byron.f.choice_parameter(['+', '-', '*', '/', '&', '^', '|'])
    variable = byron.f.macro('var {_node} uint64', _label='')
    # variable.force_parent('prologue')

    # standard
    main_prologue = byron.f.macro('package main\nfunc evolved_function() uint64 {{')
    imath = byron.f.macro(
        '{var} {op}= {num}',
        var=byron.f.global_reference(variable, creative_zeal=1),
        op=math_op,
        num=int64,
    )
    vmath = byron.f.macro(
        '{var1} = {var2} {op} {var3}',
        var1=(byron.f.global_reference(variable, creative_zeal=1, first_macro=True)),
        op=math_op,
        var2=(byron.f.global_reference(variable)),
        var3=(byron.f.global_reference(variable)),
    )
    # NOTE[GX]: in macro definition "name='prologue'"" would be considered an (illegal) parameter
    main_epilogue = byron.f.macro('return {var}\n}}', var=byron.f.global_reference(variable))
    main_prologue.baptize('prologue')
    main_epilogue.baptize('epilogue')

    # proc
    subs_prologue = byron.f.macro('func {_node}(foo uint64) uint64 {{', _label='')
    subs_math = byron.f.macro('foo {op}= {num}', op=math_op, num=int64)
    subs_epilogue = byron.f.macro('return foo\n}}')
    subs = byron.f.sequence([subs_prologue, byron.f.bunch([subs_math], size=(2, 10)), subs_epilogue], name='function')

    call = byron.f.macro(
        '{var1} = {sub}({var2})',
        var1=byron.f.global_reference(variable),
        sub=byron.f.global_reference(subs, creative_zeal=1, first_macro=True),
        var2=byron.f.global_reference(variable),
    )

    few_default_vars = byron.f.bunch([variable], size=2)
    # NOTE[GX]: Force all newly created variables to appear after the few default ones
    variable.force_parent(few_default_vars)
    code = byron.f.bunch([imath, vmath, call], weights=(3, 3, 1), size=(2, 20), name='body')
    return byron.f.sequence((main_prologue, few_default_vars, code, main_epilogue), max_instances=1)
