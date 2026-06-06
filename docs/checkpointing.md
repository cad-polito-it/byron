# Population Checkpointing in Byron

This guide explains how to save and load populations in Byron, enabling you to:
- Resume interrupted evolution runs
- Save best solutions for later analysis
- Create checkpoints during long runs
- Export and share evolved populations

## Table of Contents
- [What is Pickle?](#what-is-pickle)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)
- [Limitations](#limitations)

---

## What is Pickle?

**Pickle** is Python's built-in serialization module that saves Python objects to disk and loads them back.

### How it works:
```
Python Object  ──pickle──>  Binary File  ──unpickle──>  Python Object
  (in memory)               (on disk)                    (in memory)
```

### What gets saved:
When you pickle a Byron `Population`, it saves:
- ✅ All individuals with their complete genomes (NetworkX graphs)
- ✅ Fitness values for each individual  
- ✅ Generation counter and population metadata
- ✅ Age and lineage information
- ✅ Population configuration and parameters

### What doesn't get saved:
- ❌ The evaluator function (must be recreated)
- ⚠️ The top_frame definition (stored as reference, may not unpickle across sessions)
- ❌ Operator configurations (must be recreated)

**Important**: Due to Python's pickle limitations with dynamically created classes (closures), the `top_frame` reference in saved populations may not always unpickle correctly in new Python sessions. The population and individuals still save correctly, but you may need to recreate the `top_frame` separately.

### Important notes:
- 🔒 **Security**: Only unpickle files from trusted sources (pickle can execute arbitrary code)
- 🐍 **Python version**: Use the same Python version to save and load
- 📦 **Dependencies**: NetworkX and other dependencies must match

---

## Quick Start

### Save a population
```python
import byron
from byron.tools.checkpoint import save_population

# Run your evolution
population = byron.ea.simple_ea(top_frame, evaluator, max_generation=100)

# Save it
save_population(population, 'my_checkpoint.pkl')
```

### Load a population
```python
from byron.tools.checkpoint import load_population

# Load it back
population = load_population('my_checkpoint.pkl')

# Inspect the results
print(f"Generation: {population.generation}")
print(f"Best fitness: {population[0].fitness}")
```

---

## API Reference

### `save_population(population, filepath)`
Save an entire population to disk.

**Parameters:**
- `population` (Population): The population to save
- `filepath` (str | Path): Where to save (recommend .pkl extension)

**Example:**
```python
save_population(population, 'checkpoint_gen100.pkl')
```

---

### `load_population(filepath)`
Load a population from disk.

**Parameters:**
- `filepath` (str | Path): Path to the saved population file

**Returns:**
- `Population`: The loaded population object

**Example:**
```python
population = load_population('checkpoint_gen100.pkl')
```

---

### `save_individuals(population, filepath, indices=None, top_n=None)`
Save specific individuals from a population.

**Parameters:**
- `population` (Population): Source population
- `filepath` (str | Path): Where to save
- `indices` (list[int], optional): Specific indices to save
- `top_n` (int, optional): Save only top N fittest individuals

**Examples:**
```python
# Save top 10 individuals
save_individuals(population, 'top10.pkl', top_n=10)

# Save specific individuals
save_individuals(population, 'selected.pkl', indices=[0, 5, 10])

# Save all individuals (with metadata)
save_individuals(population, 'all.pkl')
```

---

### `load_individuals(filepath)`
Load individuals from a checkpoint file.

**Parameters:**
- `filepath` (str | Path): Path to saved individuals

**Returns:**
- `dict`: Dictionary with keys:
  - `'individuals'`: List of Individual objects
  - `'generation'`: Generation when saved
  - `'top_frame'`: The top frame used
  - `'population_extra_parameters'`: Population parameters
  - `'num_saved'`: Number of saved individuals
  - `'total_population_size'`: Original population size

**Example:**
```python
data = load_individuals('top10.pkl')
print(f"Loaded {data['num_saved']} individuals")
best = data['individuals'][0]
print(f"Best fitness: {best.fitness}")
```

---

## Usage Examples

### Example 1: Periodic Checkpointing

Save checkpoints during a long evolution run:

```python
import byron
from byron.tools.checkpoint import save_population

# Define your problem
top_frame = byron.f.sequence([...])
evaluator = byron.evaluator.PythonEvaluator(fitness_function)

# Run evolution with periodic saves
for run in range(10):
    population = byron.ea.simple_ea(
        top_frame,
        evaluator,
        max_generation=100,
        mu=20,
        lambda_=40
    )
    
    # Save checkpoint after each run
    save_population(population, f'checkpoint_run{run}.pkl')
    print(f"Run {run}: Best fitness = {population[0].fitness}")
```

### Example 2: Hall of Fame

Collect best individuals from multiple runs:

```python
from byron.tools.checkpoint import save_individuals, load_individuals

hall_of_fame = []

# Run evolution multiple times
for trial in range(5):
    population = byron.ea.simple_ea(top_frame, evaluator, max_generation=100)
    
    # Save top 3 from this trial
    save_individuals(population, f'trial_{trial}_top3.pkl', top_n=3)
    
    # Add to hall of fame
    hall_of_fame.extend(population.individuals[:3])

# Save combined hall of fame
save_individuals(
    population,  # Use last population for metadata
    'hall_of_fame.pkl',
    indices=list(range(len(hall_of_fame)))
)
```

### Example 3: Resume After Interruption

```python
import os
from byron.tools.checkpoint import save_population, load_population

checkpoint_file = 'evolution_checkpoint.pkl'

# Check if we have a checkpoint
if os.path.exists(checkpoint_file):
    print("Resuming from checkpoint...")
    population = load_population(checkpoint_file)
    start_generation = population.generation
    print(f"Resuming from generation {start_generation}")
else:
    print("Starting fresh evolution...")
    # Note: Cannot directly continue with simple_ea()
    # This is for analysis/seeding purposes

# For new run, recreate everything
top_frame = byron.f.sequence([...])
evaluator = byron.evaluator.PythonEvaluator(fitness_function)

population = byron.ea.simple_ea(
    top_frame,
    evaluator,
    max_generation=1000
)

# Save at the end
save_population(population, checkpoint_file)
```

### Example 4: Analyze Offline

Save population and analyze later without running Byron:

```python
# Save during evolution
save_population(population, 'final_population.pkl')

# Later, in a different script/session:
from byron.tools.checkpoint import load_population

population = load_population('final_population.pkl')

# Analyze without rerunning evolution
print(f"Population size: {len(population)}")
print(f"Generation: {population.generation}")

# Export phenotypes
for i, individual in enumerate(population[:10]):
    phenotype = population.dump_individual(i)
    with open(f'solution_{i}.txt', 'w') as f:
        f.write(phenotype)
```

---

## Best Practices

### ✅ DO:

1. **Use descriptive filenames** with generation/timestamp:
   ```python
   save_population(population, f'pop_gen{population.generation}_fitness{population[0].fitness}.pkl')
   ```

2. **Save periodically** during long runs:
   ```python
   if population.generation % 100 == 0:
       save_population(population, f'checkpoint_gen{population.generation}.pkl')
   ```

3. **Compress large checkpoints** (optional):
   ```python
   import gzip
   import pickle
   
   with gzip.open('population.pkl.gz', 'wb') as f:
       pickle.dump(population, f)
   ```

4. **Version your problem definitions** alongside checkpoints:
   ```python
   # Save problem config too
   config = {
       'top_frame': top_frame,
       'mu': 10,
       'lambda_': 20,
       'date': datetime.now()
   }
   with open('config.pkl', 'wb') as f:
       pickle.dump(config, f)
   ```

### ❌ DON'T:

1. **Don't unpickle untrusted files** - security risk
2. **Don't expect to continue evolution directly** - simple_ea() creates fresh populations
3. **Don't rely on cross-version compatibility** - pickle is version-sensitive
4. **Don't forget to save the evaluator code separately** - functions may not pickle well

---

## Limitations

### Cannot Resume Evolution Directly

The current `simple_ea()` and `adaptive_ea()` functions **always create a fresh population**. Loaded populations can be used for:
- ✅ Analysis and inspection
- ✅ Extracting best solutions
- ✅ Seeding new runs (manually)
- ❌ Direct continuation of evolution (requires EA modification)

### To Resume Evolution:

**Option 1**: Modify `simple_ea()` to accept `initial_population` parameter:
```python
def simple_ea(
    top_frame,
    evaluator,
    initial_population=None,  # Add this parameter
    mu=10,
    lambda_=20,
    max_generation=100,
    ...
):
    if initial_population is None:
        # Create fresh population (current behavior)
        population = Population(top_frame, ...)
        # ... initialize ...
    else:
        # Use provided population
        population = initial_population
    
    # Continue with evolution loop...
```

**Option 2**: Extract genomes and use as seeds:
```python
# Load previous best
old_pop = load_population('checkpoint.pkl')
best_genome = old_pop[0].genome

# Use as inspiration in new operators
# (requires custom initialization operators)
```

### What Can Be Pickled

**Typically works:**
- NetworkX graphs ✅
- NumPy arrays ✅
- Basic Python types (int, str, list, dict) ✅
- Byron Individual and Population objects ✅

**May not work:**
- Lambda functions ❌
- Local/nested functions ❌  
- Objects with file handles ❌
- Some custom classes without `__getstate__` ❌

---

## Troubleshooting

### "AttributeError" when loading
**Problem**: Byron version mismatch or missing dependencies

**Solution**: 
```python
# Check versions match
import byron
print(byron.__version__)
```

### Large file sizes
**Problem**: Checkpoints are too large

**Solution**: Save only top individuals:
```python
save_individuals(population, 'top10.pkl', top_n=10)
```

Or compress:
```python
import gzip
with gzip.open('checkpoint.pkl.gz', 'wb') as f:
    pickle.dump(population, f)
```

### Cannot continue evolution
**Problem**: `simple_ea()` doesn't accept existing populations

**Solution**: This is by design. Use checkpoints for analysis and seeding, not direct resumption. To truly resume, you need to modify the EA functions (see [Limitations](#limitations)).

---

## See Also

- `examples/checkpoint_example.py` - Complete working examples
- Byron documentation: https://cad-polito-it.github.io/byron/
- Python pickle docs: https://docs.python.org/3/library/pickle.html
