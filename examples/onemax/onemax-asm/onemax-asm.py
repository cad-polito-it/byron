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

if platform.machine() == "arm64":
    import library_arm64 as library
else:
    raise NotImplementedError(f"Unknown machine type: {platform.machine()}")


SCRIPT_NAME = {"Linux": "./evaluate-all.sh", "Darwin": "./evaluate-all.sh", "Windows": "evaluate-all.cmd"}


def main():
    top_frame = library.define_frame()

    evaluator = byron.evaluator.ScriptEvaluator(SCRIPT_NAME[platform.system()], filename_format="individual{i:06}.s")
    # evaluator = byron.evaluator.MakefileEvaluator('onemax.s', required_files=['main.o'], timeout=5)
    final_population = byron.ea.vanilla_ea(
        top_frame,
        evaluator,
        max_generation=100,
        max_fitness=byron.fitness.make_fitness(64.0),
        population_extra_parameters={"_comment": library.COMMENT, '$dump_node_info': True},
    )

    for i, I in final_population:
        I.as_lgp(f'final-individual_{I.id}.png')
        with open(f'final-individual_{I.id}.s', 'w') as out:
            out.write(final_population.dump_individual(i))
        print(I.describe(max_recursion=None))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase log verbosity')
    parser.add_argument(
        '-d', '--debug', action='store_const', dest='verbose', const=2, help='log debug messages (same as -vv)'
    )
    args = parser.parse_args()

    if args.verbose == 0:
        byron.logger.setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        byron.logger.setLevel(level=logging.INFO)
    elif args.verbose == 2:
        byron.logger.setLevel(level=logging.DEBUG)

    main()
