#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
#   __                          (`/\                                        #
#  |  |--.--.--.----.-----.-----`=\/\   This file is part of byron v0.1     #
#  |  _  |  |  |   _|  _  |     |`=\/\  An evolutionary optimizer & fuzzer  #
#  |_____|___  |__| |_____|__|__| `=\/  https://github.com/squillero/byron  #
#        |_____|                     \                                      #
#############################################################################
# Copyright 2022-23 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from networkx.classes import MultiDiGraph
from byron.classes.node_reference import NodeReference


def test_node_reference():
    G = MultiDiGraph()
    p1 = NodeReference(G, 1)
    p2 = NodeReference(G, 2)
    assert p1 is not None
    assert type(p1.graph) == type(G)
    assert p1.node == 1
    assert p1 != p2
    assert p2.node != 3
    assert p1.graph == p2.graph
