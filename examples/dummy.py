#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging

import byron


def main():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase log verbosity (can be used multiple times)"
    )
    parser.add_argument(
        "-d", "--debug", action="store_const", dest="verbose", const=2, help="log debug messages (same as -vv)"
    )
    args = parser.parse_args()

    if args.verbose == 0:
        byron.logger.setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        byron.logger.setLevel(level=logging.INFO)
    elif args.verbose >= 2:
        byron.logger.setLevel(level=logging.DEBUG)

    byron.welcome(logging.INFO)
    main()
