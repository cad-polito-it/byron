# Project Structure Analysis

This analysis describes the code at commit `b4aa326` (branch `exp/squillero`, October 25, 2026). Figures were measured on Python 3.15.1 with the dependencies locked in `uv.lock`.

## 1. Executive summary

Byron is a Python library for evolutionary source-code fuzzing and program generation. It combines:

- a declarative grammar framework for describing valid candidate programs;
- a graph-based representation of candidate solutions;
- evolutionary operators for initialization, mutation, and crossover;
- fitness abstractions and evaluators for Python functions or external tools;
- evolutionary algorithms with self-adaptive operator selection and population management;
- examples, tutorials, checkpointing utilities, and reproducibility checks.

The repository follows a conventional modern Python layout: maintained implementation code lives under `src/byron`, tests live under `test`, and documentation and usage material are kept outside the package. Packaging, dependencies, test configuration, type checking, formatting, and release metadata are centralized in `pyproject.toml`.

The architecture is coherent, but a review of the source found 34 defects, recorded in `extras/known-bugs.md`. Three of them break common runs: crossovers crash on grammars with structural references, `simple_ea` and `topk_tournament_ea` crash when no target fitness is given, and any run using `lifespan` crashes. Checkpointing, which several documents and examples promote, does not work with the declared dependencies.

## 2. Repository layout

```text
.
├── src/byron/                # Installable Byron package
├── test/                     # Pytest test suite
├── examples/                 # End-to-end examples and external-language demos
├── tutorials/                # Guided learning material (mostly notebooks)
├── docs/                     # GitHub Pages documentation site
├── extras/                   # Templates, notes, known bugs, and legacy tests
├── _experiments/             # Exploratory scripts and notebooks
├── .github/                  # CI workflows and Dependabot configuration
├── .well-known/tdmrep.json   # Text and data mining reservation (W3C TDMRep)
├── pyproject.toml            # Package and development configuration
├── uv.lock                   # Locked dependency resolution
├── qodana.yaml               # JetBrains Qodana configuration
├── README.md                 # Project overview and quick orientation
├── CONTRIBUTING.md           # Contribution guidance
├── CLAUDE.md                 # Guidance for AI coding assistants
├── ANALYSIS.md               # This document
├── PLAN.md                   # Empty placeholder
├── LICENSE                   # Apache License 2.0
├── THIRD_PARTY_LICENSES.md   # Notices of third-party components
└── AUTHORS                   # Author/contributor metadata
```

The maintained implementation consists of 71 Python files (9,488 lines) in `src/byron`:

| Subpackage | Files | Lines | Responsibility |
| --- | ---: | ---: | --- |
| `classes` | 23 | 3,486 | Domain model: individuals, populations, syntactic elements, evaluators |
| `framework` | 12 | 1,643 | Grammar and parameter factories |
| `ea` | 8 | 1,211 | Evolutionary algorithms, selection, operator estimator |
| `operators` | 6 | 846 | Initializers, mutations, crossovers, graph unrolling |
| top-level modules | 8 | 761 | Package API, registry, global symbols, system information |
| `tools` | 5 | 728 | Graph utilities, tag providers, entropy, names, checkpoints |
| `user_messages` | 4 | 345 | Logging, warnings, checks, exceptions |
| `fitness` | 3 | 251 | Fitness types and reversed fitness |
| `randy` | 2 | 217 | Reproducible random number generator |

The tests contain 48 tracked files (46 Python files, 4,029 lines), including unit, integration, stress, reproducibility, and external-process tests. The repository also contains a sizeable experimental and educational surface (52 files in `examples`, 12 in `tutorials`, 30 in `_experiments`, 19 in `extras`), which is useful for research workflows but should be distinguished from the core library when assessing production behavior.

Generated and local artifacts such as `.venv`, Python caches, coverage output, `dist`, `*.egg-info`, pickle files (including checkpoints), IDE settings, `.python-version`, and the local `.claude/` folder are ignored by Git. `PLAN.md` is tracked but empty; it is not part of the runtime architecture.

## 3. Packaging and development configuration

`pyproject.toml` is the central project definition:

- package name: `byron`;
- current version: `0.8a1.dev67`;
- supported Python versions: `>=3.14,<4.0`;
- build backend: `uv_build` (`>=0.13.5,<0.14`);
- source package discovery through the `src/` layout;
- primary dependencies: NetworkX, NumPy, Rich, SciPy, and tqdm, with minimum versions equal to the locked ones;
- optional integrations (`byron[all]`): joblib, matplotlib, and psutil;
- development group: pytest, pytest-emoji, coverage, Jupyter, and icecream (Ruff, mypy, and bumpver are run through `uvx`);
- pytest test path: `test`;
- mypy target module: `byron`;
- Ruff: target Python 3.14, code lines up to 120 characters, comment and docstring lines up to 80 (`W505`), import sorting, quote style preserved;
- bumpver patterns for synchronizing version metadata in `pyproject.toml`, `docs/index.md`, and `src/byron/global_symbols.py`.

`uv.lock` makes development and CI dependency resolution reproducible. `.github/workflows/pytest.yml` runs the test suite on Python 3.14 and 3.15, using `uv sync --all-extras` followed by `uv run pytest`, without the `--all` option. A Codacy security scan runs on pushes to `alpha`, `beta`, and `pre-alpha`, on pull requests to `alpha`, and weekly; Dependabot proposes weekly dependency updates; `qodana.yaml` configures JetBrains Qodana.

The quality tools currently report the following:

- in the default suite, 152 tests passed and 33 were skipped; `test_onemax` could not run in the restricted environment used for this analysis, because joblib cannot query process semaphores there;
- with `--all`, `test/stress/test_large_individuals.py::test_crossover[bunch_onepoint_crossover-100]` fails because of the crossover defect described in section 10;
- mypy, as configured, stops with `Cannot find module "byron"`, because `[tool.mypy]` lists the module without a search path; run on `src/byron`, it reports 194 errors in 38 files;
- Ruff 0.17.2 reports 675 findings on `src`, `test`, and `examples`: 259 comment or docstring lines longer than 80 characters, and the rest from rule families enabled by Ruff's default selection.

## 4. Core package architecture

### 4.1 `byron.classes`: domain model

This package contains the principal runtime objects:

- `Individual` represents a candidate solution. Its genome is a NetworkX `MultiDiGraph`, with nodes containing Byron syntactic elements and edges encoding structure or references.
- `Population` stores individuals, generation state, sorting, aging, entropy, and optional memory tracking.
- `SElement` is the common abstraction for frames, macros, and parameters. Its metaclass, `SElementMeta`, gives every generated class a unique identifier and makes classes comparable with identifier strings.
- `FrameABC` describes structural nodes that produce successors.
- `Macro` describes terminal or textual program elements.
- `ParameterABC` and its subclasses represent configurable values and structural references.
- `Node`, `NodeReference`, and `NodeView` provide graph identity and read-only navigation.
- `FitnessABC` defines fitness comparison semantics: `==` and `!=` test distinguishability, `>` and `<` fitness, and `>>` and `<<` dominance.
- `EvaluatorABC` and its subclasses connect the population to fitness computation (see section 4.5).
- `Age`, `Lineage`, monitoring, paranoia checks, and visualization helpers provide lifecycle, diagnostics, and introspection support.

The class package is the stateful center of the system. Other subsystems operate on these objects rather than introducing a separate persistence or service layer.

### 4.2 `byron.framework`: declarative program grammars

The framework translates user-facing grammar declarations into syntactic element classes. Important factories include:

- `sequence(...)` for ordered children;
- `alternative(...)` for random alternatives;
- `bunch(...)` for variable-size collections, with an optional separator;
- `bnf(...)` for recursive grammar rules, using the `SELF` placeholder;
- `macro(...)` for textual templates, with an optional safe formatting mode;
- parameter factories for integer, float, choice, array, counter, shared, local-reference, and global-reference values.

The macro factory and all parameter factories except `make_shared_parameter` are cached, so equal arguments return the same class. Frame factories create a new class at every call and register it in a global directory, which allows frames to be referenced by name. The framework uses classes as grammar definitions; instances are later placed inside an individual's graph. This separates the definition of a search space from the generated genotype and permits structural validation during initialization and evolution.

Shared parameters (`make_shared_parameter`) currently keep their value in a single object for the whole process, not per individual (see section 10).

### 4.3 `byron.operators`: genotype construction and variation

Operators are grouped by responsibility:

- `initializers.py` creates random individuals;
- `mutations.py` changes parameter values and adds or removes macros in bunches;
- `crossovers.py` exchanges parameter values, bunch tails, or whole subtrees between two parents;
- `graph_tools.py` recursively unrolls frames and macros into graph nodes and initializes their parameters;
- `ea_tools.py` groups graph elements and parameters across individuals.

The `genetic_operator` decorator in `registry.py` gives operators a common contract. It records parent arity (`None` for initializers), tracks statistics, treats exceptions of type `ByronOperatorFailure` and empty results as aborts, filters invalid offspring, assigns lineage, and discards graph components that are no longer reachable. Operators are recognized through a tag attribute; when no operator list is given, the EAs use `byron.sys.get_operators()`, which only sees the operators imported into `byron.sys`, that is, the built-in ones.

### 4.4 `byron.ea`: evolutionary algorithms

The EA layer contains:

- `simple_ea` (with the deprecated alias `adaptive_ea`), a (μ+λ) algorithm with self-adaptive operator selection;
- `topk_tournament_ea`, the same loop with top-k tournament parent selection;
- `vanilla_ea`, a minimal (μ+λ) algorithm with uniform operator choice;
- tournament, cost-based, and top-k tournament selection;
- `Estimator`, which chooses operators with a successive elimination scheme based on confidence bounds of their rewards, and adapts mutation strength through a temperature;
- `check()`, which prints the registered operators by kind.

The execution pattern of `simple_ea` is:

1. call initializer operators (with `top_frame=`) until the population holds `mu` individuals;
2. evaluate individuals without fitness and sort the population into fronts of non-dominated individuals;
3. ask the estimator for an operator, select its parents with a tournament of size 1 (that is, uniformly), and apply it, `lambda_` times;
4. if `lifespan` is set, remove individuals older than the lifespan;
5. add the offspring, evaluate them, sort the population, and keep the best `mu` individuals;
6. optionally save checkpoints or call a user callback;
7. stop at the generation limit, the target fitness, or a custom stopping condition.

Selection pressure therefore comes from (μ+λ) truncation rather than from parent selection, except in `topk_tournament_ea`. The algorithms rely on the population's fitness ordering and the `FitnessABC` comparison protocol rather than hard-coding a single scalar optimization direction.

### 4.5 Fitness and evaluation

`byron.fitness` implements fitness values and comparison behavior, including scalar (with approximate equality), integer, float, vector, lexicographic, and reversed forms. The `fitness_function` decorator in `registry.py` normalizes return values with `make_fitness`, associates a fitness type, and records a bounded log of values.

`byron.classes.evaluator` provides the execution boundary:

- `PythonEvaluator` invokes a registered Python fitness function sequentially, in a thread pool, or in joblib processes;
- `MakefileEvaluator` runs `make` in a temporary directory for each individual, in parallel threads;
- `ScriptEvaluator` writes all phenotypes to files and calls a script once;
- `ParallelScriptEvaluator` runs a script in a temporary directory for each individual, and can assign a default result when the script fails;
- the `strip_phenotypes` option removes the header, blank lines, and surrounding spaces from phenotypes (the result is still multi-line).

Evaluators dump the canonic representation of each individual, so phenotypes do not depend on internal node numbering. This design allows the same evolutionary machinery to optimize abstract functions, compiled programs, interpreters, simulators, or shell-based evaluators.

### 4.6 Tools and operational support

`byron.tools` contains cross-cutting utilities:

- `graph.py` extracts structure trees, successors, siblings, and parameters, re-fastens structural parameters, and reorders children; structure trees are cached and shared, so callers must copy them before modifying them;
- `providers.py` computes derived node tags, such as paths and type paths, and records which tags have been computed;
- `entropy.py` computes the entropy of the population's symbols as a diversity measure (the symbols currently overestimate diversity; see `extras/known-bugs.md`);
- `names.py` extracts base names from generated class names;
- `checkpoint.py` saves and loads populations or selected individuals.

Checkpointing relies on `pickle`, or on `dill` when it is installed. The standard `pickle` cannot serialize the classes generated by the framework, and `dill`, which is not a declared dependency, does not support Python 3.15 yet; in practice, checkpoints currently work only with `dill` on Python 3.14. Because pickle can execute arbitrary code while loading, checkpoint files must be treated as trusted input.

`byron.user_messages` centralizes logging, warnings, validation helpers, and Byron-specific exceptions. `global_symbols.py` supplies runtime flags (test, notebook, paranoia, and debug modes; availability of optional packages) and shared constants used across the package. `byron.randy` provides `rrandom`, the reproducible random number generator used everywhere in the package, seeded with 42 at import.

## 5. Runtime data flow

The main conceptual pipeline is:

```text
User grammar
    ↓
Framework factories
    ↓
Typed Frame/Macro/Parameter classes
    ↓
Initializer unrolling
    ↓
Individual backed by NetworkX MultiDiGraph
    ↓
Canonic representation and phenotype dump
    ↓
Evaluator
    ↓
Fitness value
    ↓
Population sorting and selection
    ↓
Mutation/crossover
    ↺
```

An individual is technically a graph rooted at `NODE_ZERO`. `FRAMEWORK` edges form the generated program hierarchy and must form a tree, while `LINK` edges, keyed by the parameter that owns them, store the targets of structural parameters. This supports non-tree relationships such as local variables, global variables, loops, and subroutines while retaining a tree-like structural view for traversal and rendering.

The graph model is the main architectural decision in Byron. It enables structural constraints and typed references, but it also means that cloning, canonical relabeling, validation, serialization, and variation must preserve both graph topology and semantic metadata. Several defects listed in section 10 come from code that traverses the whole multigraph where only the structure tree was intended.

## 6. Public API and compatibility layer

`src/byron/__init__.py` re-exports a broad convenience API under short aliases:

- `byron.f` (framework factories) and `byron.C` (classes);
- `byron.ea` (evolutionary algorithms) and `byron.op` (operators);
- `byron.evaluator`, and `byron.fit` or `byron.fitness`;
- the registry decorators `byron.genetic_operator` and `byron.fitness_function`;
- `byron.rrandom`, `byron.logger`, and `byron.sysinfo`;
- checkpoint and graph helpers, global symbols, and system information.

The modules `evaluator_.py` and `fitness_.py` act as compatibility/public-name shims around the implementation modules. All implementation modules declare `__all__`, while package `__init__` files and shims re-export them through wildcard imports, so subpackages such as `byron.op`, `byron.ea`, and `byron.C` export only their own names; before commit `8859722` they also re-exported everything they imported. The import surface still depends on chains of wildcard imports: for example, `byron.sys.get_operators()` finds operators by scanning the namespace of `byron.sys`, which is filled by `from byron.operators import *`. Changes to import order or top-level side effects should therefore be made cautiously.

`__main__.py` is a lightweight command-line entry point that prints Byron version and copyright information; the project is primarily a library rather than a command-heavy application.

## 7. Tests and quality controls

The test layout mostly mirrors the package:

```text
test/byron/classes/
test/byron/ea/
test/byron/fitness/
test/byron/framework/
test/byron/operators/
test/byron/tools/
test/byron/user_messages/
test/checkpoint/
test/paranoia/
test/randy/
test/runs/
test/stress/
```

Testing covers:

- graph-backed classes and syntactic elements;
- grammar and parameter construction;
- fitness and evaluators;
- evolutionary algorithms and selection;
- messaging and runtime modes;
- reproducibility;
- shell and external evaluator runs;
- large individuals and stress scenarios.

`test/conftest.py` adds an `--all` option for tests marked `avoidable` (the stress tests and the external evaluator run), allowing the default suite to omit tests that are expensive or intentionally optional. CI runs only the default suite. Coverage configuration includes both `src/*` and `test/*`.

Twelve test files are inactive: nine whose names start with `_test_` (in `ea`, `framework`, `tools`, and `user_messages`) and three disabled crossover and checkpoint tests (`disabled-test_*.py`). As a result, crossovers and global references are exercised only by the avoidable stress tests, checkpoints and shared parameters are not tested at all, and the tests in `test_topk_tournament_ea.py` reach their target fitness before the first generation, so they never exercise parent selection. The repository also contains `extras/test_old`, which should be treated as historical material rather than the authoritative test suite.

## 8. Examples, tutorials, and documentation

### Examples

`examples/` contains both small optimization problems and realistic source generation workflows:

- classic OneMax, TwoMax, reverse OneMax, and knapsack problems;
- C/GCC, Go, MIPS, and RISC-V examples, including RISC-V instruction and register support code;
- a shell-based evaluator;
- checkpoint and multi-session evolution examples;
- a notebook accompanying the Byron paper, and a placeholder for the PSB2 benchmark suite (README only).

These examples are important architectural consumers because they exercise the public API from outside the package and demonstrate external-process evaluation. Some of them are affected by known defects: `examples/classics/knapsack.py` crashes at startup because it sets no target fitness, and its `lifespan=2` would trigger the lifespan defect next; the checkpoint examples depend on serialization that does not work with the declared dependencies.

### Tutorials

`tutorials/` focuses on onboarding and experimentation with fitness functions, parameters, evolution, and structural constraints, mostly through notebooks (macros and parameters, frames, local and global references, checks, genetic operators, assembly, and variables).

### Documentation

`docs/` is published with GitHub Pages using the Cayman theme, with a customized layout. It includes:

- project landing page and release metadata;
- evolutionary algorithm background;
- checkpointing guides and quick references;
- multi-session evolution;
- reproducibility and paranoia checks;
- project history, contributors, and PyPI information.

The documentation is conceptually aligned with the implementation, especially around evolutionary terminology and runtime safety checks, but some details are out of date: all three checkpoint guides use the result of `load_population()` as a population, while it returns a tuple, and the docstrings of `strip_phenotypes` describe a single-line output. Outside `docs/`, `extras/known-bugs.md` lists known defects, `THIRD_PARTY_LICENSES.md` reproduces the notices of third-party components, and `CLAUDE.md` summarizes commands, architecture, and conventions for AI coding assistants.

## 9. Architectural strengths

1. **Clear separation of concerns.** Grammar definition, graph representation, variation, evaluation, and optimization are separated into identifiable packages.
2. **Extensible operator model.** Decorator-based registration gives custom fitness functions and operators a common contract, with statistics and lineage tracking, although custom operators must currently be passed to the EAs explicitly.
3. **Rich representation.** A typed directed multigraph can model structures beyond simple linear genomes or trees.
4. **Multiple evaluation boundaries.** Python, scripts, Makefiles, and parallel execution are supported without changing the EA layer.
5. **Self-adaptive search.** The estimator learns which operators produce valid and improving offspring and tunes mutation strength during the run.
6. **Research-oriented reproducibility.** Randomness, paranoia checks, checkpointing, lineage, fitness logging, and reproducibility tests are explicitly represented.
7. **Good executable documentation.** Examples cover both abstract APIs and real generated-language workflows.

## 10. Known defects

`extras/known-bugs.md` lists 34 defects ordered by severity (3 critical, 4 high, 11 medium, 16 low), each with its location, a reproduction, and a suggested fix. The most important are:

- **Crossovers on grammars with structural references (critical).** `bunch_onepoint_crossover` and `subtree_crossover` collect subtrees by traversing the whole multigraph, including `LINK` edges, so they delete and copy nodes outside the selected subtree and lose the keys of copied references. On a grammar with local jumps, most calls raise exceptions that stop the run.
- **Missing target fitness (critical).** `simple_ea` and `topk_tournament_ea` crash during initialization when `target_fitness` is not given, because the estimator multiplies it by the temperature.
- **Lifespan (critical).** Offspring keep weak references to their parents, and elders are removed before offspring are evaluated, so the fitness setter fails with `ReferenceError`.
- **Recursive grammars (high).** Frames are unrolled recursively without a depth limit; recursive BNF grammars regularly exceed the Python recursion limit.
- **Checkpoints (high).** Populations cannot be saved with the standard `pickle`, and errors are only logged.
- **Shared parameters (high).** Their value is shared by every individual in the process.
- **Operator discovery (high).** Operators registered by the user are ignored unless passed explicitly.

## 11. Maintenance observations

These are structural observations rather than defects:

- The top-level package initializer imports and re-exports many internal modules. This improves ergonomics but increases import-time coupling and makes circular-import regressions easier to introduce.
- `classes`, `framework`, `operators`, and `tools` rely heavily on wildcard imports. Every module now declares `__all__`, but module namespaces are still assembled from star-import chains, and some code, such as `byron.sys.get_operators()`, depends on what those chains bring in.
- The graph representation is powerful but centralizes significant complexity in `classes/individual.py`, `tools/graph.py`, and `operators/graph_tools.py`. Changes involving cloning, relabeling, validation, or variation should be reviewed across all three areas, and graph traversals should state whether they follow the structure tree or the whole multigraph.
- Node ids, parameter keys, and individual ids come from process-global counters, and several caches (`functools.cache`, `lru_cache`, the global element directory) hold process-wide state. This simplifies the code but complicates serialization, multi-process use, and resumed runs.
- Paranoia checks are `assert` statements, active unless Python runs with `-O`. They catch many inconsistencies during development but make unoptimized runs significantly slower.
- Optional dependencies are intentionally runtime-detected. Features such as plotting, process-based evaluation, and detailed machine information may be unavailable in minimal installations and should remain explicitly surfaced to users.
- The repository mixes maintained code with experiments, notebooks, generated documentation artifacts, historical tests, and research examples. The existing directory separation is useful, but contributors should confirm whether a change belongs to the supported package/test path before editing auxiliary material.
- Checkpoint serialization is intentionally Python-object-based. It is convenient for resuming experiments but is Python-version and code-layout sensitive, and it must not be used with untrusted files.
- Static analysis is not yet enforced: the configured mypy run cannot locate the package, and the Ruff findings and type errors listed in section 3 are not checked in CI.

## 12. Recommended navigation order for contributors

For a new feature or bug investigation, the most efficient reading order is:

1. `README.md`, `CLAUDE.md`, and `pyproject.toml` for project conventions and supported workflows.
2. `extras/known-bugs.md` for defects that may affect the area of interest.
3. `src/byron/__init__.py` to understand the public import surface.
4. The relevant domain classes under `src/byron/classes`.
5. The corresponding framework, operator, evaluator, or EA module.
6. The matching test directory under `test/byron`.
7. An executable example under `examples/` or `tutorials/`.
8. Related documentation under `docs/`.

For graph or structural changes, start with `Individual`, `NodeReference`, `tools/graph.py`, and `operators/graph_tools.py`. For new user-facing optimization behavior, start with `registry.py`, `fitness`, `evaluator`, and the EA implementations.

## 13. Overall assessment

Byron is structured as a reusable research library rather than a conventional web service or standalone application. Its central abstraction is a typed, mutable, graph-backed individual generated from a declarative grammar and optimized by registered evolutionary operators. The repository supports that model consistently across implementation, tests, examples, documentation, and CI.

The primary complexity lies in preserving graph invariants and semantic references while individuals are cloned, mutated, crossed over, evaluated, serialized, and canonically relabeled. The package boundaries are generally well aligned with those responsibilities, making the project extensible. However, the defects listed in section 10 sit exactly at these boundaries, and the code that would expose them (crossovers, checkpoints, shared parameters, recursive grammars) is the least covered by active tests. Fixing the critical defects, re-enabling the disabled tests, and running the avoidable tests in CI would give the most value. Changes to core graph or import behavior have broad impact and should be validated with both the focused unit tests and at least one end-to-end example.
