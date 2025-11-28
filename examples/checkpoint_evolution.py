#!/usr/bin/env python3
"""
Multi-Session Evolution Example with Checkpointing

Demonstrates how to use simple_ea() with checkpoint features to:
1. Save checkpoints periodically during evolution
2. Checkpoint when finding better solutions
3. Use custom callbacks for user-controlled checkpointing
"""

import byron
from pathlib import Path

NUM_BITS = 50
CHECKPOINT_DIR = Path('checkpoints')


@byron.fitness_function
def fitness(phenotype: str) -> int:
    """OneMax: count the number of '1's"""
    return phenotype.count('1')


def example_1_periodic_checkpointing():
    """Save checkpoint every 10 generations"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Periodic Checkpointing")
    print("="*60)
    
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    # Run with checkpoint every 10 generations
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=15,
        lambda_=30,
        max_generation=30,
        checkpoint_every=10,
        checkpoint_file=CHECKPOINT_DIR / 'periodic_gen{generation}.pkl',
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    print(f"\n✓ Best fitness: {population[0].fitness}")
    print(f"✓ Checkpoints saved every 10 generations in {CHECKPOINT_DIR}/")
    
    # List created checkpoints
    checkpoints = sorted(CHECKPOINT_DIR.glob('periodic_*.pkl'))
    print(f"✓ Created {len(checkpoints)} checkpoint files:")
    for cp in checkpoints:
        print(f"  - {cp.name}")


def example_2_checkpoint_on_improvement():
    """Save checkpoint when finding better solutions"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Checkpoint on Improvement")
    print("="*60)
    
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    # Checkpoint whenever we find a better solution
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=15,
        lambda_=30,
        max_generation=30,
        checkpoint_on_improvement=True,
        checkpoint_file=CHECKPOINT_DIR / 'improvement_gen{generation}.pkl',
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    print(f"\n✓ Best fitness: {population[0].fitness}")
    print(f"✓ Checkpoints saved on each improvement")
    
    # List improvement checkpoints
    checkpoints = sorted(CHECKPOINT_DIR.glob('improvement_*.pkl'))
    print(f"✓ Created {len(checkpoints)} improvement checkpoints")


def example_3_custom_callback():
    """User-controlled checkpointing with callback"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Callback Checkpointing")
    print("="*60)
    
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    checkpoint_count = [0]
    
    def my_checkpoint_callback(pop, gen):
        """Custom callback - you decide when to save!"""
        from byron.tools.checkpoint import save_population, save_individuals
        
        # Save every 5 generations
        if gen > 0 and gen % 5 == 0:
            filename = CHECKPOINT_DIR / f'custom_gen{gen}.pkl'
            save_population(pop, filename)
            checkpoint_count[0] += 1
            print(f"  [Callback] Saved checkpoint at gen {gen}, best: {pop[0].fitness}")
        
        # Save top 5 individuals at generation 15
        if gen == 15:
            save_individuals(pop, CHECKPOINT_DIR / 'top5_gen15.pkl', top_n=5)
            print(f"  [Callback] Saved top 5 individuals at gen {gen}")
    
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=15,
        lambda_=30,
        max_generation=20,
        checkpoint_callback=my_checkpoint_callback,
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    print(f"\n✓ Best fitness: {population[0].fitness}")
    print(f"✓ Made {checkpoint_count[0]} custom checkpoints via callback")


def example_4_load_and_continue():
    """Load a checkpoint and continue evolution"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Load Checkpoint and Continue")
    print("="*60)
    
    from byron.tools.checkpoint import load_population
    
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    checkpoint_file = CHECKPOINT_DIR / 'continuable.pkl'
    
    # Check if we have a checkpoint from previous run
    if checkpoint_file.exists():
        print("📂 Found existing checkpoint - continuing evolution")
        
        # Load the checkpoint
        old_pop = load_population(checkpoint_file)
        print(f"✓ Loaded generation {old_pop.generation}")
        print(f"✓ Previous best: {old_pop[0].fitness}")
        
        # Show what we're continuing from
        starting_gen = old_pop.generation
        print(f"\n🔄 Continuing for 10 more generations...")
        
    else:
        print("🆕 No checkpoint found - starting fresh")
        starting_gen = 0
    
    # Run evolution (either fresh or continuing)
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=15,
        lambda_=30,
        max_generation=10,
        checkpoint_every=5,
        checkpoint_file=checkpoint_file,
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    actual_gen = starting_gen + population.generation
    print(f"\n✓ Actual generation reached: {actual_gen}")
    print(f"✓ Best fitness: {population[0].fitness}")
    print(f"✓ Checkpoint saved to {checkpoint_file}")
    print(f"\n💡 Run this example again to continue from generation {actual_gen}!")


def analyze_checkpoints():
    """Load and analyze saved checkpoints"""
    print("\n" + "="*60)
    print("ANALYZING ALL CHECKPOINTS")
    print("="*60)
    
    from byron.tools.checkpoint import load_population
    
    if not CHECKPOINT_DIR.exists():
        print("No checkpoints directory found!")
        return
    
    checkpoint_files = sorted(CHECKPOINT_DIR.glob('*.pkl'))
    
    if not checkpoint_files:
        print("No checkpoint files found!")
        return
    
    print(f"\nFound {len(checkpoint_files)} checkpoint files:\n")
    
    for cp_file in checkpoint_files[:10]:  # Show first 10
        try:
            pop = load_population(cp_file)
            print(f"📁 {cp_file.name}")
            print(f"   Gen: {pop.generation}, Size: {len(pop)}, Best: {pop[0].fitness}")
        except Exception as e:
            print(f"❌ {cp_file.name}: Error ({e})")
    
    if len(checkpoint_files) > 10:
        print(f"\n... and {len(checkpoint_files) - 10} more checkpoint files")


def main():
    """Run all examples"""
    byron.welcome()
    
    print("\n" + "="*60)
    print("MULTI-SESSION EVOLUTION WITH CHECKPOINTS")
    print("="*60)
    print("\nDemonstrating checkpoint features in simple_ea():")
    print("  • Periodic checkpointing")
    print("  • Checkpoint on improvement")
    print("  • Custom callback control")
    print("  • Combined strategies")
    print()
    
    try:
        example_1_periodic_checkpointing()
        example_2_checkpoint_on_improvement()
        example_3_custom_callback()
        example_4_load_and_continue()
        analyze_checkpoints()
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print(f"✓ Check {CHECKPOINT_DIR}/ for saved checkpoints")
        print("\nTo load a checkpoint:")
        print("  from byron.tools.checkpoint import load_population")
        print("  pop = load_population('checkpoints/periodic_gen10.pkl')")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        print(f"✓ Checkpoints saved in {CHECKPOINT_DIR}/")


if __name__ == "__main__":
    main()
