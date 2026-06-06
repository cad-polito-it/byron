###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pytest

from unittest.mock import patch

import byron as byron

import byron.framework.utilities as utilities

from byron.framework.framework import cook_selement_list

from byron.classes.parameter import ParameterABC
from byron.classes.macro import Macro
from byron.classes.frame import FrameABC

class DummyParam(ParameterABC): 
    pass

class DummyMacro(Macro): 
    pass

class DummyFrame(FrameABC): 
    pass


class TestCookSElementList:

    @pytest.fixture(autouse=True)
    def mock_validators(self):
        with patch('byron.framework.framework.check_valid_type', return_value=True), \
             patch('byron.framework.framework.check_valid_types', return_value=True):
            yield

    @patch('byron.framework.utilities.macro')
    def test_string_conversion(self, mock_macro):
        mock_macro.return_value = "MockedStringClass"
        
        result = cook_selement_list(["hello_world"])
        
        mock_macro.assert_called_once_with("hello_world", _invalid_target=True)
        assert result == ["MockedStringClass"]

    @patch('byron.framework.utilities.macro')
    def test_parameter_conversion(self, mock_macro):
        
        mock_macro.return_value = "MockedParamClass"
        
        result = cook_selement_list([DummyParam])
        
        mock_macro.assert_called_once_with("{p}", p=DummyParam)
        assert result == ["MockedParamClass"]

    @patch('byron.framework.utilities.macro')
    def test_passthrough_elements(self, mock_macro):
        
        result = cook_selement_list([DummyMacro, DummyFrame])
        
        mock_macro.assert_not_called()
        assert result == [DummyMacro, DummyFrame]

    @patch('byron.framework.utilities.macro')
    def test_mixed_list(self, mock_macro):
      
        mock_macro.side_effect = ["CookedString", "CookedParam"]
        
        raw_list = ["text", DummyParam, DummyFrame]
        
        result = cook_selement_list(raw_list)
        
        assert mock_macro.call_count == 2
        
        assert result == ["CookedString", "CookedParam", DummyFrame]

