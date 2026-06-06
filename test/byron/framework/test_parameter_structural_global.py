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
import networkx as nx
from unittest.mock import patch, MagicMock

# ==============================================================================
# ایمپورت‌های کاملاً استاندارد از فایل parameter_structural_global
# ==============================================================================
from byron.framework.parameter_structural_global import (
    _global_reference,
    global_reference,
    ByronOperatorFailure,
    MACRO,
    NODE_ZERO
)

TARGET_MODULE = 'byron.framework.parameter_structural_global'


class TestGlobalReferenceFactory:

    def setup_method(self):
        _global_reference.cache_clear()

    # ==========================================
    # part1
    # ==========================================
    @patch(f'{TARGET_MODULE}.ParameterStructuralABC._patch_info')
    def test_class_naming_and_caching(self, mock_patch_info):
        cls1 = _global_reference(target_frame="MyMacro", first_macro=True, creative_zeal=0)
        mock_patch_info.assert_called_with(name="GlobalReference['MyMacro']")
        
        class DummyMacro: pass
        cls2 = _global_reference(target_frame=DummyMacro, first_macro=True, creative_zeal=0)
        mock_patch_info.assert_called_with(name=f"GlobalReference[{DummyMacro}]")
        
        cls3 = _global_reference(target_frame="MyMacro", first_macro=True, creative_zeal=0)
        assert cls1 is cls3

    def test_wrapper_function_validation(self):
        global_reference("Target", creative_zeal=1)
        global_reference("Target", creative_zeal=0.5)
        
        with pytest.raises(AssertionError, match="creative zeal is integer or"):
            global_reference("Target", creative_zeal=1.5)


    # ==========================================
    # part2
    # ==========================================
    @patch(f'{TARGET_MODULE}.provide_tags')
    def test_get_potential_targets_filtering(self, mock_provide_tags):
        cls = _global_reference(target_frame="TargetMacro", first_macro=False)
        mock_self = MagicMock()
        
        G = nx.DiGraph()
        
        selement_mock_1 = MagicMock()
        selement_mock_1.EXTRA_PARAMETERS = {}
        G.add_node(1, _type=MACRO, _typepath=["Root", "TargetMacro"], _selement=selement_mock_1)
        
        G.add_node(2, _type="NOT_MACRO", _typepath=["TargetMacro"])
        
        selement_mock_3 = MagicMock()
        selement_mock_3.EXTRA_PARAMETERS = {'_invalid_target': True}
        G.add_node(3, _type=MACRO, _typepath=["TargetMacro"], _selement=selement_mock_3)
        
        mock_self._node_reference.graph = G
        
        T = nx.DiGraph()
        T.add_nodes_from([1, 2, 3])
        
        targets = cls.get_potential_targets(mock_self, T)
        
        assert targets == [1]


    # ==========================================
    #part3 (Mutate) 
    # ==========================================
    @patch(f'{TARGET_MODULE}.get_structure')
    @patch(f'{TARGET_MODULE}.provide_tags')
    @patch(f'{TARGET_MODULE}.rrandom')
    def test_mutate_standard_choice(self, mock_rrandom, mock_provide, mock_get_structure):
        cls = _global_reference(creative_zeal=0)
        mock_self = MagicMock()
        mock_self.is_fastened = True
        mock_self.value = 1  
        
     
        mock_self._node_reference.graph = nx.DiGraph() 
        mock_self._node_reference.graph.add_node(NODE_ZERO, _typepath=[])
        
        mock_self.get_potential_targets.return_value = [1, 2, 3]
        mock_rrandom.choice.return_value = 2
        
        cls.mutate(mock_self)
        
        mock_rrandom.choice.assert_called_with([2, 3])
        assert mock_self.value == 2

    @patch(f'{TARGET_MODULE}.get_structure')
    @patch(f'{TARGET_MODULE}.provide_tags')
    @patch(f'{TARGET_MODULE}.unroll_selement')
    @patch(f'{TARGET_MODULE}.initialize_subtree')
    def test_mutate_create_new_target(self, mock_init, mock_unroll, mock_provide, mock_get_structure):
        cls = _global_reference(creative_zeal=1) 
        mock_self = MagicMock()
        mock_self.is_fastened = True
        mock_self.value = None
        
        G = nx.DiGraph()
        G.add_node(NODE_ZERO, _typepath=[]) 
        mock_self._node_reference.graph = G
        
        mock_new_node = MagicMock()
        mock_new_node.node = 99
        mock_unroll.return_value = mock_new_node
        
        mock_self.get_potential_targets.side_effect = [[], [99]]
        
        with patch(f'{TARGET_MODULE}.rrandom') as mock_rrandom:
            mock_rrandom.choice.side_effect = [None, 99] 
            
            cls.mutate(mock_self)
            
            assert G.has_edge(NODE_ZERO, 99)
            mock_init.assert_called_once_with(mock_new_node)
            assert mock_self.value == 99

    @patch(f'{TARGET_MODULE}.get_structure')
    @patch(f'{TARGET_MODULE}.provide_tags')
    @patch(f'{TARGET_MODULE}.unroll_selement')
    @patch(f'{TARGET_MODULE}.initialize_subtree')
    def test_mutate_fails_when_no_target_and_no_zeal(self, mock_init, mock_unroll, mock_provide, mock_get_structure):
        cls = _global_reference(creative_zeal=0)
        mock_self = MagicMock()
        mock_self.is_fastened = True
        mock_self.value = None
        
        G = nx.DiGraph()
        G.add_node(NODE_ZERO, _typepath=[])
        mock_self._node_reference.graph = G

        mock_new_node = MagicMock()
        mock_new_node.node = 99
        mock_unroll.return_value = mock_new_node
        
        mock_self.get_potential_targets.return_value = []
        
        with pytest.raises(ByronOperatorFailure):
            cls.mutate(mock_self)