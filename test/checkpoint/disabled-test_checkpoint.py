#!/usr/bin/env python3
"""Quick test to verify checkpoint functionality works"""

import sys
import os
import tempfile
from pathlib import Path

# Add Byron to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import byron
from byron.tools.checkpoint import save_population, load_population, save_individuals, load_individuals


def test_basic_checkpoint():
    """Test basic save/load of population"""
    print("Testing basic checkpoint functionality...")
    
    # Create a simple problem
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', 20))
    top_frame = byron.f.sequence([macro])
    
    @byron.fitness_function
    def fitness(phenotype: str) -> int:
        return phenotype.count('1')
    
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    # Run short evolution
    print("  Running evolution...")
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=5,
        lambda_=10,
        max_generation=5,
        target_fitness=byron.fitness.make_fitness(20)
    )
    
    original_gen = population.generation
    original_fitness = population[0].fitness
    original_size = len(population)
    
    print(f"  Original - Gen: {original_gen}, Size: {original_size}, Best: {original_fitness}")
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
        temp_file = f.name
    
    try:
        print(f"  Saving to {temp_file}...")
        save_population(population, temp_file)
        
        print(f"  Loading from {temp_file}...")
        loaded_pop = load_population(temp_file)
        
        # Verify
        assert loaded_pop.generation == original_gen, "Generation mismatch!"
        assert len(loaded_pop) == original_size, "Size mismatch!"
        assert loaded_pop[0].fitness == original_fitness, "Fitness mismatch!"
        
        print("  ✓ Population saved and loaded successfully!")
        
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_save_individuals():
    """Test saving specific individuals"""
    print("\nTesting save_individuals functionality...")
    
    # Create a simple problem
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', 10))
    top_frame = byron.f.sequence([macro])
    
    @byron.fitness_function
    def fitness(phenotype: str) -> int:
        return phenotype.count('1')
    
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    # Run short evolution
    print("  Running evolution...")
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=10,
        lambda_=20,
        max_generation=3,
        target_fitness=byron.fitness.make_fitness(10)
    )
    
    # Save top 3
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
        temp_file = f.name
    
    try:
        print("  Saving top 3 individuals...")
        save_individuals(population, temp_file, top_n=3)
        
        print("  Loading individuals...")
        data = load_individuals(temp_file)
        
        # Verify
        assert data['num_saved'] == 3, "Should have saved 3 individuals!"
        assert len(data['individuals']) == 3, "Should have loaded 3 individuals!"
        assert data['generation'] == population.generation, "Generation mismatch!"
        
        print(f"  ✓ Saved and loaded {data['num_saved']} individuals successfully!")
        
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    print("="*60)
    print("Byron Checkpoint Module Tests")
    print("="*60)
    
    try:
        test_basic_checkpoint()
        test_save_individuals()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
