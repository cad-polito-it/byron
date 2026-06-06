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
import uuid

from unittest.mock import patch

import byron as byron

import byron.framework.shared as shared

def create_dummy_parameter_class():
    
    class DummyParameter:
        def __init__(self):
            self.key = str(uuid.uuid4())
            self._value = 10
            self.mutate_call_count = 0

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, new_val):
            self._value = new_val

        def mutate(self, strength: float = 1.0) -> None:
            self.mutate_call_count += 1

        def is_correct(self, obj) -> bool:
            return obj == "correct_value"

    return DummyParameter


# ==========================================
# tests
# ==========================================
class TestSharedParameter:

    def test_ownership_initialization(self):
        DummyClass = create_dummy_parameter_class()
        SharedParamClass = shared.make_shared_parameter(DummyClass)
        
        instance1 = SharedParamClass()
        assert instance1.is_owner is True
        assert instance1._is_owner is True
        
        instance2 = SharedParamClass()
        assert instance2.is_owner is False

    def test_value_getter_and_shared_state(self):
        DummyClass = create_dummy_parameter_class()
        SharedParamClass = shared.make_shared_parameter(DummyClass)
        
        owner = SharedParamClass()
        viewer = SharedParamClass()
        
        assert owner.value == 10
        assert viewer.value == 10

    def test_value_setter_permissions(self):
        DummyClass = create_dummy_parameter_class()
        SharedParamClass = shared.make_shared_parameter(DummyClass)
        
        owner = SharedParamClass()
        viewer = SharedParamClass()
        
        owner.value = 50
        assert owner.value == 50
        assert viewer.value == 50
        
        viewer.value = 99 
        
        assert viewer.value == 50 
        assert owner.value == 50

    def test_mutate_permissions(self):
        DummyClass = create_dummy_parameter_class()
        SharedParamClass = shared.make_shared_parameter(DummyClass)
        
        owner = SharedParamClass()
        viewer = SharedParamClass()
        
        # 1.
        owner.mutate(strength=0.5)
        assert viewer.value == 10 
        
        # 2.
        viewer.mutate(strength=1.0)

    def test_is_correct(self):
        DummyClass = create_dummy_parameter_class()
        SharedParamClass = shared.make_shared_parameter(DummyClass)
        
        p = SharedParamClass()
        
        assert p.is_correct("correct_value") is True
        assert p.is_correct("wrong_value") is False

    @patch('byron.classes.parameter.ParameterSharedABC._patch_info')
    def test_class_naming(self, mock_patch_info):
        DummyClass = create_dummy_parameter_class()
        
        SharedParamClass = shared.make_shared_parameter(DummyClass)
        
        mock_patch_info.assert_called_once_with(name="Shared❬DummyParameter❭")