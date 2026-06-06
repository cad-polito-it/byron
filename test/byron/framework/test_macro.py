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

from unittest.mock import patch, MagicMock

import byron as byron

from byron.framework.macro import macro, _macro, _check_parameters

from byron.classes.parameter import ParameterABC

DummyParamClass = type('DummyParamClass', (ParameterABC,), {})


class TestMacro:

    # ==========================================
    # 1. Tests for _check_parameters
    # ==========================================
    def test_check_parameters(self):
        mock_node_view = MagicMock()
        
        valid_param = MagicMock()
        valid_param.value = 42
        valid_param.is_correct.return_value = True
        
        invalid_param = MagicMock()
        invalid_param.is_correct.return_value = False
        
        mock_node_view.node_attributes = {
            'v': valid_param,          
            '_hidden': invalid_param,  
            '%special': invalid_param  
        }
        
        assert _check_parameters(mock_node_view) is True
        valid_param.is_correct.assert_called_once_with(42)
        invalid_param.is_correct.assert_not_called() 
        
        mock_node_view.node_attributes['v2'] = invalid_param
        assert _check_parameters(mock_node_view) is False


    # ==========================================
    # 2. Tests for _macro (Class Builder)
    # ==========================================
    @patch('byron.classes.macro.Macro._patch_info')
    @patch('byron.classes.macro.Macro.add_node_check')
    def test_macro_builder(self, mock_add_check, mock_patch_info):
        
        M_text = _macro(text="Hello", macro_parameters=(), extra_parameters=())
        assert M_text.TEXT == "Hello"
        assert M_text.PARAMETERS == {}
        mock_patch_info.assert_called_with(name='Text#')
        
        M_user = _macro(
            text="Hello {v}", 
            macro_parameters=(('v', DummyParamClass),), 
            extra_parameters=(('_color', 'red'),)
        )
        assert M_user.PARAMETERS == {'v': DummyParamClass}
        assert M_user.EXTRA_PARAMETERS == {'_color': 'red'}
        mock_patch_info.assert_called_with(name='User#')
        
        mock_add_check.assert_called_with(_check_parameters)


    # ==========================================
    # 3. Tests for macro (Router)
    # ==========================================
    @patch('byron.classes.macro.Macro.is_name_valid', return_value=True)
    def test_macro_router(self, mock_is_name_valid): 
        
        M = macro(
            "Test {b} {a}",
            b=DummyParamClass,
            _extra2="foo",
            a=DummyParamClass,
            _extra1="bar"
        )
        
        assert list(M.PARAMETERS.keys()) == ['a', 'b']
        assert list(M.EXTRA_PARAMETERS.keys()) == ['_extra1', '_extra2']
        
        assert M.PARAMETERS['a'] == DummyParamClass
        assert M.EXTRA_PARAMETERS['_extra1'] == 'bar'

    @patch('byron.classes.macro.Macro.is_name_valid', return_value=False)
    def test_macro_invalid_name(self, mock_is_name_valid):
        with pytest.raises(AssertionError, match="invalid parameter name"):
            macro("Test {1invalid}", **{'1invalid': DummyParamClass})