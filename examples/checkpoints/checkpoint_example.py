#!/usr/bin/env python3
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

"""
Example: Saving and Loading Populations with Checkpoints

This example demonstrates how to:
1. Save a population during/after evolution
2. Load a saved population
3. Extract and save specific individuals
4. Manually create a new population from saved individuals

Use cases:
- Resume interrupted evolution runs
- Save best solutions from multiple runs
- Analyze evolved populations offline
- Create hall of fame with best individuals
"""

import byron
from byron.tools.checkpoint import save_population, load_population, save_individuals, load_individuals

# Problem configuration
NUM_BITS = 100


@byron.fitness_function
def fitness(phenotype: str) -> int:
    """OneMax: count the number of '1's in the bitstring"""
    return phenotype.count('1')


def run_and_save_checkpoint():
    """Example 1: Run evolution and save checkpoint"""
    print("\n=== Example 1: Running evolution and saving checkpoint ===")
    
    # Define the problem
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    # Run evolution for 50 generations
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=10,
        lambda_=20,
        max_generation=50,
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    # Save the entire population
    save_population(population, 'checkpoint_gen50.pkl')
    
    # Save only top 5 individuals
    save_individuals(population, 'top5_gen50.pkl', top_n=5)
    
    print(f"Saved population at generation {population.generation}")
    print(f"Best fitness: {population[0].fitness}")
    return population


def load_and_analyze():
    """Example 2: Load saved population and analyze it"""
    print("\n=== Example 2: Loading and analyzing saved population ===")
    
    # Load the full population
    population = load_population('checkpoint_gen50.pkl')
    
    print(f"Loaded population from generation {population.generation}")
    print(f"Population size: {len(population)}")
    print(f"Best individual: {population[0].describe(include_structure=False)}")
    
    # Show top 3 individuals
    print("\nTop 3 individuals:")
    for i in range(min(3, len(population))):
        ind = population[i]
        print(f"  #{i+1}: {ind.fitness} - {ind}")
    
    return population


def load_individuals_example():
    """Example 3: Load specific individuals and inspect them"""
    print("\n=== Example 3: Loading saved individuals ===")
    
    # Load the top 5 individuals we saved
    data = load_individuals('top5_gen50.pkl')
    
    print(f"Loaded {data['num_saved']} individuals from generation {data['generation']}")
    print(f"Original population had {data['total_population_size']} individuals")
    
    # Inspect each individual
    for i, ind in enumerate(data['individuals']):
        print(f"\nIndividual {i+1}:")
        print(f"  ID: {ind.id}")
        print(f"  Fitness: {ind.fitness}")
        print(f"  Age: {ind.age}")
        if ind.lineage:
            print(f"  Lineage: {ind.lineage}")
    
    return data


def create_population_from_saved():
    """Example 4: Create a new population from saved individuals"""
    print("\n=== Example 4: Creating population from saved individuals ===")
    
    # Load individuals
    data = load_individuals('top5_gen50.pkl')
    
    # Create a new population with the same configuration
    new_population = byron.classes.Population(
        data['top_frame'],
        extra_parameters=data['population_extra_parameters']
    )
    
    # Add the loaded individuals
    # Note: We need to clone them to avoid issues with generation counter
    cloned_individuals = [ind.clone for ind in data['individuals']]
    new_population += cloned_individuals
    
    print(f"Created new population with {len(new_population)} individuals")
    print(f"New population generation: {new_population.generation}")
    
    # Now you could continue evolution with this population
    # However, you'd need to re-create the evaluator and manually
    # integrate with the EA (see advanced example below)
    
    return new_population


def resume_evolution_manually():
    """Example 5: Continue evolution by tracking generation numbers"""
    print("\n=== Example 5: Continuing evolution from checkpoint ===")
    
    # Load saved population
    population = load_population('checkpoint_gen50.pkl')
    
    starting_gen = population.generation
    previous_best = population[0].fitness
    
    print(f"Loaded population from generation {starting_gen}")
    print(f"Previous best fitness: {previous_best}")
    
    # Recreate problem definition
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    print(f"\nContinuing evolution for 30 more generations...")
    print(f"(Starting fresh run, but tracking we're logically at gen {starting_gen})")
    
    # Run another session
    new_population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=10,
        lambda_=20,
        max_generation=30,
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    # Track total progress
    actual_generation = starting_gen + new_population.generation
    new_best = new_population[0].fitness
    
    print(f"\n✓ Continuation complete!")
    print(f"✓ Previous best (gen {starting_gen}): {previous_best}")
    print(f"✓ New best (gen {actual_generation}): {new_best}")
    
    if new_best > previous_best:
        improvement = new_best.values[0] - previous_best.values[0]
        print(f"✓ Improvement: +{improvement}")
    
    print(f"\n💡 You're logically at generation {actual_generation} across sessions!")
    
    return new_population


def main():
    """Run all examples"""
    byron.welcome()
    
    try:
        # Example 1: Run and save
        run_and_save_checkpoint()
        
        # Example 2: Load and analyze
        load_and_analyze()
        
        # Example 3: Load specific individuals
        load_individuals_example()
        
        # Example 4: Create population from saved
        create_population_from_saved()
        
        # Example 5: Discussion on resuming evolution
        resume_evolution_manually()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("Check the generated .pkl files:")
        print("  - checkpoint_gen50.pkl  (full population)")
        print("  - top5_gen50.pkl        (top 5 individuals)")
        print("="*60)
        
    except FileNotFoundError:
        print("\nNote: Some examples require checkpoint files from previous examples.")
        print("Run all examples in sequence to see full functionality.")


if __name__ == "__main__":
    main()
