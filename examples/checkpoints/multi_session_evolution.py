#!/usr/bin/env python3
"""
Real Multi-Session Evolution: Load and Continue

This example shows how to actually USE a saved checkpoint to continue evolution.
You can run this script multiple times, and each time it will continue from where
it left off!
"""

import byron
from pathlib import Path
from byron.tools.checkpoint import load_population, save_population

NUM_BITS = 50
CHECKPOINT_FILE = Path('multi_session_checkpoint.pkl')


@byron.fitness_function
def fitness(phenotype: str) -> int:
    """OneMax: count the number of '1's"""
    return phenotype.count('1')


def get_problem_definition():
    """Returns the problem definition - must be consistent across sessions!"""
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    return top_frame, evaluator


def run_session(generations_per_session=10):
    """Run one session - either starting fresh or continuing from checkpoint"""
    
    top_frame, evaluator = get_problem_definition()
    
    # Check if we have a checkpoint
    if CHECKPOINT_FILE.exists():
        print("\n" + "="*60)
        print("📂 CHECKPOINT FOUND - CONTINUING EVOLUTION")
        print("="*60)
        
        # Load previous population
        old_pop = load_population(CHECKPOINT_FILE)
        
        print(f"✓ Loaded from generation {old_pop.generation}")
        print(f"✓ Best fitness so far: {old_pop[0].fitness}")
        print(f"✓ Population size: {len(old_pop)}")
        
        # Display best individual
        print(f"\nBest individual so far:")
        print(f"  Fitness: {old_pop[0].fitness}")
        print(f"  Age: {old_pop[0].age}")
        print(f"  Phenotype sample: {old_pop.dump_individual(0)[:50]}...")
        
        starting_gen = old_pop.generation
        total_gens = starting_gen + generations_per_session
        
        print(f"\n🔄 Continuing for {generations_per_session} more generations")
        print(f"   Target: generation {total_gens}")
        
    else:
        print("\n" + "="*60)
        print("🆕 NO CHECKPOINT - STARTING FRESH EVOLUTION")
        print("="*60)
        
        starting_gen = 0
        total_gens = generations_per_session
        
        print(f"Starting new evolution for {generations_per_session} generations")
    
    # Track improvements across sessions
    session_callback_data = {'improvements': 0, 'starting_gen': starting_gen}
    
    def session_callback(pop, gen):
        """Track progress during this session"""
        # Show progress every 5 generations
        if gen % 5 == 0 and gen > 0:
            actual_gen = starting_gen + gen
            print(f"  Gen {actual_gen}: Best = {pop[0].fitness}, Entropy = {pop.entropy:.3f}")
    
    # Run evolution
    print(f"\n▶️  Running evolution...")
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=20,
        lambda_=40,
        max_generation=generations_per_session,
        checkpoint_every=5,
        checkpoint_file=CHECKPOINT_FILE,
        checkpoint_callback=session_callback,
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    # Show session summary
    actual_final_gen = starting_gen + population.generation
    print(f"\n" + "="*60)
    print(f"✓ SESSION COMPLETE")
    print("="*60)
    print(f"Actual generation: {actual_final_gen}")
    print(f"Best fitness: {population[0].fitness}")
    print(f"Checkpoint saved: {CHECKPOINT_FILE}")
    
    if CHECKPOINT_FILE.exists():
        print(f"\n💡 To continue evolution, run this script again!")
        print(f"   Each run adds {generations_per_session} more generations.")
    
    return population


def show_checkpoint_history():
    """Show evolution history from checkpoint"""
    print("\n" + "="*60)
    print("📊 CHECKPOINT HISTORY")
    print("="*60)
    
    if not CHECKPOINT_FILE.exists():
        print("No checkpoint file found yet.")
        return
    
    pop = load_population(CHECKPOINT_FILE)
    print(f"\nCurrent State:")
    print(f"  Generation: {pop.generation}")
    print(f"  Population size: {len(pop)}")
    print(f"  Best fitness: {pop[0].fitness}")
    print(f"  Average fitness: {sum(pop[i].fitness for i in range(len(pop))) / len(pop):.2f}")
    print(f"  Entropy: {pop.entropy:.4f}")
    
    print(f"\nTop 5 individuals:")
    for i in range(min(5, len(pop))):
        ind = pop[i]
        print(f"  #{i+1}: {ind.fitness} (age: {ind.age})")


def main():
    """Main entry point"""
    byron.welcome()
    
    print("\n" + "="*60)
    print("MULTI-SESSION EVOLUTION DEMO")
    print("="*60)
    print("\nThis script demonstrates REAL checkpoint continuation:")
    print("• Run it once: starts fresh evolution (10 generations)")
    print("• Run it again: loads checkpoint and continues (10 more)")
    print("• Keep running: keeps adding generations!")
    print()
    
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--reset':
            if CHECKPOINT_FILE.exists():
                CHECKPOINT_FILE.unlink()
                print("✓ Checkpoint deleted. Starting fresh next run.\n")
            else:
                print("No checkpoint to delete.\n")
            return
        elif sys.argv[1] == '--status':
            show_checkpoint_history()
            return
        elif sys.argv[1] == '--help':
            print("Usage:")
            print("  python multi_session_evolution.py          # Run one session")
            print("  python multi_session_evolution.py --reset  # Delete checkpoint")
            print("  python multi_session_evolution.py --status # Show checkpoint info")
            return
    
    # Run one session
    try:
        population = run_session(generations_per_session=10)
        show_checkpoint_history()
        
        print("\n" + "="*60)
        print("✓ Run complete!")
        print("="*60)
        print("\nNext steps:")
        print("• Run again to continue evolution")
        print("• Use --status to see current state")
        print("• Use --reset to start over")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        if CHECKPOINT_FILE.exists():
            print(f"✓ Progress saved in {CHECKPOINT_FILE}")
            print("✓ Run again to continue from where you left off")


if __name__ == "__main__":
    main()
