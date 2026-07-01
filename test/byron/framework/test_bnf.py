###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron as byron


def test_bnf():
    production = [[byron.f.SELF]]
    name = "test_bnf"
    frame = byron.f.bnf(production, name)
    assert str(frame) == 'Frame❰test_bnf❱'
    assert byron.tools.names.base_name(str(frame)) == name
