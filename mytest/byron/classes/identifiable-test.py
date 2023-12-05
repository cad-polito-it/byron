import pytest
from byron.classes.identifiable import IdentifiableABC

class MockIdentifiable(IdentifiableABC):
    def __init__(self, identity):
        self._id = identity

    @property
    def _identity(self):
        return self._id

# Test cases
def test_identifiable_hash():
    obj = MockIdentifiable('id123')
    assert hash(obj) == hash('id123')

def test_identifiable_equality():
    obj1 = MockIdentifiable('id123')
    obj2 = MockIdentifiable('id123')
    obj3 = MockIdentifiable('id456')
    assert obj1 == obj2
    assert obj1 != obj3

def test_identifiable_equality_with_different_class():
    obj1 = MockIdentifiable('id123')
    obj2 = 'id123'  # Different type
    assert obj1 != obj2

def test_identifiable_equality_with_none():
    obj1 = MockIdentifiable('id123')
    assert obj1 != None

