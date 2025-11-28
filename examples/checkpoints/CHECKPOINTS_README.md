# Checkpoint Examples

This directory contains examples demonstrating how to use Byron's checkpoint system to save and load populations across evolution sessions.

## Quick Start

The **simplest** way to understand checkpoints:

```bash
# Run this multiple times - each time continues from previous session!
python multi_session_evolution.py
```

## Examples Overview

### 1. `multi_session_evolution.py` ⭐ **START HERE**
**The main example** - shows real multi-session evolution.

Run it multiple times. Each run:
- Loads the previous checkpoint (if exists)
- Runs 10 more generations
- Saves updated checkpoint
- Shows cumulative progress

```bash
# First run: generations 0-10
python multi_session_evolution.py

# Second run: continues to generation 20
python multi_session_evolution.py

# Third run: continues to generation 30
python multi_session_evolution.py
```

**Commands:**
- `python multi_session_evolution.py` - Run one session
- `python multi_session_evolution.py --status` - Show current progress
- `python multi_session_evolution.py --reset` - Start over

---

### 2. `real_world_checkpoints.py`
**Production-ready** checkpoint pattern with progress tracking.

Features:
- ✓ Detailed progress reports
- ✓ Shows session summaries
- ✓ Tracks cumulative generations
- ✓ Compares improvements
- ✓ Command-line interface

```bash
python real_world_checkpoints.py         # Run session (15 gens)
python real_world_checkpoints.py --status # Show history
python real_world_checkpoints.py --reset  # Delete checkpoint
```

---

### 3. `checkpoint_evolution.py`
**Demonstrates all checkpoint strategies** in `simple_ea()`:

- **Example 1**: Periodic checkpointing (every N generations)
- **Example 2**: Checkpoint on fitness improvement
- **Example 3**: Custom callback control
- **Example 4**: Load checkpoint and continue

```bash
python checkpoint_evolution.py
```

Run example 4 multiple times to see continuation!

---

### 4. `checkpoint_example.py`
**Low-level checkpoint API** demonstration.

Shows how to use checkpoint functions directly:
- `save_population()` / `load_population()`
- `save_individuals()` / `load_individuals()`
- Creating populations from saved individuals
- Analyzing checkpoint files

```bash
python checkpoint_example.py
```

---

## Key Concepts

### What Gets Saved in a Checkpoint?

✅ **Saved:**
- All individuals (genomes + fitness values)
- Generation number
- Population metadata (entropy, size, etc.)
- Problem definition (top_frame structure)

❌ **NOT Saved:**
- Evaluator function (recreate this yourself)
- Random state (different runs = different randomness)
- Evolution algorithm internal state

### How Continuation Works

```python
# Load checkpoint to see where you stopped
old_pop = load_population('checkpoint.pkl')
starting_gen = old_pop.generation  # e.g., 50

# Run MORE generations
new_pop = byron.ea.simple_ea(..., max_generation=20)

# Track cumulative progress
actual_gen = starting_gen + new_pop.generation  # 50 + 20 = 70
```

**Important:** `simple_ea()` always runs from its own generation 0 to `max_generation`. The checkpoint tells you where you *previously* stopped, so you can track cumulative progress.

### Three Checkpoint Strategies

#### Strategy 1: Periodic (every N generations)
```python
byron.ea.simple_ea(
    ...,
    checkpoint_every=10,
    checkpoint_file='periodic_gen{generation}.pkl'
)
```

#### Strategy 2: On Improvement
```python
byron.ea.simple_ea(
    ...,
    checkpoint_on_improvement=True,
    checkpoint_file='best_gen{generation}.pkl'
)
```

#### Strategy 3: Custom Callback
```python
def my_callback(pop, gen):
    if should_save(gen):
        save_population(pop, f'custom_gen{gen}.pkl')

byron.ea.simple_ea(
    ...,
    checkpoint_callback=my_callback
)
```

## Common Use Cases

### Use Case 1: Resume After Crash
```python
# Run with periodic checkpoints
population = byron.ea.simple_ea(
    ...,
    checkpoint_every=5,
    checkpoint_file='backup_gen{generation}.pkl'
)

# If it crashes, load last checkpoint:
pop = load_population('backup_gen45.pkl')
# Continue from generation 45 in next run
```

### Use Case 2: Overnight Sessions
```bash
# Monday night: run 50 generations
python my_evolution.py --generations 50

# Tuesday night: continue for 50 more
python my_evolution.py --generations 50

# Total: 100 generations across sessions
```

### Use Case 3: Cluster Jobs with Time Limits
```python
# Each job runs 100 generations, saves checkpoint
# Next job loads checkpoint and continues
while not converged:
    submit_job("python evolve.py --continue-from checkpoint.pkl")
```

### Use Case 4: Interactive Evolution
```python
# Run, check results, decide whether to continue
pop = load_population('checkpoint.pkl')
print(f"Best fitness: {pop[0].fitness}")

if input("Continue? ") == 'y':
    # Run more generations
    ...
```

## API Reference

### Save/Load Full Population

```python
from byron.tools.checkpoint import save_population, load_population

# Save entire population
save_population(population, 'my_checkpoint.pkl')

# Load it back
pop = load_population('my_checkpoint.pkl')
print(f"Loaded gen {pop.generation}, best: {pop[0].fitness}")
```

### Save/Load Specific Individuals

```python
from byron.tools.checkpoint import save_individuals, load_individuals

# Save top 10 individuals
save_individuals(population, 'hall_of_fame.pkl', top_n=10)

# Or specific indices
save_individuals(population, 'selected.pkl', indices=[0, 5, 10])

# Load them back
data = load_individuals('hall_of_fame.pkl')
print(f"Loaded {len(data['individuals'])} individuals")
for ind in data['individuals']:
    print(f"  {ind.fitness}")
```

### Using Checkpoints in simple_ea

```python
population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    mu=20,
    lambda_=40,
    max_generation=100,
    
    # Checkpoint every 10 generations
    checkpoint_every=10,
    
    # Also checkpoint on improvement
    checkpoint_on_improvement=True,
    
    # Filename template ({generation} replaced automatically)
    checkpoint_file='exp_gen{generation}.pkl',
    
    # Custom callback for additional control
    checkpoint_callback=my_callback_function
)
```

## Troubleshooting

### Problem: "Can't pickle function"

**Solution:** Install `dill` for better serialization:
```bash
pip install dill
```

Byron automatically uses dill if available.

### Problem: "Cannot resume evolution directly"

**Explanation:** `simple_ea()` always creates a fresh population. You track continuation by:
1. Loading checkpoint to get previous generation number
2. Running more generations with a new call to `simple_ea()`
3. Tracking cumulative progress manually

See `multi_session_evolution.py` for the pattern.

### Problem: Different results after loading checkpoint

**Expected behavior:** Each `simple_ea()` call uses different random seeds unless you set them explicitly. Checkpoints preserve individuals, not randomness.

## Best Practices

1. **Use descriptive filenames** with generation numbers:
   ```python
   checkpoint_file='experiment_onemax_gen{generation}.pkl'
   ```

2. **Keep multiple checkpoints**, not just the latest:
   ```python
   checkpoint_every=10  # Creates separate files
   ```

3. **Track cumulative generations** across sessions:
   ```python
   total_gen = previous_gen + current_gen
   ```

4. **Save best individuals separately**:
   ```python
   save_individuals(pop, 'best_solutions.pkl', top_n=5)
   ```

5. **Version control your scripts** so problem definitions stay consistent

## See Also

- `../docs/checkpoint_workflow.md` - Detailed workflow guide
- `../docs/checkpoint_quick_reference.md` - Quick API reference
- `../docs/multi_session_evolution.md` - Comprehensive multi-session patterns
- `../src/byron/tools/checkpoint.py` - Source code

## Quick Comparison

| Example | Best For | Complexity | Key Feature |
|---------|----------|------------|-------------|
| `multi_session_evolution.py` | **Getting started** | Simple | Automatic continuation |
| `real_world_checkpoints.py` | **Production use** | Medium | Progress tracking |
| `checkpoint_evolution.py` | **Learning strategies** | Medium | All checkpoint methods |
| `checkpoint_example.py` | **API details** | Advanced | Low-level functions |

**Recommendation:** Start with `multi_session_evolution.py`, then check `real_world_checkpoints.py` for production patterns!
