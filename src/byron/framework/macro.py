###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

__all__ = ["macro"]

from functools import cache
from typing import Any

from byron.classes.macro import Macro
from byron.classes.node_view import NodeView
from byron.classes.parameter import ParameterABC

# from byron.user_messages import *
from byron.user_messages import check_valid_type


@cache
def _macro(
    text: str, macro_parameters: tuple[tuple[str, type[ParameterABC]]], extra_parameters: tuple[tuple[str, Any]], safe_format: bool = False
) -> type[Macro]:
    class M(Macro):
        TEXT = text
        PARAMETERS = dict(macro_parameters)
        EXTRA_PARAMETERS = dict(extra_parameters) if extra_parameters else dict()
        SAFE_FORMAT = safe_format

        __slots__ = []  # Preventing the automatic creation of __dict__

    if not macro_parameters:
        M._patch_info(name='Text#')
    else:
        M._patch_info(name='User#')

    M.add_node_check(_check_parameters)

    return M


def macro(text: str, *, safe_format: bool = False, **parameters) -> type[Macro]:
    """Class factory: Returns the class for a specific macro.

    A macro is a fragment of text with variable elements, the `parameters`, appearing
    in curly brackets, eg. ``"My name is {surname}, {name} {surname}"``.

    Parameters are specified as keyword arguments.

    Note: The text and the parameters are eventually parsed by the ``str.format()``, thus
    the `Format Specification Mini-Language` `[1]`_ may be used.

    Parameters
    ----------
    text :
        the text of the macro in f-string format.
    safe_format :
        if True, use safe substitution that ignores unknown {placeholders} in the text.
        This is useful when the macro text contains literal braces (e.g., JSON content).
        Default is False (standard str.format() behavior).
    parameters :
        parameters used in the macro.

    Returns
    -------
    A macro.

    Examples
    --------
    Macro that displays the same 8-bit integer in decimal and hexadecimal formats

    >>> M = macro('Decimal {v} is {v:#x} in hexadecimal', v=integer_parameter(0, 256))
    >>> m = M()

    Macro with JSON content using safe_format to avoid KeyError on literal braces

    >>> M = macro('{"kind": "LITERAL", "value": {val}}', safe_format=True, val=integer_parameter(0, 100))

    References
    ----------
    .. [1] https://docs.python.org/3/library/string.html#formatspec
    """
    assert check_valid_type(text, str)
    macro_parameters = list()
    extra_parameters = list()
    for n, p in parameters.items():
        if n[0] != "_":
            assert Macro.is_name_valid(n), f"ValueError: invalid parameter name: {n!r}"
            assert check_valid_type(p, ParameterABC, subclass=True)
            macro_parameters.append((n, p))
        else:
            extra_parameters.append((n, p))

    return _macro(text, tuple(sorted(macro_parameters)), tuple(sorted(extra_parameters)), safe_format)


def _check_parameters(node_view: NodeView):
    # skip type and _selement because you don't need to check them
    return all(
        node_view.node_attributes[p].is_correct(node_view.node_attributes[p].value)
        for p in node_view.node_attributes
        if p[0] != '_' and p[0] != '%'
    )
