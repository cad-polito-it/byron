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
import importlib
from unittest.mock import patch, MagicMock

import byron as byron

se_module = importlib.import_module("byron.framework.show_element-unknown")

as_text = se_module.as_text
as_lgp = se_module.as_lgp
as_forest = se_module.as_forest
_generate_random_individual = se_module._generate_random_individual
Individual = se_module.Individual
NODE_ZERO = se_module.NODE_ZERO

from byron.classes.parameter import ParameterABC
from byron.classes.frame import FrameABC

class DummyParam(ParameterABC): 
    pass

class DummySElement(FrameABC): 
    pass

PATCH_TARGET = 'byron.framework.show_element-unknown'

class TestShowElementUnknown:

    # ==========================================
    # 1. Tests for Visualizers (as_lgp)
    # ==========================================
    @patch(f'{PATCH_TARGET}.notebook_mode', False)
    def test_as_lgp_file_mode(self):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.as_lgp.return_value = "saved_to_lgp_file"
        
        result = as_lgp(mock_ind)
        
        mock_ind.as_lgp.assert_called_once_with('byron_lgp.svg')
        assert result == "saved_to_lgp_file"

    @patch(f'{PATCH_TARGET}.notebook_mode', True)
    def test_as_lgp_notebook_mode(self):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.as_lgp.return_value = "notebook_lgp_display"
        
        result = as_lgp(mock_ind)
        
        mock_ind.as_lgp.assert_called_once_with() 
        assert result == "notebook_lgp_display"


    # ==========================================
    # 2. Tests for Visualizers (as_forest)
    # ==========================================
    @patch(f'{PATCH_TARGET}.notebook_mode', False)
    def test_as_forest_file_mode(self):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.as_forest.return_value = "saved_to_forest_file"
        
        result = as_forest(mock_ind)
        
        mock_ind.as_forest.assert_called_once_with('byron_forest.svg')
        assert result == "saved_to_forest_file"

    @patch(f'{PATCH_TARGET}.notebook_mode', True)
    def test_as_forest_notebook_mode(self):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.as_forest.return_value = "notebook_forest_display"
        
        result = as_forest(mock_ind)
        
        mock_ind.as_forest.assert_called_once_with() 
        assert result == "notebook_forest_display"


    # ==========================================
    # 3. Tests for as_text
    # ==========================================
    @patch(f'{PATCH_TARGET}.notebook_mode', False)
    @patch(f'{PATCH_TARGET}.DEFAULT_EXTRA_PARAMETERS', {'default': 1})
    @patch(f'{PATCH_TARGET}.DEFAULT_OPTIONS', {'opt': 2})
    def test_as_text_with_individual(self):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.dump.return_value = "DUMP_TEXT"
        mock_ind.genome.nodes = {NODE_ZERO: {}}
        
        result = as_text(mock_ind, node_info=True, extra_parameters={'extra': 3})
        
        expected_params = {'default': 1, 'opt': 2, 'extra': 3, '$dump_node_info': True}
        mock_ind.dump.assert_called_once_with(expected_params)
        assert result == "DUMP_TEXT"

    @patch(f'{PATCH_TARGET}.notebook_mode', True)
    @patch('builtins.print')
    def test_as_text_notebook_mode(self, mock_print):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.dump.return_value = "NOTEBOOK_DUMP"
        mock_ind.genome.nodes = {NODE_ZERO: {}}
        
        result = as_text(mock_ind)
        
        mock_print.assert_called_once_with("NOTEBOOK_DUMP")
        assert result is None  

    @patch(f'{PATCH_TARGET}._generate_random_individual')
    @patch(f'{PATCH_TARGET}.macro')
    def test_as_text_with_parameter(self, mock_macro, mock_gen):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.genome.nodes = {NODE_ZERO: {}}
        mock_gen.return_value = mock_ind
        
        as_text(DummyParam)
        
        mock_macro.assert_called_once()
        mock_gen.assert_called_once()

    def test_as_text_invalid_type(self):
        with pytest.raises(NotImplementedError):
            as_text("InvalidStringValue")


    # ==========================================
    # 4. Tests for _generate_random_individual
    # ==========================================
    @patch(f'{PATCH_TARGET}.rrandom')
    @patch(f'{PATCH_TARGET}.random_individual')
    def test_generate_random_individual(self, mock_random_ind, mock_rrandom):
        mock_rrandom.state = "SAVED_STATE"
        mock_instance = MagicMock(spec=Individual)
        mock_random_ind.side_effect = [[], [mock_instance]]
        
        result = _generate_random_individual(DummySElement, seed=123)
        
        assert result == mock_instance
        mock_rrandom.seed.assert_called_once_with(123)
        assert mock_rrandom.state == "SAVED_STATE"
        assert mock_random_ind.call_count == 2