# Multi-Session Evolution Guide

## Running Evolution Across Multiple Sessions

This guide shows you how to run evolutionary algorithms across multiple sessions with automatic checkpointing. Perfect for long-running experiments, batch jobs, or when you need to stop and resume.

## Quick Start

### Automatic Periodic Checkpointing

```python
import byron

# Checkpoint every 10 generations
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=100,
    checkpoint_every=10,
    checkpoint_file='evolution_gen{generation}.pkl'
)
```

### Checkpoint on Improvement

```python
# Save checkpoint whenever we find a better solution
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=100,
    checkpoint_on_improvement=True,
    checkpoint_file='best_gen{generation}.pkl'
)
```

### Custom User-Controlled Checkpointing

```python
def my_checkpoint_logic(population, generation):
    """You decide when to save!"""
    from byron.tools.checkpoint import save_population
    
    # Example: Save every 20 generations
    if generation % 20 == 0:
        save_population(population, f'checkpoint_gen{generation}.pkl')
    
    # Example: Save when fitness exceeds threshold
    if population[0].fitness > target_threshold:
        save_population(population, f'milestone_{generation}.pkl')
    
    # Example: User input checkpoint
    # (you could check a file, signal, etc.)

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=my_checkpoint_logic
)
```

## Complete Example: Three Sessions

### Session 1: Start Evolution (Day 1)

```python
import byron
from pathlib import Path

# Setup
@byron.fitness_function
def fitness(phenotype):
    return phenotype.count('1')

macro = byron.f.macro('{v}', v=byron.f.array_parameter('01', 100))
top_frame = byron.f.sequence([macro])
evaluator = byron.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)

    # Run 30 generations with checkpoints every 10
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        mu=20,
        lambda_=40,
        max_generation=30,
        checkpoint_every=10,
        checkpoint_file='experiment_gen{generation}.pkl'
    )print(f"Day 1 done: Gen {population.generation}, Best: {population[0].fitness}")
# Checkpoints saved: experiment_gen10.pkl, experiment_gen20.pkl, experiment_gen30.pkl
```

### Session 2: Analyze Progress (Day 2)

```python
from byron.tools.checkpoint import load_population

# Load the latest checkpoint
population = load_population('experiment_gen30.pkl')

print(f"Loaded from generation {population.generation}")
print(f"Best fitness: {population[0].fitness}")
print(f"Population size: {len(population)}")

# Analyze top individuals
for i in range(5):
    ind = population[i]
    print(f"#{i+1}: {ind.fitness} - {ind.describe(include_structure=False)}")
```

### Session 3: Continue Evolution (Day 3)

```python
# ⚠️ IMPORTANT: Current limitation
# You cannot directly resume the SAME evolution with simple_ea
# It always starts a fresh population

# WORKAROUND 1: Start a new run and compare with old results
old_pop = load_population('experiment_gen30.pkl')
print(f"Previous best: {old_pop[0].fitness}")

# Run NEW evolution
new_pop = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=30,
    checkpoint_file='experiment_session2_gen{generation}.pkl'
)

print(f"New run best: {new_pop[0].fitness}")

# WORKAROUND 2: Save best individuals as "hall of fame"
# Use them for analysis, comparison, or seeding future work
```

## Checkpointing Strategies

### Strategy 1: Time-Based Checkpointing

```python
import time

last_checkpoint = [time.time()]

def time_based_checkpoint(population, generation):
    """Checkpoint every 5 minutes"""
    from byron.tools.checkpoint import save_population
    
    current_time = time.time()
    if current_time - last_checkpoint[0] >= 300:  # 5 minutes
        save_population(population, f'time_checkpoint_gen{generation}.pkl')
        last_checkpoint[0] = current_time
        print(f"⏱️  Time-based checkpoint at gen {generation}")

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=time_based_checkpoint
)
```

### Strategy 2: Fitness Milestone Checkpointing

```python
def milestone_checkpoint(population, generation):
    """Save when reaching fitness milestones"""
    from byron.tools.checkpoint import save_population
    
    fitness_val = population[0].fitness.values[0]
    milestones = [50, 75, 90, 95, 99, 100]
    
    for milestone in milestones:
        if fitness_val >= milestone:
            filename = f'milestone_{milestone}_gen{generation}.pkl'
            if not Path(filename).exists():
                save_population(population, filename)
                print(f"🏆 Milestone {milestone} reached at gen {generation}!")
                break

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=milestone_checkpoint
)
```

### Strategy 3: Top-N Individual Tracking

```python
def save_top_individuals(population, generation):
    """Keep track of best individuals throughout evolution"""
    from byron.tools.checkpoint import save_individuals
    
    if generation % 10 == 0:
        # Save top 5 every 10 generations
        save_individuals(
            population,
            f'top5_gen{generation}.pkl',
            top_n=5
        )

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=save_top_individuals
)
```

### Strategy 4: Interactive User-Controlled Checkpointing

```python
import os

def user_triggered_checkpoint(population, generation):
    """Check for user-created trigger file"""
    from byron.tools.checkpoint import save_population
    
    trigger_file = 'SAVE_CHECKPOINT_NOW.trigger'
    
    if os.path.exists(trigger_file):
        save_population(population, f'user_checkpoint_gen{generation}.pkl')
        os.remove(trigger_file)
        print(f"💾 User-triggered checkpoint saved at gen {generation}")

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=user_triggered_checkpoint
)

# In another terminal during evolution:
# $ touch SAVE_CHECKPOINT_NOW.trigger
```

## Managing Checkpoint Files

### Organizing Checkpoints by Experiment

```python
from pathlib import Path
from datetime import datetime

# Create experiment-specific directory
experiment_id = datetime.now().strftime('%Y%m%d_%H%M%S')
checkpoint_dir = Path('experiments') / experiment_id
checkpoint_dir.mkdir(parents=True, exist_ok=True)

# Use organized checkpoint path
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_file=checkpoint_dir / 'gen{generation}.pkl'
)
```

### Cleanup Old Checkpoints

```python
def cleanup_old_checkpoints(population, generation):
    """Keep only the last 3 checkpoints"""
    from byron.tools.checkpoint import save_population
    from pathlib import Path
    
    # Save current
    save_population(population, f'checkpoint_gen{generation}.pkl')
    
    # Remove old ones (keep last 3)
    checkpoints = sorted(Path('.').glob('checkpoint_gen*.pkl'))
    for old_checkpoint in checkpoints[:-3]:
        old_checkpoint.unlink()
        print(f"🗑️  Removed old checkpoint: {old_checkpoint}")

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=cleanup_old_checkpoints
)
```

### Size-Aware Checkpointing

```python
def smart_checkpoint(population, generation):
    """Only checkpoint if population is interesting"""
    from byron.tools.checkpoint import save_individuals
    
    # Save full population periodically
    if generation % 20 == 0:
        save_population(population, f'full_gen{generation}.pkl')
    
    # Save only top individuals more frequently
    elif generation % 5 == 0:
        save_individuals(population, f'top10_gen{generation}.pkl', top_n=10)

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    checkpoint_callback=smart_checkpoint
)
```

## Batch Job Integration

### SLURM Job with Checkpointing

```bash
#!/bin/bash
#SBATCH --job-name=byron_evolution
#SBATCH --time=24:00:00
#SBATCH --mem=8G

# Enable checkpointing
python - <<EOF
import byron

# Setup problem...
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=1000,
    checkpoint_every=50,  # Checkpoint every 50 generations
    checkpoint_file='${SLURM_JOB_ID}_gen{generation}.pkl'
)
EOF
```

### Handling Interruptions

```python
import signal
import sys
from byron.tools.checkpoint import save_population

# Global reference to current population
current_population = None

def signal_handler(signum, frame):
    """Save checkpoint when interrupted"""
    if current_population is not None:
        print("\n⚠️  Interrupted! Saving emergency checkpoint...")
        save_population(current_population, 'emergency_checkpoint.pkl')
        print("✓ Emergency checkpoint saved")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Run evolution
current_population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=1000,
    checkpoint_every=10
)
```

## Best Practices

### ✅ DO:

1. **Use descriptive filenames**
   ```python
   checkpoint_file='experiment_onemax_100bits_gen{generation}.pkl'
   ```

2. **Checkpoint at reasonable intervals**
   - Fast evolution: Every 10-20 generations
   - Slow evolution: Every 1-5 generations
   - Very slow: Every generation

3. **Save metadata alongside checkpoints**
   ```python
   import json
   
   def save_with_metadata(population, generation):
       from byron.tools.checkpoint import save_population
       
       # Save population
       checkpoint = f'gen{generation}.pkl'
       save_population(population, checkpoint)
       
       # Save metadata
       metadata = {
           'generation': generation,
           'best_fitness': str(population[0].fitness),
           'population_size': len(population),
           'timestamp': datetime.now().isoformat()
       }
       with open(f'gen{generation}_meta.json', 'w') as f:
           json.dump(metadata, f, indent=2)
   ```

4. **Test checkpoint loading**
   ```python
   # After saving, immediately test loading
   test_pop = load_population('checkpoint.pkl')
   assert test_pop.generation == population.generation
   ```

### ❌ DON'T:

1. **Don't checkpoint too frequently** - Slows down evolution
2. **Don't forget to clean up** - Disk space can fill quickly
3. **Don't rely on cross-version compatibility** - Document your Byron version
4. **Don't checkpoint without error handling** - Wrap in try/except

## Troubleshooting

### "Cannot resume evolution"
**Problem**: Loaded population doesn't continue where it left off

**Explanation**: `simple_ea()` and `simple_ea()` always create fresh populations. This is by design in the current Byron architecture.

**Solution**: Use checkpoints for:
- Analysis and inspection
- Comparing multiple runs
- Extracting best solutions
- Hall of fame tracking

### "Checkpoint files are too large"
**Problem**: Each checkpoint is hundreds of MB

**Solutions**:
1. Save only top individuals:
   ```python
   save_individuals(pop, 'top10.pkl', top_n=10)
   ```

2. Compress checkpoints:
   ```python
   import gzip
   with gzip.open('checkpoint.pkl.gz', 'wb') as f:
       dill.dump(population, f)
   ```

3. Checkpoint less frequently

### "Checkpoint fails with pickle error"
**Problem**: `AttributeError` or `PicklingError`

**Solution**: Install `dill` for better serialization:
```bash
pip install dill
```

## Running the Example

```bash
cd examples
python multi_session_evolution.py
```

This demonstrates all checkpointing strategies in action!
