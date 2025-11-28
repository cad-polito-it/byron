#!/usr/bin/env python3
"""
REAL WORLD CHECKPOINT USAGE

This example demonstrates the actual workflow for using checkpoints
to continue evolution across multiple sessions.

KEY CONCEPTS:
1. Checkpoints save population state (generation, individuals, fitness)
2. Loading checkpoint tells you which generation you reached
3. You run MORE generations, tracking cumulative progress
4. Each session adds to the total generation count

This is perfect for:
- Long-running experiments that exceed available time
- Resuming after interruptions/crashes
- Incremental evolution on cluster/cloud with time limits
- Interactive evolution where you check progress and continue
"""

import byron
from pathlib import Path
from byron.tools.checkpoint import load_population, save_population

# Configuration
NUM_BITS = 50
CHECKPOINT = Path('real_world_checkpoint.pkl')
GENERATIONS_PER_SESSION = 15


@byron.fitness_function
def fitness(phenotype: str) -> int:
    """OneMax: count '1's in bitstring"""
    return phenotype.count('1')


def get_starting_point():
    """Load checkpoint if exists, otherwise start fresh"""
    if CHECKPOINT.exists():
        print("📂 Found checkpoint - loading previous work...")
        old_pop = load_population(CHECKPOINT)
        
        print(f"\n   Previous Session Summary:")
        print(f"   ├─ Generation reached: {old_pop.generation}")
        print(f"   ├─ Best fitness: {old_pop[0].fitness}")
        print(f"   ├─ Population size: {len(old_pop)}")
        print(f"   └─ Entropy: {old_pop.entropy:.4f}")
        
        return old_pop.generation, old_pop[0].fitness
    else:
        print("🆕 No checkpoint found - starting fresh evolution")
        return 0, None


def run_session():
    """Run one session of evolution"""
    
    # Check where we left off
    starting_gen, previous_best = get_starting_point()
    
    # Setup problem (must match original definition!)
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    # Calculate target
    target_gen = starting_gen + GENERATIONS_PER_SESSION
    
    print(f"\n▶️  Running Evolution Session")
    print(f"   ├─ Starting from: generation {starting_gen}")
    print(f"   ├─ Running for: {GENERATIONS_PER_SESSION} generations")
    print(f"   └─ Will reach: generation {target_gen}")
    print()
    
    # Track progress during run
    progress_callback_data = {'starting': starting_gen, 'last_report': 0}
    
    def progress_tracker(pop, gen):
        """Show progress updates"""
        actual_gen = progress_callback_data['starting'] + gen
        if gen % 5 == 0 and gen != progress_callback_data['last_report']:
            print(f"   Gen {actual_gen:3d}: Best={pop[0].fitness}, "
                  f"Entropy={pop.entropy:.3f}")
            progress_callback_data['last_report'] = gen
    
    # Run the evolution
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=20,
        lambda_=40,
        max_generation=GENERATIONS_PER_SESSION,
        checkpoint_file=CHECKPOINT,
        checkpoint_every=5,  # Save every 5 generations
        checkpoint_callback=progress_tracker,
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    # Calculate actual cumulative generation
    actual_generation = starting_gen + population.generation
    
    # Show session results
    print(f"\n✅ Session Complete!")
    print(f"   ├─ Cumulative generation: {actual_generation}")
    print(f"   ├─ Current best fitness: {population[0].fitness}")
    
    if previous_best is not None:
        improvement = population[0].fitness.values[0] - previous_best.values[0]
        if improvement > 0:
            print(f"   ├─ Improvement this session: +{improvement}")
        else:
            print(f"   ├─ No improvement (was {previous_best})")
    
    print(f"   └─ Checkpoint saved to: {CHECKPOINT}")
    
    return actual_generation, population


def show_history():
    """Display evolution history from checkpoint"""
    if not CHECKPOINT.exists():
        print("\n⚠️  No checkpoint file found yet")
        print("   Run this script to create one!")
        return
    
    pop = load_population(CHECKPOINT)
    
    print("\n" + "="*60)
    print("📊 EVOLUTION HISTORY")
    print("="*60)
    print(f"\nTotal generations completed: {pop.generation}")
    print(f"Best fitness achieved: {pop[0].fitness}")
    print(f"Population diversity (entropy): {pop.entropy:.4f}")
    
    print(f"\n🏆 Top 5 Individuals:")
    for i in range(min(5, len(pop))):
        ind = pop[i]
        print(f"   {i+1}. Fitness: {ind.fitness:3s} │ Age: {ind.age:3d} │ "
              f"ID: {ind.id}")
    
    print(f"\n💡 To continue evolution, run this script again!")
    print(f"   Each run adds {GENERATIONS_PER_SESSION} more generations")


def main():
    """Main entry point"""
    import sys
    
    byron.welcome()
    
    print("\n" + "="*60)
    print("REAL WORLD CHECKPOINT USAGE EXAMPLE")
    print("="*60)
    
    # Handle command-line options
    if len(sys.argv) > 1:
        if sys.argv[1] == '--reset':
            if CHECKPOINT.exists():
                CHECKPOINT.unlink()
                print("✓ Checkpoint deleted. Next run will start fresh.\n")
            else:
                print("No checkpoint to delete.\n")
            return
        
        elif sys.argv[1] == '--status':
            show_history()
            return
        
        elif sys.argv[1] == '--help':
            print("\nUsage:")
            print("  python real_world_checkpoints.py           # Run one session")
            print("  python real_world_checkpoints.py --reset   # Delete checkpoint")
            print("  python real_world_checkpoints.py --status  # Show history")
            print()
            return
    
    # Run one evolution session
    try:
        final_gen, population = run_session()
        
        print("\n" + "="*60)
        print("WHAT NEXT?")
        print("="*60)
        print(f"\n✓ You've completed {final_gen} total generations")
        print("\n📋 Options:")
        print("   1. Run this script again to continue evolution")
        print("   2. Use --status to see current state")
        print("   3. Use --reset to start over from scratch")
        print("   4. Load checkpoint in Python to analyze results:")
        print(f"\n      from byron.tools.checkpoint import load_population")
        print(f"      pop = load_population('{CHECKPOINT}')")
        print(f"      print(pop[0].fitness)  # Best solution")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Evolution interrupted!")
        if CHECKPOINT.exists():
            print(f"✓ Progress saved to {CHECKPOINT}")
            print("✓ Run again to continue from where you left off")
        sys.exit(0)


if __name__ == "__main__":
    main()
