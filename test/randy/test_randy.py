# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import random
import byron as byron

BATCH_SIZE = 4096


def test_reproducibility():
    seed = random.randint(0, 1_000_000)
    byron.rrandom.seed(seed)
    v1 = [byron.rrandom.random_float() for _ in range(BATCH_SIZE)]
    v2 = [byron.rrandom.random_float() for _ in range(BATCH_SIZE)]
    byron.rrandom.seed(seed)
    v3 = [byron.rrandom.random_float() for _ in range(BATCH_SIZE)]
    assert v1 == v3
    assert v2 != v3
    byron.rrandom.seed()
    v4 = [byron.rrandom.random_float() for _ in range(BATCH_SIZE)]
    assert v1 != v4

    seed = random.randint(0, 1_000_000)
    byron.rrandom.seed(seed)
    v1 = [byron.rrandom.random_int(0, 1_000_000) for _ in range(BATCH_SIZE)]
    v2 = [byron.rrandom.random_int(0, 1_000_000) for _ in range(BATCH_SIZE)]
    byron.rrandom.seed(seed)
    v3 = [byron.rrandom.random_int(0, 1_000_000) for _ in range(BATCH_SIZE)]
    assert v1 == v3
    assert v2 != v3
    byron.rrandom.seed()
    v4 = [byron.rrandom.random_int(0, 1_000_000) for _ in range(BATCH_SIZE)]
    assert v1 != v4


def test_independence():
    seed = random.randint(0, 1_000_000)
    byron.rrandom.seed(seed)
    v1 = [byron.rrandom.random_float() for _ in range(BATCH_SIZE)]
    byron.rrandom.seed(seed)
    v2_1 = [byron.rrandom.random_float() for _ in range(BATCH_SIZE // 2)]
    z = [random.random() for _ in range(BATCH_SIZE)]
    v2_2 = [byron.rrandom.random_float() for _ in range(BATCH_SIZE // 2)]
    assert v1 == v2_1 + v2_2


def test_randy_choice():
    seq = ['apple', 'banana', 'cherry']
    values = set()
    for _ in range(BATCH_SIZE):
        val = byron.rrandom.choice(seq)
        values |= {val}
        assert val in seq
    assert values == set(seq)

    alphabet = "ABCDEFGHIJKLMNOPQRTUVWXYZ"
    for _ in range(10):
        for i, c in enumerate(alphabet):
            val = byron.rrandom.choice(alphabet, loc=i, sigma=0)
            assert val == c
