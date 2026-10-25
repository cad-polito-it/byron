# Known bugs

This list was compiled by reviewing the source code of `src/byron` and reproducing each problem with small scripts. It refers to commit `52ae016` (branch `exp/squillero`), tested on Python 3.15.1 and 3.14.9 with the dependencies locked in `uv.lock`. Line numbers refer to that commit. Unless noted otherwise, a problem occurs both with and without `-O`.

Severity levels:

- **Critical**: crashes or corrupts a run of the main EAs with default settings or documented options, on common grammars.
- **High**: a documented feature is unusable or silently wrong.
- **Medium**: wrong behavior in specific situations, usually with a workaround.
- **Low**: minor defects, dead code, misleading documentation, cosmetic or performance issues.

## Critical

### C1. Crossovers delete and copy nodes outside the chosen subtree

**Where:** `src/byron/operators/crossovers.py` lines 198, 206, 225 (in `bunch_onepoint_crossover`) and 304, 308, 328 (in `subtree_crossover`).

**What happens:** Both operators collect "the subtree" with `nx.dfs_preorder_nodes` on the whole genome, which also follows `LINK` edges. Removing a subtree therefore also deletes the targets of its structural references, such as sibling instructions that should have been kept. Copying a subtree from the second parent also copies whatever its references point to. Copied `LINK` edges lose their keys, so the references they belonged to come out unset.

On a bunch of instructions with local jumps, 297 of 400 calls to `bunch_onepoint_crossover` raised `NetworkXError` ("node … is not in the digraph") or the paranoia `AssertionError` in `set_successors_order` (`src/byron/tools/graph.py:92`), and only 2 produced a valid offspring. Neither exception is `ByronOperatorFailure`, so it escapes the operator and stops `simple_ea`, with or without `-O`. On the same grammar, `subtree_crossover` never produced a valid offspring (400 aborts). On a grammar with global references, it produced 13 valid offspring out of 400. All registered crossovers are used by default, so any run on an assembly-like grammar with jumps crashes within the first generations. The crossover test was disabled in commit `ec29652`.

**Reproduce:** run `simple_ea` on `sequence([bunch([macro('add {r}', r=...), macro('jmp {t}', t=local_reference())], size=(6, 20))])`.

**Fix:** collect subtrees on the structure tree only (`FRAMEWORK` edges, for example through `get_structure`), copy edges with their keys (`out_edges(..., keys=True, data=True)`), and remap or drop references that leave the copied subtree.

### C2. `simple_ea` and `topk_tournament_ea` crash without `target_fitness`

**Where:** `src/byron/ea/estimator.py:82-83`.

**What happens:** `Estimator.__init__` computes `fitness.__class__(fitness * temperature)`. With the default `target_fitness=None`, this raises `TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'` before generation 0. `examples/classics/knapsack.py` fails this way.

**Fix:** set `_near = None` when no target is given; `strength()` already handles `None`.

### C3. `lifespan` makes the EAs crash with `ReferenceError`

**Where:** the fitness setter in `src/byron/classes/individual.py:266-273`, `src/byron/registry.py:180`, `src/byron/ea/simple_ea.py:285` and `src/byron/ea/topk_tournament_ea.py:295`.

**What happens:** The lineage stores parents as `weakref.proxy` objects. The EAs call `population.life_cycle()` after creating the offspring but before evaluating them, so parents that age out are freed. When the evaluator assigns the offspring's fitness, the setter reads `parent.fitness` through the dead proxy and raises `ReferenceError: weakly-referenced object no longer exists`. Reproduced with `simple_ea(..., lifespan=1)`; `examples/classics/knapsack.py` uses `lifespan=2`.

**Fix:** skip dead parents in the setter by catching `ReferenceError`, as `Lineage.__str__` and `describe()` already do, or remove the elders after the evaluation.

## High

### H1. Recursive BNF grammars overflow the Python stack

**Where:** `_recursive_unroll` in `src/byron/operators/graph_tools.py:105-131` and `src/byron/framework/bnf.py`.

**What happens:** Frames are unrolled recursively with no limit on depth or size. With the grammar from the `bnf()` docstring (`bnf([[term], [op, SELF, SELF]])`), 3 of 300 random individuals raised `RecursionError`, and the largest had 51,511 nodes. The error is not `ByronOperatorFailure`, so it propagates: with `mu=100`, initialization fails roughly 60% of the time.

**Fix:** unroll iteratively or with a depth/size budget, and raise `ByronOperatorFailure` when the budget is exceeded.

### H2. Checkpoints cannot be saved with the declared dependencies

**Where:** `src/byron/tools/checkpoint.py:37-46, 83`, and the `_save_checkpoint` helpers in `src/byron/ea/simple_ea.py:198-204` and `src/byron/ea/topk_tournament_ea.py`.

**What happens:** Frames, macros and parameters are classes created inside factory functions, which the standard `pickle` cannot serialize (`PicklingError: Can't pickle local object Frame❬SingleFrame#10❭`). The module uses `dill` when it is installed, but `dill` is not a dependency, and `dill` 0.4.1 fails on Python 3.15 (`'code' object has no attribute 'co_lnotab'`). Saving works with `dill` on Python 3.14. The EAs catch the exception and only log an error, so a run that was asked to save checkpoints continues without any. Reversed (minimization) fitness classes cannot be pickled either (`reverse_fitness.<locals>.T`).

**Fix:** declare a suitable serializer, or implement `__reduce__` for the generated classes (rebuilding them from their factory arguments), and stop swallowing checkpoint failures.

### H3. Shared parameters are shared by every individual in the process

**Where:** `src/byron/framework/shared.py:37-69`.

**What happens:** `make_shared_parameter()` keeps the value in a single `parameter_instance` captured by the class closure. Every individual sees the same value, including parents whose fitness has already been computed. Cloning copies `_is_owner`, so clones of the first individual can change the value. In the probe, mutating a clone changed the phenotype of the original. `T.__init__` also skips `super().__init__()`, so these parameters have no `key`.

**Fix:** keep the shared value inside each individual's genome, for example in one owner node per individual that is re-linked on clone.

### H4. User-defined genetic operators are never used

**Where:** `SysInfo.genetic_operators`, `SysInfo.fitness_functions`, `SysInfo.show` and `get_operators` in `src/byron/sys.py:78-114`.

**What happens:** These functions read `inspect.currentframe().f_globals`, which is the namespace of `byron.sys`, not the caller's. The EAs call `get_operators()` when `operators` is not given, so an operator registered with `@byron.genetic_operator` in a user script is silently ignored, and `byron.sysinfo.fitness_functions` is always empty. Passing `operators=[...]` works, but then the built-in operators must be listed as well.

**Fix:** keep a registry that the `genetic_operator` decorator fills, such as a module-level list in `registry.py`.

## Medium

### M1. Fitness values of unsupported types fail with a misleading error

**Where:** `make_fitness` in `src/byron/fitness/basic.py:161-172`.

**What happens:** Only `int`, `float` and `Sequence` values are accepted. A fitness function that returns a `numpy.int64`, a NumPy array or any other type reaches the `else` branch, whose message calls `type()` without an argument, so the user sees `TypeError: type() takes 1 or 3 arguments`. With `-O` the function returns `None`, which is stored as the fitness. Strings are sequences, so `"12"` silently becomes `Lexicographic((1.0, 2.0))`.

**Fix:** accept `numbers.Integral` and `numbers.Real` (and arrays through `tolist()`), reject `str`, and raise an explicit `TypeError` that names `type(data)`.

### M2. Mixed fitness types crash the stopping condition

**Where:** `src/byron/ea/simple_ea.py:221-224` (the same code is in `topk_tournament_ea.py` and `vanilla_ea.py`), `src/byron/classes/fitness.py:75-79` and `src/byron/fitness/reverse.py:45`.

**What happens:** A numeric `target_fitness` is converted with `make_fitness`. An `int` target becomes `Integer`, while a fitness function returning `float` produces `Scalar`, so the first comparison fails the "Different Fitness types" check. A reversed (minimization) fitness compared with a plain number fails the same check. With `-O`, the comparison reaches `super(T, other)` with an object of the wrong type and raises `TypeError`.

**Fix:** convert the target with the type produced by the fitness function, and document how to express targets for reversed fitness.

### M3. Population entropy does not measure diversity

**Where:** `as_message` in `src/byron/classes/individual.py:277-283`, and `src/byron/tools/entropy.py`.

**What happens:** Each parameter contributes `hash((node, value))`. Node ids are unique across individuals, so identical individuals never share parameter symbols: ten clones of one individual have an entropy of 1.962 instead of 1.386 (the entropy of a single individual). Parameters whose names contain `_` are skipped because of the `k.isalnum()` filter. This affects the logged 𝐻 value and `entropy=True` in `simple_ea` and `topk_tournament_ea`.

**Fix:** hash the node's path in the structure tree instead of the node id, and select parameters with `isinstance(value, ParameterABC)`.

### M4. Uniform crossover leaves array parameters inconsistent

**Where:** `src/byron/operators/crossovers.py:116` and `src/byron/framework/parameter.py:204-211`.

**What happens:** `parameter_uniform_crossover` assigns `param._value` directly. Array parameters keep their old `_raw_value`, so the next partial mutation rebuilds the value from the first parent's symbols. In the probe, an all-`1` value received from the second parent became all-`0` after `mutate(strength=0.01)`. For structural parameters, the assignment has no effect but still counts as a crossover, so the offspring equals the first parent.

**Fix:** copy values through the `value` setter, keep `_raw_value` consistent with `value`, and skip structural parameters.

### M5. `array_parameter` with string symbols and a separator is always invalid

**Where:** `src/byron/framework/parameter.py:194-211`.

**What happens:** `is_correct()` checks the length and the symbols of the joined string, so the separators make every value invalid. `array_parameter('01', 4, sep=' ')` fails with the paranoia `AssertionError` at the first mutation. With `-O`, every individual is invalid and `random_individual()` (`src/byron/operators/initializers.py:40`) loops forever: more than 100,000 failed attempts in 20 seconds.

**Fix:** validate `value.split(sep)` when a separator is set.

### M6. One failing external evaluation aborts the run

**Where:** `MakefileEvaluator` in `src/byron/classes/evaluator.py:389-398`, and `ScriptEvaluator` in lines 506-533.

**What happens:** Both evaluators call `subprocess.run(..., check=True)`, so a program that fails to build or run, or a timeout, raises from the worker and ends the evolution. Unlike `ParallelScriptEvaluator`, they offer no `default_result`. `ScriptEvaluator` checks the number of output lines with an `assert`, so with `-O` a mismatch surfaces later as an `AttributeError` or `TypeError`; it also leaves its phenotype files behind when the script fails. This is based on reading the code.

**Fix:** support `default_result`, replace the `assert` with an explicit error, and delete the files in a `finally` block.

### M7. `topk_tournament_ea` calls the cost function with the wrong arguments

**Where:** `src/byron/ea/selection.py:57-59`.

**What happens:** `top_k_tournament_selection` calls `tournament_cost_function(candidates, max_selectable)` and expects a sorted list back. `topk_tournament_ea` documents, and `simple_ea` uses, a per-individual `Callable[[Individual], float]`. Passing such a function raises `TypeError: <lambda>() takes 1 positional argument but 2 were given`. `test/test_topk_tournament_ea.py` misses this because its target fitness is reached before the first generation, so the selection never runs.

**Fix:** sort the candidates with `key=tournament_cost_function`, as `tournament_selection` does, and make the test run at least one generation.

### M8. `Estimator` assumptions break valid configurations

**Where:** `src/byron/ea/estimator.py:69-83, 145`.

**What happens:** `simple_ea(max_generation=None, stopper=...)` passes `simple_ea`'s own checks but fails in `Estimator` with `TypeError: '>' not supported between instances of 'NoneType' and 'int'`. With `entropy=True`, a `temperature` of 1 or more makes `log()` fail with a math domain error. `_near = target * temperature` assumes a positive target to be maximized, so it is meaningless for minimization and for negative targets. Operators are keyed by `__name__`, so two operators with the same name collapse into one.

**Fix:** handle a missing horizon, validate `temperature`, derive `_near` from the fitness ordering, and key operators by the function object.

### M9. Individuals without an operator lineage cannot be evaluated

**Where:** `src/byron/classes/individual.py:266-273` and `src/byron/registry.py:180`.

**What happens:** The fitness setter updates operator statistics through `self._lineage`. An individual built by hand has no lineage (`AttributeError: 'NoneType' object has no attribute 'parents'`). Calling an initializer positionally, as in `random_individual(top_frame)`, records the frame class as a parent (`AttributeError: type object 'T' has no attribute 'fitness'`). The EAs call initializers with `top_frame=`, which avoids the second case.

**Fix:** skip the statistics when there is no lineage, and never record initializer arguments as parents.

### M10. Resumed runs are not reproducible

**Where:** `src/byron/randy/main.py:32-36, 52-59` and `src/byron/tools/checkpoint.py`.

**What happens:** Checkpoints do not include the random generator, so a run resumed in a new process restarts `rrandom` from seed 42. `Randy` cannot be pickled or deep-copied anyway: `__setstate__` assigns `state` before `_generator` exists (`AttributeError: 'Randy' object has no attribute '_generator'`).

**Fix:** create the generator in `__setstate__` before restoring its state, and save `rrandom.state` in checkpoints.

### M11. `load_population()` returns a tuple, but the documentation uses it as a population

**Where:** `src/byron/tools/checkpoint.py:96`, the docstrings in `src/byron/ea/simple_ea.py:174` and `src/byron/ea/topk_tournament_ea.py:180`, `docs/checkpoint_quick_reference.md` and `docs/checkpoint_workflow.md`.

**What happens:** `load_population()` returns `(population, generation)`. Passing the result to `simple_ea(population=...)`, as documented, raises `AttributeError: 'tuple' object has no attribute 'generation'`.

**Fix:** return only the population (its generation is available as `population.generation`), or update every example.

## Low

### L1. Top-k selection can pick the same individual twice

`src/byron/ea/selection.py:56-66`. Candidates are drawn with replacement, so `with_replacement=False` does not guarantee distinct winners (reproduced). `with_replacement=True` has no effect, because `max_selectable` never exceeds the number of candidates.

### L2. Fractional tournament sizes fail

`src/byron/ea/selection.py:84-107`. `tournament_selection` supports a fractional extra candidate (`tournament_size % 1`) but calls `range(tournament_size)`, so a size of `1.5` raises `TypeError`. `tournament_selection_with_cost` is unreachable, because the first branch of `tournament_selection` already handles cost functions.

### L3. `vanilla_ea` patches `SElement` globally

`src/byron/ea/vanilla_ea.py:104` replaces `SElement.is_valid` with its debug version for the rest of the process, which also affects later runs of the other EAs.

### L4. `simple_ea` and `topk_tournament_ea` flood the log

`src/byron/ea/simple_ea.py:268-273` and `src/byron/ea/topk_tournament_ea.py:268-281` log an INFO message for every parent selection (two in `topk_tournament_ea`). In a 10-generation run, these were 279 of 412 log lines.

### L5. Removing individuals from a population is slow

`src/byron/classes/population.py:154` and `src/byron/classes/individual.py:141-148`. `list.remove()` compares with `Individual.__eq__`, which runs a graph isomorphism test against every preceding individual with equal fitness. Removing 50 of 200 tied, small individuals took 0.37 seconds, against 0.01 milliseconds with an identity-based filter. Node attributes compare by identity, so `__eq__` is effectively an identity test anyway.

### L6. Global counters restart after loading a checkpoint

`src/byron/classes/node.py:36`, `src/byron/classes/parameter.py:46` and `src/byron/classes/individual.py:108`. Node ids, parameter keys and individual ids restart in a new process, so new ids collide with loaded ones: 20 of 20 new node ids did in the probe. Cloning relabels all nodes before a mutation, which hides most collisions in practice; parameter keys may still clash while structural parameters are re-fastened.

### L7. `Individual.size` and `f.estimate_size()` do not work

`src/byron/classes/individual.py:156-162` reads a nonexistent `size` attribute of the syntactic elements (`AttributeError`) and overwrites partial sums with `=`. `src/byron/framework/show_element.py:132` assigns to `individuals` instead of `individual` (`UnboundLocalError`).

### L8. `Byron` answers every attribute lookup

`src/byron/classes/byron.py:48-70` returns a placeholder string for any unknown attribute, under a bare `except:`. As a result, `hasattr()` is always true and `copy.deepcopy(Byron())` raises `TypeError: 'str' object is not callable`.

### L9. `FitnessABC.run_paranoia_checks()` raises `AttributeError`

`src/byron/classes/fitness.py:126-127` calls `super().run_paranoia_checks()`, but `Paranoid` is no longer among the base classes.

### L10. `Vector` consistency checks never run

`src/byron/fitness/basic.py:106` defines `cheeck_comparable` (a typo), so vectors of different lengths are not detected. `Vector.__mul__` (line 134) returns a `list` instead of a `Vector`.

### L11. `choice_parameter` rejects collections without indexing

`src/byron/framework/parameter.py:170` reads `alternatives[0]`, so a `set`, which the `Collection` annotation allows, raises `TypeError` when paranoia checks are enabled.

### L12. Broken or debugging helpers are still exported

`get_dfs_subtree` in `src/byron/tools/graph.py:233` calls `deque.pop()` unbound, reads `_kind` instead of `_type`, and reverses a generator. `calculate_delta_entropy` in `src/byron/tools/entropy.py:42` prints its results and returns `None`. `merge_individuals` in `src/byron/operators/ea_tools.py:140` relabels nodes to plain integers instead of `Node` objects. None of them is used.

### L13. New macros are never appended at the end of a bunch

`src/byron/operators/mutations.py:100` and `src/byron/framework/parameter_structural_global.py:145` take the insertion index from the half-open `random_int(0, len(...))`, so the last position is never chosen.

### L14. Edge cases in two mutation operators

In `src/byron/operators/mutations.py:130`, `remove_macro_from_bunch` with `strength=0` selects from an empty slice, and `rrandom.choice` raises `ValueError` instead of `ByronOperatorFailure`. The docstring of `generic_parameter_mutation` (line 48) says it retries 100 times and does not call `mutate` when `strength` is 0; it does neither.

### L15. Inaccurate documentation

In `src/byron/classes/evaluator.py:81, 141`, `strip_phenotypes` is documented to join lines with spaces, but it joins them with newlines, as the tests expect. The `ParallelScriptEvaluator` docstring (line 536) is copied from `MakefileEvaluator` and describes `make` parameters it does not have. `src/byron/framework/__init__.py:32` says that all factories are cached, but `sequence`, `alternative` and `bunch` are not.

### L16. Cosmetic defects

`src/byron/classes/individual.py:446` pluralizes "macro" using the number of frames. `patch_pos` in `src/byron/classes/_individual_as.py:325-346` repeats the same comparison in each `if`/`elif` pair, so plots are always flipped vertically and never horizontally. The header of `MacroZero` in `src/byron/classes/readymade_macros.py:37-42` freezes the "Automagically written … at" timestamp at import time.
