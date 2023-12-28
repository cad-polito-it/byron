import pytest
from byron.classes.parameter import ParameterStructuralABC, NodeReference
import networkx as nx


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

