import pytest
from byron.classes.value_bag import ValueBag

def test_valuebag_init():
    vb = ValueBag()
    assert isinstance(vb, ValueBag)

def test_valuebag_read_only():
    vb = ValueBag()
    with pytest.raises(NotImplementedError):
        vb['key'] = 'value'

    with pytest.raises(NotImplementedError):
        del vb['key']

def test_valuebag_missing():
    vb = ValueBag()
    assert vb.__missing__("$flag") is False
    assert vb.__missing__("normal_key") is None


def test_valuebag_safe_keys():
    vb = ValueBag({"safe_key": "value", "_private": "hidden"})
    assert "safe_key" in vb.keys()
    assert "_private" in vb.keys()  # Assuming underscore is allowed at the start based on SAFE_KEY regex


def test_valuebag_attr_access():
    vb = ValueBag({"safe_key": "value"})
    assert vb.safe_key == "value"

def test_valuebag_or_ior():
    vb1 = ValueBag({"key1": "value1"})
    vb2 = ValueBag({"key2": "value2"})
    vb3 = vb1 | vb2
    assert "key1" in vb3 and "key2" in vb3
    vb1 |= vb2
    assert "key2" in vb1


def test_valuebag_getattr_invalid():
    vb = ValueBag()
    assert vb.invalid_key is None  # Expect None for invalid keys


def test_valuebag_flag_keys():
    vb = ValueBag()  # Create an empty ValueBag
    assert vb["$missing_flag"] is False  # Flag keys should return False when missing


def test_valuebag_update_or():
    vb1 = ValueBag({"key1": "value1"})
    vb2 = {"key2": "value2"}
    vb1 |= vb2
    assert "key2" in vb1  # Ensure __ior__ works with regular dicts
#todo add __hash__(self) in the value_bag
def test_valuebag_hashable():
    vb = ValueBag({"key": "value"})
    assert isinstance(hash(vb), int), "ValueBag should be hashable"

def test_valuebag_repr():
    vb = ValueBag({"key": "value"})
    assert isinstance(repr(vb), str)  # Ensure __repr__ returns a string

def test_valuebag_iter():
    vb = ValueBag({"key1": "value1", "key2": "value2"})
    keys = [k for k in vb]  # Iterating over ValueBag
    assert "key1" in keys and "key2" in keys  # Check keys are in the iterator
