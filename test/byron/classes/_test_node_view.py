#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest
import networkx as nx
import byron as byron


@pytest.fixture
def sample_graph():
    G = nx.MultiDiGraph()
    G.add_node(0, _macro="macro1")
    G.add_node(1, _macro="macro2")
    G.add_edge(0, 1, kind="framework")
    return G


def test_nodeview_properties(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    assert node_view.genome == sample_graph
    assert node_view.id == 0


def test_nodeview_attributes(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    assert dict(node_view.attributes) == {"_macro": "macro1"}


def test_nodeview_setattr(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    with pytest.raises(NotImplementedError):
        node_view.some_attribute = 10


def test_nodeview_getattr_unknown_property(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    with pytest.raises(KeyError):
        node_view.unknown_property


def test_nodeview_getattr_deprecated_property(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    with pytest.deprecated_call():
        _ = node_view.G


def test_nodeview_framework_tree(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    assert len(node_view.framework_tree.edges) == 1


def test_nodeview_predecessor(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 1)
    node_view = byron.classes.NodeView(ref)

    assert node_view.predecessor.id == 0


def test_nodeview_successors(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    assert len(node_view.successors) == 1
    assert node_view.successors[0].id == 1


def test_nodeview_links(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    assert len(node_view.links) == 0


def test_nodeview_name(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    assert node_view.name == "macro1"


def test_nodeview_path(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 1)
    node_view = byron.classes.NodeView(ref)

    assert node_view.path == (0, 1)


def test_nodeview_pathname(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 1)
    node_view = byron.classes.NodeView(ref)

    assert node_view.pathname == "n0.n1"


def test_nodeview_out_degree(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    assert node_view.out_degree == 1


def test_nodeview_in_degree(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 1)
    node_view = byron.classes.NodeView(ref)

    assert node_view.in_degree == 1


def test_nodeview_kind_out_degree(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 0)
    node_view = byron.classes.NodeView(ref)

    assert node_view.framework_out_degree == 1


def test_nodeview_kind_in_degree(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 1)
    node_view = byron.classes.NodeView(ref)

    assert node_view.framework_in_degree == 1


def test_nodeview_all_edges(sample_graph):
    ref = byron.classes.NodeReference(sample_graph, 1)
    node_view = byron.classes.NodeView(ref)

    assert len(node_view.all_edges) == 1
    assert node_view.all_edges[0] == (0, 1, "framework")
