# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
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

__all__ = ["safe_dump"]

from collections import Counter
from byron.user_messages import logger

_name_counter = Counter()
_used_names = set()


def safe_dump(obj, **extra_parameters):
    extra = dict(extra_parameters)
    dumped = None
    while not dumped:
        try:
            dumped = obj.dump(**extra)
        except KeyError as k:
            if k.args[0] in extra:
                logger.error(f"dump: Can't safely dump {obj!r}")
                raise k
            extra[k.args[0]] = "{" + k.args[0] + "}"
        except Exception as e:
            logger.error(f"dump: Can't safely dump {obj!r}")
            raise e
    return dumped
