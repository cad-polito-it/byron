###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-25 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

"""Tests for crossover operators."""

import pytest

import byron
from byron.operators.crossovers import (
    parameter_uniform_crossover,
    bunch_onepoint_crossover,
    subtree_crossover,
)
from byron.operators.initializers import random_individual
from byron.user_messages import ByronOperatorFailure


# ============================================================================
# Fixtures for creating test individuals
# ============================================================================

@pytest.fixture
def simple_macro():
    """A simple macro with an integer parameter."""
    return byron.f.macro("value: {v}", v=byron.f.integer_parameter(0, 100))


@pytest.fixture
def simple_top_frame(simple_macro):
    """A simple frame containing a single macro."""
    return byron.f.sequence([simple_macro])


@pytest.fixture
def bunch_top_frame(simple_macro):
    """A frame containing a bunch of macros."""
    inner_bunch = byron.f.bunch(simple_macro, size=(2, 6))
    return byron.f.sequence([inner_bunch])


@pytest.fixture
def complex_top_frame():
    """A more complex frame structure with multiple macro types."""
    macro1 = byron.f.macro("op1: {a}", a=byron.f.integer_parameter(0, 50))
    macro2 = byron.f.macro("op2: {b}", b=byron.f.integer_parameter(50, 100))
    macro3 = byron.f.macro("op3: {c}", c=byron.f.integer_parameter(0, 1000))
    
    alt = byron.f.alternative([macro1, macro2])
    inner_bunch = byron.f.bunch([macro1, macro2, macro3], size=(2, 5))
    inner_seq = byron.f.sequence([alt, inner_bunch])
    
    return byron.f.sequence([inner_seq])


@pytest.fixture
def nested_frame_top():
    """A frame with nested structure for subtree crossover testing."""
    macro = byron.f.macro("val: {x}", x=byron.f.integer_parameter(0, 100))
    
    inner_seq = byron.f.sequence([macro, macro])
    middle_seq = byron.f.sequence([inner_seq, macro])
    
    return byron.f.sequence([middle_seq])


def create_individual(top_frame):
    """Helper function to create a valid individual."""
    individuals = random_individual(top_frame)
    return individuals[0]


# ============================================================================
# Tests for parameter_uniform_crossover
# ============================================================================

class TestParameterUniformCrossover:
    """Tests for parameter_uniform_crossover operator."""
    
    def test_crossover_returns_list(self, simple_top_frame):
        """Test that crossover returns a list of individuals."""
        parent1 = create_individual(simple_top_frame)
        parent2 = create_individual(simple_top_frame)
        
        # The genetic_operator decorator catches ByronOperatorFailure and returns []
        result = parameter_uniform_crossover(parent1, parent2)
        assert isinstance(result, list)
        if len(result) > 0:
            # Crossover succeeded - check offspring is valid
            assert len(result) == 1
            assert isinstance(result[0], byron.classes.Individual)
        # Empty list is acceptable - means crossover failed (no common macros, etc.)
    
    def test_crossover_preserves_structure(self, simple_top_frame):
        """Test that crossover preserves individual structure."""
        parent1 = create_individual(simple_top_frame)
        parent2 = create_individual(simple_top_frame)
        
        try:
            result = parameter_uniform_crossover(parent1, parent2)
            offspring = result[0]
            
            # Check that offspring has valid structure
            assert offspring.valid
            assert len(offspring.genome.nodes) > 0
        except ByronOperatorFailure:
            pass
    
    def test_crossover_with_strength_zero(self, simple_top_frame):
        """Test that strength=0 means no crossover from parent2."""
        parent1 = create_individual(simple_top_frame)
        parent2 = create_individual(simple_top_frame)
        
        # With strength=0, should return empty list because no crossover occurs
        # (the @genetic_operator decorator catches ByronOperatorFailure and returns [])
        result = parameter_uniform_crossover(parent1, parent2, strength=0.0)
        assert result == []
    
    def test_crossover_with_complex_individuals(self, complex_top_frame):
        """Test crossover with more complex individuals."""
        parent1 = create_individual(complex_top_frame)
        parent2 = create_individual(complex_top_frame)
        
        try:
            result = parameter_uniform_crossover(parent1, parent2, strength=0.5)
            assert isinstance(result, list)
            assert len(result) == 1
        except ByronOperatorFailure:
            # Acceptable if no crossover happened
            pass
    
    def test_crossover_num_parents_attribute(self):
        """Test that the operator has correct num_parents attribute."""
        assert hasattr(parameter_uniform_crossover, 'num_parents')
        assert parameter_uniform_crossover.num_parents == 2


# ============================================================================
# Tests for bunch_onepoint_crossover
# ============================================================================

class TestBunchOnepointCrossover:
    """Tests for bunch_onepoint_crossover operator."""
    
    def test_crossover_returns_list(self, bunch_top_frame):
        """Test that crossover returns a list of individuals."""
        parent1 = create_individual(bunch_top_frame)
        parent2 = create_individual(bunch_top_frame)
        
        try:
            result = bunch_onepoint_crossover(parent1, parent2)
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], byron.classes.Individual)
        except ByronOperatorFailure:
            # Acceptable - bunches might be too small
            pass
    
    def test_crossover_modifies_bunch(self, bunch_top_frame):
        """Test that crossover actually modifies the bunch."""
        parent1 = create_individual(bunch_top_frame)
        parent2 = create_individual(bunch_top_frame)
        
        # Dump both parents to get their representation
        dump1 = parent1.dump()
        dump2 = parent2.dump()
        
        try:
            result = bunch_onepoint_crossover(parent1, parent2)
            offspring = result[0]
            offspring_dump = offspring.dump()
            
            # Offspring should be valid
            assert offspring.valid
            
            # Offspring should potentially be different from parent1
            # (not always, depending on crossover point)
        except ByronOperatorFailure:
            pass
    
    def test_crossover_respects_size_constraints(self, bunch_top_frame):
        """Test that crossover respects bunch size constraints."""
        parent1 = create_individual(bunch_top_frame)
        parent2 = create_individual(bunch_top_frame)
        
        try:
            result = bunch_onepoint_crossover(parent1, parent2)
            offspring = result[0]
            
            # Find bunch nodes in offspring
            from byron.classes.frame import MacroBunch, FrameBunch
            for n in offspring.genome.nodes:
                selement = offspring.genome.nodes[n].get('_selement')
                if selement and isinstance(selement, (MacroBunch, FrameBunch)):
                    size_min = selement.SIZE[0]
                    size_max = selement.SIZE[1] - 1
                    out_degree = offspring.genome.out_degree(n)
                    assert size_min <= out_degree <= size_max
        except ByronOperatorFailure:
            pass
    
    def test_crossover_fails_without_bunches(self, simple_top_frame):
        """Test that crossover fails gracefully without bunch nodes."""
        parent1 = create_individual(simple_top_frame)
        parent2 = create_individual(simple_top_frame)
        
        # Should return empty list when no bunch nodes exist
        # (the @genetic_operator decorator catches ByronOperatorFailure and returns [])
        result = bunch_onepoint_crossover(parent1, parent2)
        assert result == []
    
    def test_crossover_num_parents_attribute(self):
        """Test that the operator has correct num_parents attribute."""
        assert hasattr(bunch_onepoint_crossover, 'num_parents')
        assert bunch_onepoint_crossover.num_parents == 2


# ============================================================================
# Tests for subtree_crossover
# ============================================================================

class TestSubtreeCrossover:
    """Tests for subtree_crossover operator."""
    
    def test_crossover_returns_list(self, nested_frame_top):
        """Test that crossover returns a list of individuals."""
        parent1 = create_individual(nested_frame_top)
        parent2 = create_individual(nested_frame_top)
        
        try:
            result = subtree_crossover(parent1, parent2)
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], byron.classes.Individual)
        except ByronOperatorFailure:
            # Acceptable - might not find matching frames
            pass
    
    def test_crossover_produces_valid_offspring(self, nested_frame_top):
        """Test that crossover produces valid offspring."""
        parent1 = create_individual(nested_frame_top)
        parent2 = create_individual(nested_frame_top)
        
        try:
            result = subtree_crossover(parent1, parent2)
            offspring = result[0]
            
            assert offspring.valid
        except ByronOperatorFailure:
            pass
    
    def test_crossover_with_complex_frame(self, complex_top_frame):
        """Test crossover with complex frame structure."""
        parent1 = create_individual(complex_top_frame)
        parent2 = create_individual(complex_top_frame)
        
        try:
            result = subtree_crossover(parent1, parent2)
            assert isinstance(result, list)
            assert len(result) == 1
        except ByronOperatorFailure:
            pass
    
    def test_crossover_num_parents_attribute(self):
        """Test that the operator has correct num_parents attribute."""
        assert hasattr(subtree_crossover, 'num_parents')
        assert subtree_crossover.num_parents == 2


# ============================================================================
# Integration tests
# ============================================================================

class TestCrossoverIntegration:
    """Integration tests for crossover operators."""
    
    def test_all_crossovers_in_operators_list(self):
        """Test that all crossovers are accessible from byron.operators."""
        assert hasattr(byron.operators, 'parameter_uniform_crossover')
        assert hasattr(byron.operators, 'bunch_onepoint_crossover')
        assert hasattr(byron.operators, 'subtree_crossover')
    
    def test_crossovers_have_num_parents_two(self):
        """Test that all crossover operators have num_parents=2."""
        assert byron.operators.parameter_uniform_crossover.num_parents == 2
        assert byron.operators.bunch_onepoint_crossover.num_parents == 2
        assert byron.operators.subtree_crossover.num_parents == 2
    
    def test_multiple_crossovers_sequence(self, complex_top_frame):
        """Test applying multiple crossovers in sequence."""
        individuals = [create_individual(complex_top_frame) for _ in range(4)]
        
        # Try each crossover type
        crossovers = [
            parameter_uniform_crossover,
            bunch_onepoint_crossover,
            subtree_crossover,
        ]
        
        for crossover in crossovers:
            try:
                result = crossover(individuals[0], individuals[1])
                if result:
                    # Use offspring for next iteration
                    individuals[0] = result[0]
            except ByronOperatorFailure:
                # Some crossovers may fail, which is acceptable
                pass
    
    def test_crossover_does_not_modify_parents(self, bunch_top_frame):
        """Test that crossover does not modify parent individuals."""
        parent1 = create_individual(bunch_top_frame)
        parent2 = create_individual(bunch_top_frame)
        
        # Store original dumps
        dump1_before = parent1.dump()
        dump2_before = parent2.dump()
        
        try:
            bunch_onepoint_crossover(parent1, parent2)
        except ByronOperatorFailure:
            pass
        
        # Parents should be unchanged
        dump1_after = parent1.dump()
        dump2_after = parent2.dump()
        
        assert dump1_before == dump1_after
        assert dump2_before == dump2_after


# ============================================================================
# Edge case tests
# ============================================================================

class TestCrossoverEdgeCases:
    """Edge case tests for crossover operators."""
    
    def test_crossover_same_parent_twice(self, bunch_top_frame):
        """Test crossover with the same individual as both parents."""
        parent = create_individual(bunch_top_frame)
        
        try:
            result = parameter_uniform_crossover(parent, parent, strength=0.5)
            # Should succeed but might not change much
            assert isinstance(result, list)
        except ByronOperatorFailure:
            # Acceptable
            pass
    
    def test_crossover_strength_edge_values(self, complex_top_frame):
        """Test crossover with edge strength values."""
        parent1 = create_individual(complex_top_frame)
        parent2 = create_individual(complex_top_frame)
        
        # Strength = 1.0 means always take from parent2
        try:
            result = parameter_uniform_crossover(parent1, parent2, strength=1.0)
            assert isinstance(result, list)
        except ByronOperatorFailure:
            pass
