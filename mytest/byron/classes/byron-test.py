import pytest
from byron.classes.byron import Byron  # Corrected import statement

# def test_str_method():
#     byron = Byron()
#     expected_str = f'This is Byron v{Byron.__version__} "{Byron.__codename__}"'
#     assert str(byron) == expected_str, "The __str__ method does not return the expected string."

# def test_version():
#     byron = Byron()
#     expected_version = f'{Byron.__version__} "{Byron.__codename__}"'
#     assert byron.version == expected_version, "Version attribute does not match."

def test_networkx_version():
    byron = Byron()
    import networkx as nx
    expected_nx_version = f'{nx.__version__}'
    assert byron.nx == expected_nx_version, "NetworkX version attribute does not match."

def test_python_version():
    byron = Byron()
    import sys
    expected_python_version = f'{sys.version}'
    assert byron.python == expected_python_version, "Python version attribute does not match."

def test_system_version():
    byron = Byron()
    import platform
    expected_system_version = f'{platform.version()}'
    assert byron.system == expected_system_version, "System version attribute does not match."

def test_machine_info():
    byron = Byron()
    import platform
    import psutil
    desc = f'{platform.machine()} ({platform.processor()})'
    if psutil:
        desc += f'; {psutil.cpu_count(logical=False)} physical cores ({psutil.cpu_count(logical=True)} logical); {psutil.virtual_memory().total // 2 ** 20:,} MiB RAM'
    assert byron.machine == desc, "Machine information does not match."


# def test_getattr_invalid():
#     byron = Byron()
#     # Use a try-except block to assert a SyntaxError is raised
#     try:
#         _ = byron.invalid_attr
#         assert False, "SyntaxError was not raised for an invalid attribute"
#     except SyntaxError:
#         pass  # This is the expected outcome