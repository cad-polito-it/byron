import pytest
import networkx as nx
from byron.classes.node_view import NodeView
from byron.classes.node_reference import NodeReference
from byron.classes.node import Node
from byron.classes.selement import SElement
from byron.classes.parameter import ParameterABC
from byron.classes.value_bag import ValueBag
from typing import Any


class MockSElement(SElement):
    def dump(self, value_bag):
        return "MockDump" 
    
class MockParameter(ParameterABC):
    def __init__(self, value):
        super().__init__()
        self._value = value  

    def mutate(self, strength: float = 1.0) -> None:
        pass

    def is_correct(self, obj: Any) -> bool:
     
        return True
    

@pytest.fixture
def mock_graph():
    G = nx.MultiDiGraph()
    G.add_node(0, _type='Type', _selement=MockSElement(), param=MockParameter(42))
    G.add_node(1, _type='Type', _selement=MockSElement())
    G.add_edge(0, 1, _type='FRAMEWORK')
    return G

@pytest.fixture
def node_view_instance(mock_graph):
    return NodeView(NodeReference(mock_graph, Node(0)))


def test_node_view_initialization(mock_graph):
    nv = NodeView(NodeReference(mock_graph, Node(0)))
    assert isinstance(nv, NodeView)
    assert nv.node == 0


def test_graph_property(node_view_instance):
    assert isinstance(node_view_instance.graph, nx.MultiDiGraph)


def test_node_property(node_view_instance):
    assert node_view_instance.node == 0


def test_selement_property(node_view_instance):
    assert isinstance(node_view_instance.selement, MockSElement)


def test_type_property(node_view_instance):
    assert node_view_instance.type_ == MockSElement


def test_node_type_property(node_view_instance):
    assert node_view_instance.node_type == 'Type'

def test_path_string_property(node_view_instance):
    assert isinstance(node_view_instance.path_string, str)

def test_node_attributes_property(node_view_instance):
    attributes = node_view_instance.node_attributes
    assert isinstance(attributes, dict)
    assert '_type' in attributes
    assert '_selement' in attributes


def test_p_property(node_view_instance):
    p = node_view_instance.p
    assert isinstance(p, dict)
    assert 'param' in p
    assert p['param'] == 42


def test_tree_property(node_view_instance):
    tree = node_view_instance.tree
    assert isinstance(tree, nx.DiGraph)


def test_parent_property(node_view_instance):
    parent = node_view_instance.parent
    assert isinstance(parent, NodeView)
    assert parent.node == 0


def test_children_property(node_view_instance):
    children = node_view_instance.children
    assert isinstance(children, list)
    for child in children:
        assert isinstance(child, NodeView)


def test_path_property(node_view_instance):
    path = node_view_instance.path
    assert isinstance(path, tuple)
    for node in path:
        assert isinstance(node, NodeView)

def test_out_degree_property(node_view_instance):
    out_degree = node_view_instance.out_degree
    assert isinstance(out_degree, int)

def test_safe_dump(node_view_instance):
    dumped = node_view_instance.safe_dump
    assert isinstance(dumped, str)
    assert dumped == "MockDump"

def test_fields_property(node_view_instance):
    fields = node_view_instance.fields
    assert isinstance(fields, list)
    assert 'graph' in fields
    assert 'node' in fields

def test_make_static_method(mock_graph):
    nv = NodeView.make(mock_graph, 0)
    assert isinstance(nv, NodeView)
    assert nv.node == 0


if __name__ == "__main__":
    pytest.main()
