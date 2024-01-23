# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################

# Copyright 2023 Giovanni Squillero and Alberto Tonda
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
# v1 / April 2023 / Squillero (GX)

__all__ = ["check_valid_type", "check_valid_types", "check_value_range", "check_valid_length", "check_no_duplicates"]

from numbers import Number
from collections.abc import Collection

from .messaging import logger
from .exception import *

PARANOIA_TYPE_ERROR = 'TypeError (paranoia check)'
PARANOIA_VALUE_ERROR = 'ValueError (paranoia check)'


def check_valid_type(obj, valid: type, subclass: bool = False) -> bool:
    """Checks if obj type is valid, croak on fail. Subclasses are not valid by default."""
    if not subclass and isinstance(obj, valid):
        return True
    elif subclass and isinstance(obj, type) and issubclass(obj, valid):
        return True
    if subclass and isinstance(obj, valid):
        hint = " — did you instantiate the object adding extra '()'?"
    elif not subclass and isinstance(obj, type) and issubclass(obj, valid):
        hint = " — did you forget to instantiate the object?"
    else:
        hint = ''
    logger.error(
        "TypeError: invalid type %s for %s: expected %s%s%s",
        type(obj),
        repr(obj),
        "sublass of " if subclass else "",
        valid,
        hint,
    )
    raise ByronError(PARANOIA_TYPE_ERROR)


def check_valid_types(obj, *valid_types: type, subclass: bool = False) -> bool:
    """Checks if obj type is valid."""
    for valid in valid_types:
        if not subclass and isinstance(obj, valid):
            return True
        elif subclass and isinstance(obj, type) and issubclass(obj, valid):
            return True
    logger.error(
        "TypeError: invalid type %s for %s: expected %s",
        type(obj),
        repr(obj),
        " or ".join(repr(v) for v in valid_types),
    )
    raise ByronError(PARANOIA_TYPE_ERROR)


def check_value_range(val: Number, min_: Number | None = None, max_: Number | None = None) -> bool:
    """Checks that `val` is in the half-open range [min_, max_)."""
    if min_ is not None and val < min_:
        logger.error("ValueError: %s < %s (min)", repr(val), repr(min_))
        raise ByronError(PARANOIA_VALUE_ERROR)
    if max_ is not None and val >= max_:
        logger.error("ValueError: %s >= %s (max)", repr(val), repr(max_))
        raise ByronError(PARANOIA_VALUE_ERROR)
    return True


def check_valid_length(obj: Collection, min_length: int | None = None, max_length: int | None = None) -> bool:
    """Checks that `len(obj)` is in the half-open range [min_, max_)."""
    if min_length is not None and len(obj) < min_length:
        logger.error("ValueError: incorrect length: len(%s) < %s", repr(obj), repr(min_length))
        raise ByronError(PARANOIA_VALUE_ERROR)
        return False
    if max_length is not None and len(obj) >= max_length:
        logger.error("ValueError: incorrect length: len(%s) >= %s", repr(obj), repr(max_length))
        raise ByronError(PARANOIA_VALUE_ERROR)
        return False
    return True


def check_no_duplicates(obj: Collection) -> bool:
    """Checks that `obj` does not contain duplicated elements."""
    seq = list(obj)
    if any(i != seq.index(x) for i, x in enumerate(seq)):
        dups = set(x for i, x in enumerate(seq) if i != seq.index(x))
        logger.error("ValueError: duplicated elements: %s", ", ".join(repr(_) for _ in sorted(dups)))
        raise ByronError(PARANOIA_VALUE_ERROR)
    return True
