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

import byron.framework.parameter as parameter

class TestNumericParameter:

    def test_numeric_initialization(self):
        IntParam = parameter._numeric(type_=int, min_=0, max_=10)
        assert IntParam.MAX == 10
        assert IntParam.MIN == 0

    def test_is_correct_for_integers(self):
        IntParam = parameter._numeric(type_=int, min_=0, max_=10)
        p = IntParam()
        assert p.is_correct(5) is True      #correct
        assert p.is_correct(10) is False    # wrong range
        assert p.is_correct(5.5) is False   # wrong type

    def test_run_paranoia_checks_fail(self):
        IntParam = parameter._numeric(type_=int, min_=0, max_=10)
        p = IntParam()
        p._value = 15  #  
        with pytest.raises(AssertionError, match="TypeError: not a <class 'int'> in range 0-10"):
            p.run_paranoia_checks()

    @patch('byron.framework.parameter.rrandom') #
    def test_mutate_int(self, mock_rrandom):
        mock_rrandom.random_int.return_value = 7 #
        IntParam = parameter._numeric(type_=int, min_=0, max_=10)
        p = IntParam()
        p._value = 5
        p.mutate(strength=0.5)
        
        mock_rrandom.random_int.assert_called_once_with(0, 10, loc=5, strength=0.5)
        assert p.value == 7 #

class TestIntegerParameter:
    
    def test_integer_parameter_valid(self):
        IntParam = parameter.integer_parameter(min_=0, max_=10)
        assert IntParam.MIN == 0
        assert IntParam.MAX == 10

    @patch('byron.framework.parameter.syntax_warning_hint') # 
    def test_integer_parameter_warning_small_range(self, mock_warning):
        parameter.integer_parameter(min_=5, max_=6)
        mock_warning.assert_called_once()


class TestFloatParameter:

    def test_float_parameter_valid(self):
        FloatParam = parameter.float_parameter(min_=0.0, max_=5.5)
        assert FloatParam.MIN == 0.0
        assert FloatParam.MAX == 5.5

class TestChoiceParameter:

    def test_choice_parameter_valid_and_sorted(self):
        ChoiceParam = parameter.choice_parameter(alternatives=[3, 1, 2])
        assert ChoiceParam.ALTERNATIVES == (1, 2, 3)

    @patch('byron.framework.parameter.syntax_warning_hint')
    def test_choice_parameter_size_warning(self, mock_warning):
        large_list = list(range(1000))
        parameter.choice_parameter(alternatives=large_list)
        assert "impair performances" in mock_warning.call_args[0][0]

class TestChoiceParameterInstance:

    def test_is_correct(self):
        ChoiceParam = parameter.choice_parameter(alternatives=["apple", "banana", "cherry"])
        p = ChoiceParam()
        assert p.is_correct("apple") is True
        assert p.is_correct("orange") is False

    @patch('byron.framework.parameter.rrandom')
    def test_mutate(self, mock_rrandom):
        ChoiceParam = parameter.choice_parameter(alternatives=[10, 20, 30])
        p = ChoiceParam()
        p._value = 10
        mock_rrandom.choice.return_value = 20
        
        p.mutate(strength=1.0)
        mock_rrandom.choice.assert_called_with((10, 20, 30))
        assert p.value == 20

class TestArrayParameterRange:

    def test_initialization_constants(self):
        ArrayParam = parameter._array_parameter_range(min_=0, max_=10, length=3, sep=',')
        assert ArrayParam.RANGE == (0, 10)
        assert ArrayParam.LENGTH == 3
        assert ArrayParam.SEP == ','

    def test_is_correct(self):
        ArrayParam = parameter._array_parameter_range(min_=0, max_=10, length=3, sep=',')
        p = ArrayParam()
        
        assert p.is_correct("5,0,9") is True
        
        assert p.is_correct("10,2,3") is False 
        
        assert p.is_correct("-1,5,5") is False 
        
        with pytest.raises(ValueError):
            p.is_correct("A,2,3")

    @patch('byron.framework.parameter.rrandom')
    def test_mutate_full_strength(self, mock_rrandom):
        
        ArrayParam = parameter._array_parameter_range(min_=0, max_=10, length=3, sep=',')
        p = ArrayParam()
        mock_rrandom.random_int.side_effect = [5, 2, 8]
        
        p.mutate(strength=1.0)
        
        assert p.value == "5,2,8"
        assert mock_rrandom.random_int.call_count == 3

    @patch('byron.framework.parameter.rrandom')
    def test_mutate_partial_strength(self, mock_rrandom):
        
        ArrayParam = parameter._array_parameter_range(min_=0, max_=10, length=3, sep=',')
        p = ArrayParam()
        p._raw_value = [1, 1, 1] 
        mock_rrandom.boolean.side_effect = [False, True, False]
        
        mock_rrandom.random_int.side_effect = [9] 
        
        p.mutate(strength=0.5)
        
        assert p._raw_value == [1, 9, 1]
        assert p.value == "1,9,1"

class TestArrayParameterStr:

    def test_initialization_constants(self):
        ArrayParam = parameter._array_parameter_str(symbols=('A', 'B', 'C'), length=3, sep='-')
        assert ArrayParam.DIGITS == ('A', 'B', 'C')
        assert ArrayParam.LENGTH == 3

    def test_is_correct(self):
        ArrayParam = parameter._array_parameter_str(symbols=('A', 'B', 'C'), length=3, sep='')
        p = ArrayParam()
        
        assert p.is_correct(['A', 'B', 'A']) is True
        assert p.is_correct(['A', 'B']) is False         
        assert p.is_correct(['A', 'B', 'C', 'A']) is False 
        assert p.is_correct(['A', 'X', 'C']) is False     

    @patch('byron.framework.parameter.rrandom') 
    def test_mutate_full_strength(self, mock_rrandom):
        ArrayParam = parameter._array_parameter_str(symbols=('A', 'B'), length=3, sep='-')
        p = ArrayParam()
        mock_rrandom.choice.side_effect = ['A', 'B', 'A']
        
        with patch.object(ArrayParam, 'is_correct', return_value=True):
            p.mutate(strength=1.0)
    
        assert p.value == "A-B-A"
        assert mock_rrandom.choice.call_count == 3

    @patch('byron.framework.parameter.rrandom')
    def test_mutate_partial_strength(self, mock_rrandom):
        ArrayParam = parameter._array_parameter_str(symbols=('A', 'B'), length=3, sep='-')
        p = ArrayParam()
        p._raw_value = ['A', 'A', 'A'] 
        
        mock_rrandom.boolean.side_effect = [True, False, True]
        mock_rrandom.choice.side_effect = ['B', 'B'] 
        
        with patch.object(ArrayParam, 'is_correct', return_value=True):
            p.mutate(strength=0.5)
        
        assert p._raw_value == ['B', 'A', 'B']
        assert p.value == "B-A-B"

class TestArrayParameterRouter:

    def test_array_parameter_with_range(self):
        ArrayParam = parameter.array_parameter(symbols=range(0, 5), length=4)
        
        assert hasattr(ArrayParam, 'RANGE')
        assert ArrayParam.RANGE == (0, 5)
        assert ArrayParam.LENGTH == 4
        assert ArrayParam.SEP == ' '

    def test_array_parameter_with_strings(self):
        ArrayParam = parameter.array_parameter(symbols=['B', 'A'], length=2)
        
        assert hasattr(ArrayParam, 'DIGITS')
        assert ArrayParam.DIGITS == ('A', 'B')
        assert ArrayParam.LENGTH == 2

    def test_array_parameter_custom_sep(self):
        ArrayParam = parameter.array_parameter(symbols=range(0, 5), length=4, sep='-')
        assert ArrayParam.SEP == '-'  


class TestCounterParameter:

    def test_is_correct(self):
        CounterParam = parameter.counter_parameter()
        p = CounterParam()
        
        assert p.is_correct(100) is True
        assert p.is_correct("anything") is True

    def test_mutate_increments(self):
        CounterParam = parameter.counter_parameter()
        
        CounterParam.COUNTER = 0
        
        p1 = CounterParam()
        
        p1.mutate()
        assert p1.value == 1
        
        p1.mutate()
        assert p1.value == 2
        
        p2 = CounterParam()
        p2.mutate()
        assert p2.value == 3      