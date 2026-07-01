###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0


import _byron as byron


def test_random_individual():
    """Check the reproducibility of an individual of 1,000 random integers between -1M and +1M"""

    m = byron.f.macro("{n}", n=byron.f.integer_parameter(-1_000_000, 1_000_000 + 1))
    bunch = byron.framework.bunch(m, size=1_000)
    population = byron.classes.Population(top_frame=bunch, evaluator=None)

    byron.rrandom.seed(42)
    population.add_random_individual()
    reference = population.dump_individual(0)

    population.add_random_individual()
    # Next individuals should be different
    assert reference != population.dump_individual(len(population.individuals) - 1)

    byron.rrandom.seed(None)
    population.add_random_individual()
    assert reference != population.dump_individual(len(population.individuals) - 1)

    byron.rrandom.seed(42)
    population.add_random_individual()
    assert reference == population.dump_individual(len(population.individuals) - 1)
