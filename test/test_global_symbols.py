# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda

import byron


def test_framework():
    assert 'framework' == byron.FRAMEWORK


def test_link():
    assert 'link' == byron.LINK


def test_node_zero():
    assert 0 == byron.NODE_ZERO
