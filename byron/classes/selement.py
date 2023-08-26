# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
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
# v1 / June 2023 / Squillero (GX)

__all__ = ['SElement', 'SElementMeta']

from typing import Callable, Sequence, Optional
from collections import defaultdict
import re
from uuid import uuid1 as generate_uuid

from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.user_messages import *


class SElementMeta(type):
    """Metaclass for all SElements. Allows comparisons with strings"""

    BYRON_CLASS_ID: str
    BYRON_CLASS_NAME: str
    BYRON_CLASS_TAGS: tuple[str]
    FORCED_PARENT: type | str | None

    _counters = defaultdict(int)

    def __new__(cls, name, *args, **kwargs):
        # new_cls = super(SElementMeta, cls).__new__(cls, name, *args, **kwargs)
        new_cls = super().__new__(cls, name, *args, **kwargs)
        new_cls.BYRON_CLASS_NAME = name
        new_cls.BYRON_CLASS_ID = f'⎨{name}${generate_uuid()}⎬'
        new_cls.BYRON_CLASS_TAGS = tuple()
        new_cls.FORCED_PARENT = None
        return new_cls

    def __eq__(self, other):
        # print(f"SElementMeta.__eq__:: self: {self} ({self!r}) =?= other: {other} ({other!r})")
        if isinstance(other, str):
            # other is a string, let's do the magic
            return self.BYRON_CLASS_ID == other
        elif not isinstance(other, type):
            # other is an object
            return False
        elif not issubclass(other, SElement):
            # other is a class, but not an SElement
            return False
        else:
            return self.BYRON_CLASS_ID == other.BYRON_CLASS_ID

    def __hash__(self):
        return hash(self.BYRON_CLASS_ID)

    def __repr__(self):
        return self.BYRON_CLASS_NAME

    def baptize(cls, name):
        cls._patch_info(custom_class_id=name)

    def _patch_info(
        cls,
        *,
        name: str | None = None,
        kind: str | None = None,
        tag: str | Sequence[str] = (),
        custom_class_id: str | None = None,
    ):
        from byron.classes.macro import Macro
        from byron.classes.frame import FrameABC
        from byron.classes.parameter import ParameterABC

        if custom_class_id:
            cls.BYRON_CLASS_ID = custom_class_id
            B = '❰❱'
            assert not name, f"{PARANOIA_VALUE_ERROR}: Cannot specify 'name' if 'custom_class_id'"
            name = custom_class_id
        else:
            B = '❬❭'

        if not name:
            name = cls.__name__
        if name[-1] == '#':
            SElementMeta._counters[name] += 1
            name += str(SElementMeta._counters[name])

        if issubclass(cls, Macro):
            if not kind:
                kind = 'Macro'
            if not tag:
                tag = FRAMEWORK
        elif issubclass(cls, FrameABC):
            if not kind:
                kind = 'Frame'
            if not tag:
                tag = FRAMEWORK
        elif issubclass(cls, ParameterABC):
            if not tag:
                tag = 'parameter'
            pass

        # kind
        if kind:
            cls.BYRON_CLASS_NAME = f'{kind}{B[0]}{name}{B[1]}'
        else:
            cls.BYRON_CLASS_NAME = name

        # tags
        if not tag:
            tag = ['byron']
        elif isinstance(tag, str):
            tag = ['byron', tag]
        else:
            tag = ['byron'] + list(tag)

        cls.BYRON_CLASS_TAGS = tuple(tag)

    def force_parent(cls, parent):
        cls.FORCED_PARENT = parent


class SElement(metaclass=SElementMeta):
    r"""Syntactic Element (SElement)

    SElement classe is the building block of the syntax of the individual, the common ancestor of both `macros` and
    `frames`. SElements can check the validity of nodes references. Node checks can be added dynamically to a
    `Pedantic` class via the @classmethod `add_node_check`.

    All checks, both value- and node- ones, can be later called from an instance with
    `object.is_valid(node_reference)`. If the class does not implement node checks, the parameter
    `node_reference` can be omitted or be explicitly ``None``.
    """

    # these are immutable to avoid any problem with aliasing
    NODE_CHECKS: tuple[Callable] = tuple()

    def __repr__(self):
        # BRACKETS: ⁅ ⁆ 〈 〉❬ ❭
        lst = list(self.__class__.BYRON_CLASS_TAGS)
        lst.append(repr(self.__class__))
        return f'''<{'.'.join(lst)} at {hex(id(self))}>'''

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return id()

    @classmethod
    def add_node_check(cls, function: Callable) -> None:
        cls.NODE_CHECKS = tuple([*cls.NODE_CHECKS, function])

    def is_valid(self, node: Optional['NodeReference'] = None) -> bool:
        r"""Checks the validity of a `NodeReference` and internal attributes"""
        return all(f(node) for f in self.__class__.NODE_CHECKS)

    def _is_valid_debug(self, node_ref: 'NodeReference') -> None:
        check_result = True
        for f in self.__class__.NODE_CHECKS:
            if not f(node_ref):
                logger.debug(f"is_valid: Failed check on {node_ref}: {f}")
                check_result = False
        return check_result

    @property
    def shannon(self) -> list[int]:
        raise NotImplementedError
