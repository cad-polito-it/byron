#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.1    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import logging
import time

import byron

from tqdm.auto import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    byron.logger.debug(
        "[bold]B[/] [blue]blue[/] [blue bold]boldblue[/] Normal [bold red blink]Server is shutting down![/]",
    )

    exit()
    with logging_redirect_tqdm([byron.logger]):
        for i in tqdm(range(100)):
            time.sleep(0.1)
            if False and i > 0 and i % 7 == 0:
                byron.logger.info(f"console logging redirected to `tqdm.write({i})`")
