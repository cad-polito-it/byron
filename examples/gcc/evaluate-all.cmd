@echo off
rem   _____                          |   |
rem  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an
rem  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer.
rem  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"
rem        |_____|                    \|/
rem                                    '
rem Copyright 2023-25 Giovanni Squillero and Alberto Tonda
rem SPDX-License-Identifier: Apache-2.0

for %%x in (%*) do (
    copy "%%~x" onemax.s >NUL:
    make -s
)
