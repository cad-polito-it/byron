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

import byron as byron

from unittest.mock import patch, MagicMock, PropertyMock

# ==============================================================================
# parameter_structural_local
# ==============================================================================
from byron.framework.parameter_structural_local import (
    _local_reference,
    local_reference,
    SE_DIRECTORY,
    ByronOperatorFailure 
)

# ==============================================================================
# patch
# ==============================================================================
TARGET_MODULE = 'byron.framework.parameter_structural_local'


class TestLocalReferenceFactory:

    def setup_method(self):
        _local_reference.cache_clear()

    # ==========================================
    # part1(Cache)
    # ==========================================
    def test_caching_and_directory_registration(self):
        cls1 = _local_reference(backward=True, self_loop=True, forward=True)
        cls2 = _local_reference(backward=True, self_loop=True, forward=True)
        
        assert cls1 is cls2
        assert cls1 in SE_DIRECTORY

    @patch(f'{TARGET_MODULE}.ParameterStructuralABC._patch_info')
    def test_class_naming_logic(self, mock_patch_info):
       
        _local_reference(backward=True, self_loop=False, forward=False)
        mock_patch_info.assert_called_with(name="LocalReference[<≠≯]")
        
        _local_reference.cache_clear()
        
        _local_reference(backward=True, self_loop=True, forward=True)
        mock_patch_info.assert_called_with(name="LocalReference[<=>]")

    def test_wrapper_function(self):
        cls = local_reference(backward=1, loop=0, forward=1)
        
        assert cls.BACKWARD is True
        assert cls.SELF_LOOP is False
        assert cls.FORWARD is True


    # ==========================================
    # part2
    # ==========================================
    @patch(f'{TARGET_MODULE}.get_siblings')
    def test_potential_targets_forward_only(self, mock_get_siblings):
        cls = _local_reference(backward=False, self_loop=False, forward=True)
        
        mock_self = MagicMock()
        mock_self._node_reference.node = "NODE_C"
        mock_get_siblings.return_value = ["NODE_A", "NODE_B", "NODE_C", "NODE_D", "NODE_E"]
        
        targets = cls.potential_targets.fget(mock_self)
        
        assert targets == ["NODE_D", "NODE_E"]
        mock_get_siblings.assert_called_once_with(mock_self._node_reference)

    @patch(f'{TARGET_MODULE}.get_siblings')
    def test_potential_targets_backward_and_self(self, mock_get_siblings):
        
        cls = _local_reference(backward=True, self_loop=True, forward=False)
        
        mock_self = MagicMock()
        mock_self._node_reference.node = "NODE_B"
        mock_get_siblings.return_value = ["NODE_A", "NODE_B", "NODE_C"]
        
        targets = cls.potential_targets.fget(mock_self)
        
        assert targets == ["NODE_A", "NODE_B"]


    # ==========================================
    # part3(Mutate)
    # ==========================================
    def test_mutate_unfastened_node(self):
        cls = _local_reference()
        
        mock_self = MagicMock()
        mock_self.is_fastened = False
        
        with pytest.raises(AssertionError, match="node is unfastened"):
            cls.mutate(mock_self)

    def test_mutate_empty_targets(self):
        cls = _local_reference()
        
        mock_self = MagicMock()
        mock_self.is_fastened = True
        mock_self.potential_targets = []
        
        with pytest.raises(ByronOperatorFailure):
            cls.mutate(mock_self)

    @patch(f'{TARGET_MODULE}.rrandom')
    def test_mutate_strength_one(self, mock_rrandom):
    
        cls = _local_reference()
        
        mock_self = MagicMock()
        mock_self.is_fastened = True
        mock_self.value = "OLD_NODE"
        
        targets_list = ["NODE_A", "NODE_B"]
        mock_self.potential_targets = targets_list
      
        mock_rrandom.choice.return_value = "NODE_B"
        
        cls.mutate(mock_self, strength=1.0)
       
        mock_rrandom.choice.assert_called_once_with(targets_list, None)
        assert mock_self.value == "NODE_B"

    @patch(f'{TARGET_MODULE}.rrandom')
    def test_mutate_custom_strength(self, mock_rrandom):
        cls = _local_reference()
        
        mock_self = MagicMock()
        mock_self.is_fastened = True
        mock_self.value = "NODE_B"
        
        targets_list = ["NODE_A", "NODE_B", "NODE_C"]
        mock_self.potential_targets = targets_list
        
        cls.mutate(mock_self, strength=0.5)
        
        mock_rrandom.choice.assert_called_once_with(targets_list, 1, strength=0.5)