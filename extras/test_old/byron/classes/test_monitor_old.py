###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest

import byron as byron


@byron.classes.failure_rate
def always_succeeds():
    return True


@byron.classes.failure_rate
def always_fails():
    return False


def test_failure_rate():
    for _ in range(100):
        assert always_succeeds()

    with pytest.warns(RuntimeWarning):
        for _ in range(100):
            assert not always_fails()

    @byron.classes.failure_rate
    def raises_exception():
        raise ValueError("This is an exception")

    with pytest.raises(ValueError):
        raises_exception()
