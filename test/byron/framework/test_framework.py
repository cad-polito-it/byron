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
from functools import partial


import byron as byron

import byron.framework.framework as framework

@pytest.fixture(autouse=True)
def mock_validators():
    with patch('byron.framework.framework.check_valid_type', return_value=True), \
         patch('byron.framework.framework.check_valid_types', return_value=True), \
         patch('byron.framework.framework.check_valid_length', return_value=True), \
         patch('byron.framework.framework.cook_selement_list', side_effect=lambda x: tuple(x)):
        yield

class DummyMacro:
    pass

class DummyFrame:
   pass

DummyMacro = type('DummyMacro', (framework.Macro,), {})
DummyMacro2 = type('DummyMacro2', (framework.Macro,), {})
DummyFrame = type('DummyFrame', (framework.FrameABC,), {})

@patch('byron.framework.framework.SE_DIRECTORY', new_callable=set) 
class TestAlternative:

    @patch('byron.framework.framework.rrandom')
    def test_successors_returns_random_choice(self, mock_rrandom, mock_se_dir):
        Dummy1, Dummy2 = MagicMock(), MagicMock()
        mock_rrandom.choice.return_value = Dummy2 
        
        FrameClass = framework.alternative(alternatives=[Dummy1, Dummy2])
        instance = FrameClass()
        
        assert instance.successors == [Dummy2]
        mock_rrandom.choice.assert_called_once_with((Dummy1, Dummy2))

    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_naming_logic(self, mock_patch_info, mock_se_dir):
        Dummy1 = MagicMock()
        
        framework.alternative(alternatives=[Dummy1], name="MyCustomAlt")
        mock_patch_info.assert_called_with(custom_class_id="MyCustomAlt")
        
        framework.alternative(alternatives=[Dummy1])
        mock_patch_info.assert_called_with(name="FrameAlternative#")

    @patch('byron.classes.frame.FrameABC.add_node_check')
    def test_max_instances(self, mock_add_check, mock_se_dir):
        Dummy1 = MagicMock()
        
        framework.alternative(alternatives=[Dummy1], max_instances=5)
        
        mock_add_check.assert_called_once()
        args, _ = mock_add_check.call_args
        partial_func = args[0]
        
        assert isinstance(partial_func, framework.partial)
        assert partial_func.func.__name__ == '_check_instances_number'
        assert partial_func.keywords == {'max_instances': 5}

@patch('byron.framework.framework.SE_DIRECTORY', new_callable=set)
class TestSequence:

    def test_successors_returns_all_elements(self, mock_se_dir):
        Dummy1, Dummy2 = MagicMock(), MagicMock()
        
        FrameClass = framework.sequence(seq=[Dummy1, Dummy2])
        instance = FrameClass()
        
        assert instance.successors == (Dummy1, Dummy2)

    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_naming_logic(self, mock_patch_info, mock_se_dir):
        Dummy1, Dummy2 = MagicMock(), MagicMock()
        
        framework.sequence(seq=[Dummy1, Dummy2], name="MySequence")
        mock_patch_info.assert_called_with(custom_class_id="MySequence")
        
        framework.sequence(seq=[Dummy1])
        mock_patch_info.assert_called_with(name="SingleFrame#")
        
        framework.sequence(seq=[Dummy1, Dummy2])
        mock_patch_info.assert_called_with(name="FrameSequence#")

    @patch('byron.classes.frame.FrameABC.add_node_check')
    def test_max_instances(self, mock_add_check, mock_se_dir):
        Dummy1 = MagicMock()
        
        framework.sequence(seq=[Dummy1, Dummy1], max_instances=10)
        
        mock_add_check.assert_called_once()
        partial_func = mock_add_check.call_args[0][0]
        assert partial_func.keywords == {'max_instances': 10}

class TestNodeChecks:

    def test_check_out_degree(self):
        mock_node = MagicMock()
        mock_node.out_degree = 5
        
        assert framework._check_out_degree(mock_node, min_=0, max_=10) is True
        assert framework._check_out_degree(mock_node, min_=5, max_=6) is True
        assert framework._check_out_degree(mock_node, min_=0, max_=5) is False 
        assert framework._check_out_degree(mock_node, min_=6, max_=10) is False

    def test_check_instances_number(self):
        mock_node = MagicMock()
        
        class MySElement: pass
        target_selement = MySElement()
        mock_node.selement = target_selement
        
        mock_node.graph.nodes.return_value = [
            ("node1", MySElement()), 
            ("node2", MySElement()), 
            ("node3", "DifferentType")
        ]
        
        assert framework._check_instances_number(mock_node, max_instances=3) is True
        assert framework._check_instances_number(mock_node, max_instances=2) is True
        assert framework._check_instances_number(mock_node, max_instances=1) is False


# ==========================================
# 2. Tests for bunch() Factory
# ==========================================
@patch('byron.framework.framework.SE_DIRECTORY', new_callable=set)
class TestBunchFactory:

    @pytest.fixture(autouse=True)
    def mock_dependencies(self):
        with patch('byron.framework.framework.check_valid_type', return_value=True), \
             patch('byron.framework.framework.check_valid_types', return_value=True), \
             patch('byron.framework.framework.check_valid_length', return_value=True):
            yield

    @patch('byron.framework.framework.syntax_warning_hint')
    def test_debug_hints_warnings(self, mock_warning, mock_se_dir):
        framework.bunch(pool=[DummyMacro], size=(2, 3))
        mock_warning.assert_called_with(
            "Ranges are half open: the size of this macro bunch is always 2 — did you mean 'size=2'?",
            stacklevel_offset=1
        )
        
        framework.bunch(pool=[DummyMacro, DummyMacro], size=1)
        mock_warning.assert_called_with(
            "Found duplicate macros in pool — considering using 'weights'",
            stacklevel_offset=1
        )

    def test_mixed_types_assertion(self, mock_se_dir):
        with pytest.raises(AssertionError, match="Mixed Frame/Macro bunches are not yet supported"):
            framework.bunch(pool=[DummyMacro, DummyFrame], size=1)

    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_weights_logic(self, mock_patch, mock_se_dir):
        BunchClass = framework.bunch(pool=[DummyMacro, DummyMacro2], size=1, weights=[3, 1])
        assert BunchClass.POOL == (DummyMacro, DummyMacro, DummyMacro, DummyMacro2)

    @patch('byron.framework.framework.rrandom')
    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_successors_random_size(self, mock_patch, mock_rrandom, mock_se_dir):
        BunchClass = framework.bunch(pool=[DummyMacro], size=(2, 5))
        instance = BunchClass()
        
        mock_rrandom.random_int.return_value = 3
        mock_rrandom.choice.return_value = "SelectedNode"
        
        result = instance.successors
        
        assert len(result) == 3
        assert result == ["SelectedNode", "SelectedNode", "SelectedNode"]
        mock_rrandom.random_int.assert_called_once_with(2, 5)

    @patch('byron.framework.framework.rrandom')
    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_successors_fixed_initial_size(self, mock_patch, mock_rrandom, mock_se_dir):
        BunchClass = framework.bunch(pool=[DummyMacro], size=(1, 10, 4))
        instance = BunchClass()
        
        mock_rrandom.choice.return_value = "Node"
        
        result = instance.successors
        
        assert len(result) == 4
        mock_rrandom.random_int.assert_not_called()

    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_naming_logic(self, mock_patch_info, mock_se_dir):
        framework.bunch(pool=[DummyMacro], size=1, name="MyBunch")
        mock_patch_info.assert_called_with(custom_class_id="MyBunch")
        
        framework.bunch(pool=[DummyMacro], size=1)
        mock_patch_info.assert_called_with(name="SingleMacro#")
        
        framework.bunch(pool=[DummyFrame], size=(3, 4))
        mock_patch_info.assert_called_with(name="FrameArray#")
        
        framework.bunch(pool=[DummyFrame], size=(1, 5))
        mock_patch_info.assert_called_with(name="FrameBunch#")

    @pytest.fixture(autouse=True)
    def mock_dependencies(self):
        with patch('byron.framework.framework.check_valid_type', return_value=True), \
             patch('byron.framework.framework.check_valid_types', return_value=True), \
             patch('byron.framework.framework.check_valid_length', return_value=True):
            yield
            
   

    @patch('byron.framework.framework.syntax_warning_hint')
    def test_debug_hints_warnings(self, mock_warning, mock_se_dir):
        
        framework.bunch(pool=[DummyMacro], size=(2, 3))
        mock_warning.assert_called_with(
            "Ranges are half open: the size of this macro bunch is always 2 — did you mean 'size=2'?",
            stacklevel_offset=1
        )
        
        framework.bunch(pool=[DummyMacro, DummyMacro], size=1)
        mock_warning.assert_called_with(
            "Found duplicate macros in pool — considering using 'weights'",
            stacklevel_offset=1
        )

    def test_mixed_types_assertion(self, mock_se_dir):
        """تست ارور دادن در صورتی که ماکرو و فریم با هم ترکیب شوند"""
        with pytest.raises(AssertionError, match="Mixed Frame/Macro bunches are not yet supported"):
            framework.bunch(pool=[DummyMacro, DummyFrame], size=1)

    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_weights_logic(self, mock_patch, mock_se_dir):
        """POOL"""
        BunchClass = framework.bunch(pool=[DummyMacro, DummyMacro2], size=1, weights=[3, 1])
        
        assert BunchClass.POOL == (DummyMacro, DummyMacro, DummyMacro, DummyMacro2)

    @patch('byron.framework.framework.rrandom')
    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_successors_random_size(self, mock_patch, mock_rrandom, mock_se_dir):
        """successorم"""
        BunchClass = framework.bunch(pool=[DummyMacro], size=(2, 5))
        instance = BunchClass()
        
        mock_rrandom.random_int.return_value = 3
        mock_rrandom.choice.return_value = "SelectedNode"
        
        result = instance.successors
        
        assert len(result) == 3
        assert result == ["SelectedNode", "SelectedNode", "SelectedNode"]
        mock_rrandom.random_int.assert_called_once_with(2, 5)

    @patch('byron.framework.framework.rrandom')
    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_successors_fixed_initial_size(self, mock_patch, mock_rrandom, mock_se_dir):
        """successor"""
        
        BunchClass = framework.bunch(pool=[DummyMacro], size=(1, 10, 4))
        instance = BunchClass()
        
        mock_rrandom.choice.return_value = "Node"
        
        result = instance.successors
        
        assert len(result) == 4
        
        mock_rrandom.random_int.assert_not_called()

    @patch('byron.classes.frame.FrameABC._patch_info')
    def test_naming_logic(self, mock_patch_info, mock_se_dir):
        
        framework.bunch(pool=[DummyMacro], size=1, name="MyBunch")
        mock_patch_info.assert_called_with(custom_class_id="MyBunch")
        
        framework.bunch(pool=[DummyMacro], size=1)
        mock_patch_info.assert_called_with(name="SingleMacro#")
      
        framework.bunch(pool=[DummyFrame], size=(3, 4))
        mock_patch_info.assert_called_with(name="FrameArray#")
   
        framework.bunch(pool=[DummyFrame], size=(1, 5))
        mock_patch_info.assert_called_with(name="FrameBunch#")