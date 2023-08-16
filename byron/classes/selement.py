# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
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

from typing import Optional, Callable, Any, Sequence
from uuid import uuid1 as generate_uuid

from byron.user_messages import *
from byron.tools.names import canonize_name, uncanonize_name


class SElementMeta(type):
    """Metaclass for all SElements. Allows comparisons with strings"""

    def __new__(cls, name, *args, **kwargs):
        new_cls = super(SElementMeta, cls).__new__(cls, name, *args, **kwargs)
        new_cls.ID = f'{name}${generate_uuid()}'
        new_cls.FORCED_PARENT = None
        return new_cls

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, other):
        if isinstance(other, str):
            # other is a string, let's do the magic
            return self.ID == other
        elif not isinstance(other, type):
            # other is an object
            return False
        elif not issubclass(other, SElement):
            # other is a class, but not a SElement
            return False
        else:
            return self.ID == other.ID

    @property
    def forced_parent(cls):
        return cls.FORCED_PARENT

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

    @classmethod
    def add_node_check(cls, function: Callable) -> None:
        cls.NODE_CHECKS = tuple([*cls.NODE_CHECKS, function])

    def is_valid(self, node: Optional["NodeReference"] = None) -> bool:
        r"""Checks the validity of a `NodeReference` and internal attributes"""
        return all(f(node) for f in self.__class__.NODE_CHECKS)

    def _is_valid_debug(self, node: "NodeReference") -> None:
        check_result = True
        for f in self.__class__.NODE_CHECKS:
            if not f(node):
                logger.info(f"NodeChecks: Failed check on genome 0x{id(node.genome):x}: {f.__qualname__}({node})")
                check_result = False
        return check_result
