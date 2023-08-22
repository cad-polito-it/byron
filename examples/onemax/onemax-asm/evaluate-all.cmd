@echo off
rem    __                          (`/\
rem   |  |--.--.--.----.-----.-----`=\/\   This file is part of Byron v0.8
rem   |  _  |  |  |   _|  _  |     |`=\/\  An evolutionary optimizer & fuzzer
rem   |_____|___  |__| |_____|__|__| `=\/  https://github.com/cad-polito-it/byron
rem         |_____|                     \
rem
rem Copyright 2023 Giovanni Squillero and Alberto Tonda
rem SPDX-License-Identifier: Apache-2.0

for %%x in (%*) do (
    copy "%%~x" onemax.s >NUL:
    make -s
)
