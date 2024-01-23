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

#############################################################################
# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

__all__ = ["Paranoid"]


class Paranoid:
    """Abstract class: Paranoid classes do implement `run_paranoia_checks()`."""

    def run_paranoia_checks(self) -> bool:
        """Check the internal consistency of a "paranoid" object.

        The function should be overridden by the sub-classes to implement the
        required, specific checks. It always returns `True`, but throws an
        exception whenever an inconsistency is detected.

        **Notez bien**: Sanity checks may be computationally intensive,
        paranoia checks are not supposed to be used in production environments
        (ie. when `-O` is used for compiling). Their typical usage is:
        `assert foo.run_paranoia_checks()`

        Returns:
            True (always)

        Raise:
            AssertionError if some internal data structure is incoherent
        """
        return True
