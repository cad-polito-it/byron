# Checkpoint Workflow Guide

## How Multi-Session Evolution Works

### The Concept

When you save a checkpoint, you're capturing the **current state** of evolution. When you load it back, you can track where you left off and logically continue across multiple sessions.

```
Session 1:        Gen 0 ──► Gen 10    [Save checkpoint]
                   ↓
Session 2:        [Load checkpoint] ──► Gen 11-20  [Save checkpoint]
                                          ↓
Session 3:                    [Load checkpoint] ──► Gen 21-30
```

### Important: Understanding Generation Tracking

⚠️ **Key Point**: `simple_ea()` always runs from generation 0 to `max_generation` internally. The "continuation" is **logical**, not direct.

**What gets saved in a checkpoint:**
- All individuals with their genomes and fitness values
- Population metadata (generation number, entropy, etc.)
- Problem configuration (top_frame definition)
- Extra parameters

**What does NOT get saved:**
- The evaluator function (can't always pickle functions)
- The evolutionary algorithm state (selection history, etc.)
- Random number generator state

### Three Ways to Use Checkpoints

#### 1. **Periodic Snapshots** (Simplest)
Save at regular intervals to avoid losing work:

```python
population = byron.ea.simple_ea(
    top_frame, evaluator,
    mu=20, lambda_=40,
    max_generation=100,
    checkpoint_every=10,  # Save every 10 generations
    checkpoint_file='evolution_gen{generation}.pkl'
)
```

**Use case:** Long-running experiments where you want to preserve intermediate results.

#### 2. **On-Improvement Checkpoints** 
Save only when finding better solutions:

```python
population = byron.ea.simple_ea(
    top_frame, evaluator,
    mu=20, lambda_=40,
    max_generation=100,
    checkpoint_on_improvement=True,  # Save when fitness improves
    checkpoint_file='best_gen{generation}.pkl'
)
```

**Use case:** Focusing on breakthrough moments, conserving disk space.

#### 3. **User-Controlled Checkpointing**
Complete control via callbacks:

```python
def my_callback(pop, gen):
    from byron.tools.checkpoint import save_population
    
    # Save every hour
    if time.time() - last_save_time > 3600:
        save_population(pop, f'hourly_gen{gen}.pkl')
    
    # Or based on user input, performance metrics, etc.
    if should_save():
        save_population(pop, f'manual_gen{gen}.pkl')

population = byron.ea.simple_ea(
    top_frame, evaluator,
    checkpoint_callback=my_callback,
    # ... other parameters
)
```

**Use case:** Time-based saving, conditional logic, interactive control.

### Multi-Session Evolution Pattern

Here's the recommended pattern for running evolution across multiple sessions:

```python
from byron.tools.checkpoint import load_population, save_population
from pathlib import Path

CHECKPOINT_FILE = Path('my_evolution.pkl')

# Check if we have previous work
if CHECKPOINT_FILE.exists():
    # Load previous state
    old_pop = load_population(CHECKPOINT_FILE)
    starting_gen = old_pop.generation
    print(f"Continuing from generation {starting_gen}")
else:
    starting_gen = 0
    print("Starting fresh evolution")

# Run evolution for N more generations
population = byron.ea.simple_ea(
    top_frame, evaluator,
    mu=20, lambda_=40,
    max_generation=10,  # Run 10 more generations
    checkpoint_file=CHECKPOINT_FILE,
    checkpoint_every=5
)

# Track total progress
actual_generation = starting_gen + population.generation
print(f"You're now at generation {actual_generation}")
```

**Run this script multiple times**, and each time it will:
1. Check for existing checkpoint
2. Load previous generation number
3. Run N more generations
4. Save new checkpoint with updated generation
5. Track cumulative progress

### Practical Examples

#### Example 1: Overnight Runs

```bash
# Monday evening - run for 50 generations
python my_evolution.py --generations 50

# Tuesday morning - continue for 50 more
python my_evolution.py --generations 50

# Wednesday - continue again
python my_evolution.py --generations 50

# Total: 150 generations across 3 sessions
```

#### Example 2: Interactive Checkpointing

```python
import signal
from byron.tools.checkpoint import save_population

def signal_handler(sig, frame):
    print("\n⚠️  Interrupt received - saving checkpoint...")
    save_population(current_population, 'interrupted.pkl')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Now Ctrl+C will save before exiting
population = byron.ea.simple_ea(...)
```

#### Example 3: Batch Processing

```python
# Submit multiple sessions to a cluster
for session in range(10):
    # Each session continues from previous
    if Path(f'checkpoint_session{session-1}.pkl').exists():
        old_pop = load_population(f'checkpoint_session{session-1}.pkl')
        starting_gen = old_pop.generation
    else:
        starting_gen = 0
    
    population = byron.ea.simple_ea(
        top_frame, evaluator,
        max_generation=100,
        checkpoint_file=f'checkpoint_session{session}.pkl'
    )
    
    print(f"Session {session}: Reached generation {starting_gen + 100}")
```

### What You Can Do With Checkpoints

✅ **Analysis**: Load any checkpoint to examine the population at that point
```python
pop = load_population('checkpoint_gen50.pkl')
print(f"Generation {pop.generation}")
print(f"Best: {pop[0].fitness}")
print(f"Entropy: {pop.entropy}")
```

✅ **Comparison**: Compare populations across different checkpoints
```python
pop1 = load_population('checkpoint_gen10.pkl')
pop2 = load_population('checkpoint_gen50.pkl')
print(f"Fitness improvement: {pop2[0].fitness - pop1[0].fitness}")
```

✅ **Extract Solutions**: Get the best individuals from any session
```python
from byron.tools.checkpoint import load_individuals, save_individuals

# Save top 10 from a checkpoint
pop = load_population('checkpoint_gen100.pkl')
save_individuals(pop, 'hall_of_fame.pkl', top_n=10)

# Load them later
data = load_individuals('hall_of_fame.pkl')
for ind in data['individuals']:
    print(f"Solution: {ind.fitness} - {ind}")
```

✅ **Resume After Crash**: If your run crashes, load the last checkpoint
```python
try:
    population = byron.ea.simple_ea(
        top_frame, evaluator,
        max_generation=1000,
        checkpoint_every=10,
        checkpoint_file='backup_gen{generation}.pkl'
    )
except Exception as e:
    print(f"Crashed: {e}")
    print("Loading last checkpoint...")
    pop = load_population('backup_gen990.pkl')  # Last saved
    # Continue from there in next run
```

### Limitations

❌ **Cannot directly resume the same evolution**
- `simple_ea()` always creates a new population internally
- You track progress by remembering the starting generation

❌ **Evaluator must be recreated**
- Functions aren't always pickleable
- You must define the same fitness function when continuing

❌ **No random state preservation**
- Each session uses a different random seed (unless you set it)
- Results won't be identical to a single long run

✅ **But checkpoints are still valuable for**:
- Preventing data loss
- Analyzing evolution progress
- Collecting best solutions
- Multi-session workflows
- Distributed computing

### Best Practices

1. **Use descriptive filenames with generation numbers**
   ```python
   checkpoint_file='myexp_gen{generation}.pkl'
   ```

2. **Keep multiple checkpoints** (not just the latest)
   ```python
   checkpoint_every=10  # Creates gen10.pkl, gen20.pkl, gen30.pkl...
   ```

3. **Track generation across sessions** 
   ```python
   starting_gen = old_pop.generation if checkpoint else 0
   actual_gen = starting_gen + new_pop.generation
   ```

4. **Save best individuals separately**
   ```python
   save_individuals(pop, 'best_ever.pkl', top_n=5)
   ```

5. **Use version control for experiment scripts**
   - Keep your problem definition consistent across sessions
   - Document any changes to parameters

## See Also

- [Checkpoint Quick Reference](checkpoint_quick_reference.md) - Basic usage examples
- [Multi-Session Evolution Guide](multi_session_evolution.md) - Detailed patterns
- `examples/multi_session_evolution.py` - Working example script
- `examples/checkpoint_evolution.py` - Various checkpoint strategies
