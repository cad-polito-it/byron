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

from byron.framework.show_element import (
    as_text, 
    as_lgp, 
    as_forest, 
    estimate_size, 
    _generate_random_individual,
    Individual
)

from byron.classes.parameter import ParameterABC
from byron.classes.frame import FrameABC

DummyParam = type('DummyParam', (ParameterABC,), {})
DummySElement = type('DummySElement', (FrameABC,), {})


class TestShowElement:

    # ==========================================
    # 1. Tests for estimate_size
    # ==========================================
    @patch('byron.framework.show_element._generate_random_individual')
    def test_estimate_size_bytes(self, mock_gen, capsys):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.size = 500
        
        mock_gen.return_value = mock_ind
        
        estimate_size(DummySElement)
        
        captured = capsys.readouterr()
        assert "≈500B" in captured.out

    @patch('byron.framework.show_element._generate_random_individual')
    def test_estimate_size_kib(self, mock_gen, capsys):
        mock_ind = MagicMock(spec=Individual)
        mock_gen.return_value = mock_ind
        
        mock_ind.size = 2048  
        estimate_size(DummySElement)
        assert "≈2KiB" in capsys.readouterr().out
        
        mock_ind.size = 5242880  
        estimate_size(DummySElement)
        assert "≈5MiB" in capsys.readouterr().out


    # ==========================================
    # 2. Tests for Visualizers (as_lgp, as_forest)
    # ==========================================
    @patch('byron.framework.show_element.notebook_mode', False)
    def test_as_lgp_file_mode(self):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.as_lgp.return_value = "saved_to_file"
        
        result = as_lgp(mock_ind)
        
        mock_ind.as_lgp.assert_called_once_with('byron_lgp.svg')
        assert result == "saved_to_file"

    @patch('byron.framework.show_element.notebook_mode', True)
    def test_as_forest_notebook_mode(self):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.as_forest.return_value = "notebook_display"
        
        result = as_forest(mock_ind)
        
        mock_ind.as_forest.assert_called_once_with() 
        assert result == "notebook_display"


    # ==========================================
    # 3. Tests for as_text
    # ==========================================
    @patch('byron.framework.show_element.notebook_mode', False)
    @patch('byron.framework.show_element.DEFAULT_EXTRA_PARAMETERS', {})
    @patch('byron.framework.show_element.DEFAULT_OPTIONS', {})
    def test_as_text_with_individual(self):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.dump.return_value = "DUMP_TEXT"
        
        from byron.framework.show_element import NODE_ZERO
        mock_ind.genome.nodes = {NODE_ZERO: {}}
        
        result = as_text(mock_ind, node_info=True)
        
        mock_ind.dump.assert_called_once_with({'$dump_node_info': True})
        assert result == "DUMP_TEXT"

    @patch('byron.framework.show_element._generate_random_individual')
    @patch('byron.framework.show_element.macro')
    def test_as_text_with_parameter(self, mock_macro, mock_gen):
        mock_ind = MagicMock(spec=Individual)
        mock_ind.dump.return_value = "PARAM_DUMP"
        
        from byron.framework.show_element import NODE_ZERO
        mock_ind.genome.nodes = {NODE_ZERO: {}}
        mock_gen.return_value = mock_ind
        
        as_text(DummyParam)
        
        mock_macro.assert_called_once()
        mock_gen.assert_called_once()

    def test_as_text_invalid_type(self):
        with pytest.raises(NotImplementedError):
            as_text("InvalidString")


    # ==========================================
    # 4. Tests for _generate_random_individual
    # ==========================================
    @patch('byron.framework.show_element.rrandom')
    @patch('byron.framework.show_element.random_individual')
    def test_generate_random_individual(self, mock_random_ind, mock_rrandom):
        mock_rrandom.state = "OLD_STATE"
        
        mock_instance = MagicMock(spec=Individual)
        mock_random_ind.side_effect = [[], [mock_instance]]
        
        result = _generate_random_individual(DummySElement, seed=99)
        
        assert result == mock_instance
        mock_rrandom.seed.assert_called_once_with(99)
        assert mock_rrandom.state == "OLD_STATE"
        assert mock_random_ind.call_count == 2