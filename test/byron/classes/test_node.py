# -*- coding: utf-8 -*-
##################################@|###|##################################@#
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0


import pytest
import networkx as nx
from byron.classes.node import Node, NODE_ZERO


def create_sample_graph():
    G = nx.MultiDiGraph()
    G.add_nodes_from([1, 2, 3])
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    return G


def test_node_initialization():
    node = Node()
    assert isinstance(node, Node)


def test_node_uniqueness():
    node1 = Node()
    node2 = Node()
    assert node1 != node2


def test_reset_labels():
    G = create_sample_graph()
    Node.reset_labels(G)
    for node in G.nodes:
        if node != NODE_ZERO:
            assert isinstance(node, Node)
            assert node != NODE_ZERO


def test_relabel_to_canonic_form():
    G = create_sample_graph()
    new_G = Node.relabel_to_canonic_form(G)
    for i, node in enumerate(new_G.nodes):
        assert node == Node(i + 1)  # Assuming Node(0) is reserved for NODE_ZERO


def test_node_creation():
    node1 = Node()
    node2 = Node()
    assert node1 != node2, "Nodes should have unique IDs"


def test_node_specific_id():
    specific_id = 5
    node = Node(specific_id)
    assert node == specific_id, "Node ID should match the specified ID"


def test_node_zero():
    assert NODE_ZERO == 0, "NODE_ZERO should be equal to 0"


def test_reset_labels():
    G = nx.MultiDiGraph()
    G.add_nodes_from([NODE_ZERO, 1, 2, 3])
    Node.reset_labels(G)
    for node in G.nodes:
        if node != NODE_ZERO:
            assert isinstance(node, Node), "All nodes except NODE_ZERO should be instances of Node"
        else:
            assert node == NODE_ZERO, "NODE_ZERO should remain unchanged"


def test_relabel_to_canonic_form():
    G = nx.MultiDiGraph()
    G.add_nodes_from([1, 2, 3])
    new_G = Node.relabel_to_canonic_form(G)
    expected_labels = [Node(i) for i in range(len(G.nodes))]
    assert sorted(new_G.nodes) == expected_labels, "Nodes should be relabeled to canonic form"


@pytest.fixture
def sample_graph():
    G = nx.MultiDiGraph()
    G.add_nodes_from([1, 2, 3])
    return G


def test_relabel_to_canonic_form_with_sample_graph(sample_graph):
    new_G = Node.relabel_to_canonic_form(sample_graph)
    for i, node in enumerate(new_G.nodes):
        # The nodes should be labeled starting from 0
        assert node == Node(i), f"Node should be labeled as Node({i})"
