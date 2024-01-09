import pytest
from byron.classes.macro import Macro, ValueBag, NodeView

def test_macro_init():
    m = Macro()
    assert isinstance(m, Macro)

def test_macro_text():
    m = Macro()
    m.TEXT = "Sample text"
    assert m.text == "Sample text"

def test_macro_parameter_types():
    m = Macro()
    m.PARAMETERS = {"param1": int, "param2": str}
    assert m.parameter_types == {"param1": int, "param2": str}

def test_macro_dump():
    m = Macro()
    m.TEXT = "Hello, {name}"
    parameters = ValueBag({'name': 'World'})
    assert m.dump(parameters) == "Hello, World"

def test_macro_is_correct_valid():
    m = Macro()
    ref = object()
    nv = NodeView(ref)
    assert m.is_correct(nv) == True

def test_macro_shannon():
    m = Macro()
    assert isinstance(m.shannon, list)

def test_macro_is_name_valid_true():
    assert Macro.is_name_valid("valid_name123") == True

def test_macro_is_name_valid_false():
    assert Macro.is_name_valid("123Invalid") == False
