###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0


class TestObject:
    def __init__(self, key_to_raise=None):
        self.key_to_raise = key_to_raise

    def dump(self, **kwargs):
        if self.key_to_raise and self.key_to_raise not in kwargs:
            raise KeyError(self.key_to_raise)
        else:
            return f"success: {kwargs.get(self.key_to_raise, '')}"


class TestObjectException(Exception):
    pass


class TestObjectWithException:
    def __init__(self, exception):
        self.exception = exception

    def dump(self, **kwargs):
        raise self.exception
