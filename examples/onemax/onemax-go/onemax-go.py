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

import logging
import platform
import argparse

import byron


def define_library():
    byron.f.set_parameter('_comment', '//')
    byron.f.set_option('$dump_node_info', False)

    # The parameter '{_byron}' can be used to get information on the current system. Available fields are:
    # 'version', 'system', 'machine', 'python', and 'networkx'
    # To get all information use the macro 'byron.f.Info'

    int64 = byron.f.integer_parameter(0, 2**64)
    variable = byron.f.macro('var {_node} uint64', _label='')
    variable.DEFAULT_PARENT = 'prologue'

    # standard
    main_prologue = byron.f.macro('package main\nfunc evolved_function() uint64 {{')
    main_prologue.ID = 'prologue'
    initialization = byron.f.macro(
        '{var} = uint64({num})', var=byron.f.global_reference(variable, creative_zeal=1.0), num=int64
    )
    imath = byron.f.macro(
        '{var} {op}= {num}',
        op=byron.f.choice_parameter(['+', '-', '*', '/', '&', '^', '|']),
        var=byron.f.global_reference(variable),
        num=int64,
    )
    vars = byron.f.bunch([initialization], size=5)
    code = byron.f.bunch([imath], size=10)
    main_epilogue = byron.f.macro('return {var}\n}}', var=byron.f.global_reference(variable))

    return byron.f.sequence((main_prologue, vars, code, main_epilogue))


def main():
    top_frame = define_library()

    evaluator = byron.evaluator.ScriptEvaluator('./evaluate-all.sh', filename_format="individual{i:06}.go")
    # evaluator = byron.evaluator.ParallelScriptEvaluator(
    #    'go', 'onemax.go', other_required_files=('main.go',), flags=('run',), timeout=5
    # )
    final_population = byron.ea.vanilla_ea(
        top_frame,
        evaluator,
        max_generation=0,
        max_fitness=byron.fitness.make_fitness(64.0),
        population_extra_parameters={'$dump_node_info': True},
    )

    for i, I in final_population:
        I.as_lgp(f'final-individual_{I.id}.png')
        with open(f'final-individual_{I.id}.go', 'w') as out:
            out.write(final_population.dump_individual(i))
        print(I.describe(max_recursion=None))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose', action='store_const', dest='verbose', const=2, help='use verbose logging (debug messages)'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_const', dest='verbose', const=0, help='be quiet (only log warning messages)'
    )
    args = parser.parse_args()

    if args.verbose == 0:
        byron.logger.setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        byron.logger.setLevel(level=logging.INFO)
    elif args.verbose == 2:
        byron.logger.setLevel(level=logging.DEBUG)

    main()
