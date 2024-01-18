#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0



import pytest
from byron.classes.parameter import ParameterStructuralABC, NodeReference,ParameterABC
import networkx as nx
from typing import Any  

class ConcreteParameter(ParameterABC):
    def __init__(self):
        super().__init__()  
        self._value = 0     

    def mutate(self, strength: float = 1.0) -> None:
        self._value += strength

    def is_correct(self, obj: Any) -> bool:
        return isinstance(obj, (int, float))  



@pytest.fixture
def simple_graph():
    G = nx.MultiDiGraph()
    G.add_node(1)
    G.add_node(2)
    return G

@pytest.fixture
def node_reference(simple_graph):
    return NodeReference(simple_graph, 1)

class TestParameterStructuralABC:

    def test_init(self):
        param = ParameterStructuralABC()
        assert param._node_reference is None

    def test_fasten(self, node_reference):
        param = ParameterStructuralABC()
        param.fasten(node_reference)
        assert param._node_reference == node_reference

    def test_unfasten(self, node_reference):
        param = ParameterStructuralABC()
        param.fasten(node_reference)
        param.unfasten()
        assert param._node_reference is None

    def test_is_fastened(self, node_reference):
        param = ParameterStructuralABC()
        assert not param.is_fastened
        param.fasten(node_reference)
        assert param.is_fastened

    def test_value_getter_fastened(self, node_reference, simple_graph):
        param = ParameterStructuralABC()
        param.fasten(node_reference)
        simple_graph.add_edge(1, 2, key=param.key, _type='LINK')
        assert param.value == 2

    def test_value_getter_unfastened(self):
        param = ParameterStructuralABC()
        with pytest.raises(AssertionError):
            _ = param.value

    def test_value_setter(self, node_reference, simple_graph):
        param = ParameterStructuralABC()
        param.fasten(node_reference)
        param.value = 2
        assert param.value == 2
        assert (1, 2, param.key) in simple_graph.edges(keys=True)


def test_ParameterABC():
    parameter_abc = ConcreteParameter()
    parameter_abc.value = 5

    assert parameter_abc.key is not None  
    assert parameter_abc.value == 5  

    parameter_abc2 = ConcreteParameter()
    parameter_abc2.value = 5

    assert parameter_abc != parameter_abc2

    assert isinstance(parameter_abc, ConcreteParameter) and parameter_abc.value == parameter_abc2.value
