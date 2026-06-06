import byron
from pathlib import Path
from byron.tools.checkpoint import load_population

CHECKPOINT = Path('demo_checkpoint.pkl')
NUM_BITS = 30

@byron.fitness_function
def fitness(phenotype: str) -> int:
    return phenotype.count('1')

def run_session(session_num):
    # Check starting point
    if CHECKPOINT.exists():
        old_pop = load_population(CHECKPOINT)
        starting_gen = old_pop.generation
        print(f"\n📂 Session {session_num}: Continuing from generation {starting_gen}")
        print(f"   Previous best: {old_pop[0].fitness}")
    else:
        starting_gen = 0
        print(f"\n🆕 Session {session_num}: Starting fresh")
    
    # Run evolution
    macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
    top_frame = byron.f.sequence([macro])
    evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)
    
    pop = byron.ea.simple_ea(
        top_frame, evaluator, mu=10, lambda_=20,
        max_generation=5,
        checkpoint_file=CHECKPOINT,
        checkpoint_every=5,
        target_fitness=byron.fitness.make_fitness(NUM_BITS)
    )
    
    actual_gen = starting_gen + pop.generation
    print(f"✓ Session {session_num} complete: now at generation {actual_gen}, best = {pop[0].fitness}")
    return actual_gen

# Run 3 consecutive sessions
print("="*60)
print("MULTI-SESSION EVOLUTION DEMO")
print("="*60)

gen1 = run_session(1)
gen2 = run_session(2)
gen3 = run_session(3)

print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)
print(f"Session 1: 0 → {gen1}")
print(f"Session 2: {gen1} → {gen2}")  
print(f"Session 3: {gen2} → {gen3}")
print(f"\n✓ Total: {gen3} generations across 3 sessions!")
