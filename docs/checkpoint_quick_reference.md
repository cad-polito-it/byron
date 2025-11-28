# Quick Reference: Checkpointing with simple_ea()

## Yes! You Can Run Multiple Evolutions Across Different Sessions

Byron's `simple_ea()` now supports **automatic checkpointing** so you can:
- ✅ Save progress periodically (time-based or generation-based)
- ✅ Save checkpoints at the end of each generation  
- ✅ Save only when finding improvements
- ✅ Have full user control via callbacks

## Three Ways to Checkpoint

### 1. Automatic Periodic Checkpointing

Save every N generations:

```python
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=1000,
    checkpoint_every=10,  # Save every 10 generations
    checkpoint_file='checkpoint_gen{generation}.pkl'
)
```

**When to use**: Long-running experiments where you want regular snapshots.

### 2. Checkpoint on Improvement

Save only when finding better solutions:

```python
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=1000,
    checkpoint_on_improvement=True,  # Save on each improvement
    checkpoint_file='best_gen{generation}.pkl'
)
```

**When to use**: When you only care about improvements, save disk space.

### 3. User-Controlled with Callback

You decide when to save:

```python
def my_checkpoint_logic(population, generation):
    from byron.tools.checkpoint import save_population
    
    # Example: Save at generations 50, 100, 500, 1000
    if generation in [50, 100, 500, 1000]:
        save_population(population, f'milestone_{generation}.pkl')
    
    # Example: Save every generation
    if True:  # Your condition here
        save_population(population, f'gen_{generation}.pkl')

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=my_checkpoint_logic
)
```

**When to use**: Custom logic, time-based checkpointing, user triggers, complex conditions.

## Checkpoint at End of Each Generation

```python
# Simply checkpoint after every single generation
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=100,
    checkpoint_every=1,  # Every generation!
    checkpoint_file='every_gen_{generation}.pkl'
)
```

**Warning**: Creates many files. Consider cleanup strategy or use callback to overwrite same file.

## User-Dependent Checkpointing

### Option A: Check for User Signal File

```python
import os

def user_triggered_checkpoint(population, generation):
    from byron.tools.checkpoint import save_population
    
    # User creates this file when they want a checkpoint
    trigger_file = 'CHECKPOINT_NOW.trigger'
    
    if os.path.exists(trigger_file):
        save_population(population, f'user_checkpoint_gen{generation}.pkl')
        os.remove(trigger_file)
        print(f"✓ User checkpoint saved at generation {generation}")

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=user_triggered_checkpoint
)
```

**Usage**: While evolution runs, do `touch CHECKPOINT_NOW.trigger` from another terminal.

### Option B: Time-Based Checkpointing

```python
import time

last_checkpoint = [time.time()]

def time_based_checkpoint(population, generation):
    from byron.tools.checkpoint import save_population
    
    current_time = time.time()
    # Checkpoint every 5 minutes
    if current_time - last_checkpoint[0] >= 300:
        save_population(population, f'time_checkpoint_gen{generation}.pkl')
        last_checkpoint[0] = current_time
        print(f"⏱️  Time-based checkpoint at gen {generation}")

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=time_based_checkpoint
)
```

### Option C: Interactive Checkpoint (Keyboard Interrupt Handler)

```python
import signal
import sys

checkpoint_requested = [False]

def request_checkpoint(signum, frame):
    checkpoint_requested[0] = True
    print("\n📌 Checkpoint will be saved at next generation...")

signal.signal(signal.SIGUSR1, request_checkpoint)  # Linux/Mac

def checkpoint_on_request(population, generation):
    from byron.tools.checkpoint import save_population
    
    if checkpoint_requested[0]:
        save_population(population, f'requested_gen{generation}.pkl')
        print(f"✓ Checkpoint saved at generation {generation}")
        checkpoint_requested[0] = False

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=checkpoint_on_request
)
```

**Usage**: Send signal with `kill -SIGUSR1 <pid>` to trigger checkpoint.

## Combine All Strategies

```python
def comprehensive_checkpoint(population, generation):
    from byron.tools.checkpoint import save_population, save_individuals
    
    # Save top 10 every 5 generations
    if generation % 5 == 0:
        save_individuals(population, f'top10_gen{generation}.pkl', top_n=10)
    
    # Save full population every 20 generations
    if generation % 20 == 0:
        save_population(population, f'full_gen{generation}.pkl')
    
    # Check for user trigger file
    if os.path.exists('CHECKPOINT_NOW.trigger'):
        save_population(population, f'user_gen{generation}.pkl')
        os.remove('CHECKPOINT_NOW.trigger')

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_every=50,              # Periodic every 50
    checkpoint_on_improvement=True,   # On improvements
    checkpoint_callback=comprehensive_checkpoint,  # Custom logic
    checkpoint_file='auto_gen{generation}.pkl'
)
```

## Loading Checkpoints

```python
from byron.tools.checkpoint import load_population

# Load saved population
population = load_population('checkpoint_gen100.pkl')

print(f"Generation: {population.generation}")
print(f"Best fitness: {population[0].fitness}")
print(f"Population size: {len(population)}")

# Get best individual's phenotype
best_phenotype = population.dump_individual(0)
print(best_phenotype)
```

## Important Limitation

⚠️ **You cannot directly resume evolution from a checkpoint**

The `simple_ea()` function always creates a **new, fresh population**. Checkpoints are for:
- ✅ Saving best solutions
- ✅ Analysis and inspection
- ✅ Comparing different runs
- ✅ Hall of fame tracking
- ❌ Resuming the exact same evolution

To work around this limitation, you can:
1. Save checkpoints regularly during long runs
2. Analyze checkpoints to extract best individuals
3. Use best individuals as seeds for new runs (requires custom operators)

## Complete Working Example

```python
import byron
from pathlib import Path

# Problem setup
NUM_BITS = 100

@byron.fitness_function  
def fitness(phenotype):
    return phenotype.count('1')

macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', NUM_BITS))
top_frame = byron.f.sequence([macro])
evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)

# Create checkpoint directory
Path('checkpoints').mkdir(exist_ok=True)

# Run with multiple checkpoint strategies
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    mu=30,
    lambda_=60,
    max_generation=100,
    checkpoint_every=10,  # Save every 10 generations
    checkpoint_on_improvement=True,  # Also save on improvements
    checkpoint_file='checkpoints/run_gen{generation}.pkl',
    target_fitness=byron.fitness.make_fitness(NUM_BITS)
)

print(f"✓ Evolution completed!")
print(f"✓ Best fitness: {population[0].fitness}")
print(f"✓ Checkpoints saved in checkpoints/")
```

## See Also

- **`examples/checkpoint_evolution.py`** - Working examples
- **`docs/multi_session_evolution.md`** - Complete guide
- **`docs/checkpointing.md`** - Checkpoint system details

## Summary

**Yes, you can checkpoint your evolution runs!**

- Use `checkpoint_every=1` to save after each generation
- Use `checkpoint_callback` for full user control (time-based, trigger files, etc.)
- Combine multiple strategies for comprehensive checkpointing
- Checkpoints save full population state for later analysis
- Cannot directly resume evolution, but great for tracking progress and saving results
