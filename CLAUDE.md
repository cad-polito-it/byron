# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Byron is an evolutionary source-code fuzzer (successor of MicroGP): it generates random programs from a user-declared grammar, encodes them as typed directed multigraphs, and improves them with an evolutionary algorithm. Alpha software; `alpha` is the main branch, `exp/*` branches are experimental.

## Commands

Dependencies are managed with `uv` (Python ≥3.14, developed on 3.15; CI tests 3.14 and 3.15). Ruff, mypy, coverage and bumpver are run via `uvx`/`uv run`, not installed as deps.

```shell
uv sync --all-extras                      # install (dev group is default)
uv run pytest                             # test suite (what CI runs)
uv run pytest --all                       # also run tests marked @pytest.mark.avoidable
uv run pytest test/randy/test_randy.py::test_name   # single test
uv run coverage run --branch -m pytest; uv run coverage html
uvx ruff check src test                   # lint (code ≤120, comments/docstrings ≤80, isort)
uvx ruff format src test                  # format (quote style preserved — don't normalize quotes)
uvx mypy                                  # type check (configured for module `byron`)
```

Release: `uvx bumpver update` (bumps `pyproject.toml`, `docs/index.md`, `src/byron/global_symbols.py` and commits), then `uv build` / `uv publish` — see `extras/memo.md`.

Test layout notes: test files prefixed `_test_` or `disabled-test_` are intentionally not collected. Examples are run directly, e.g. `uv run python examples/classics/onemax.py`.

## Architecture

The package lives in `src/byron/`. The top-level `byron/` directory at repo root contains only stale `__pycache__` — ignore it. `byron/__init__.py` re-exports everything under short aliases used throughout examples: `byron.f` (framework), `byron.op` (operators), `byron.ea`, `byron.evaluator`, `byron.fit`/`byron.fitness`, `byron.C` (classes), `byron.rrandom`, `byron.logger`.

**Grammar declaration (`framework/`) builds classes, not objects.** Functions like `f.macro(...)`, `f.sequence([...])`, `f.alternative([...])`, `f.bunch([...])`, `f.bnf(...)`, `f.integer_parameter(...)`, `f.local_reference(...)`/`f.global_reference(...)` are factories that dynamically create and return new *subclasses* of `Macro`, `FrameABC` or `ParameterABC` (in `classes/`). All of these derive from `SElement`, whose metaclass `SElementMeta` assigns each generated class a unique `BYRON_CLASS_ID` and makes classes comparable to that string ID. The "top frame" passed to an EA is such a class.

**Individuals are networkx `MultiDiGraph`s** (`classes/individual.py`). Node 0 (`NODE_ZERO`) is a `MacroZero` root. Each node stores its instantiated SElement under the `_selement` attribute; edges carry `_type`: `FRAMEWORK` edges form the structure tree (must be an arborescence), `LINK` edges are references created by structural parameters (local/global references to other nodes). `NodeReference`/`NodeView` give typed access to a node within a graph. Unrolling a grammar class into graph nodes is in `operators/graph_tools.py`; phenotype text rendering uses `_text_before_*`/`_text_after_*` extra parameters (defaults in `global_symbols.py`, overridable via `f.set_global_parameter`).

**Registration via decorators (`registry.py`).** `@byron.genetic_operator(num_parents=N)` turns a function into an operator (`num_parents=None` → initializer taking `top_frame`; 1 → mutation; ≥2 → crossover). The wrapper tracks `Statistics`, drops invalid offspring, sets lineage, and treats `None`/`[]`/`ByronOperatorFailure` as an abort. `@byron.fitness_function` wraps a function so its result is converted to a `FitnessABC` (see `fitness/basic.py`: `Scalar`, `Integer`, `Vector`, `Lexicographic`, …) and logged. Objects are recognized via `_byron_ == BYRON_TAG` and a `type` attribute (`get_byron_type`). Operators in `operators/` are discovered by EAs this way.

**Evaluation (`classes/evaluator.py`)**: `PythonEvaluator` (calls a fitness function on phenotype text; optional thread/joblib backends), `MakefileEvaluator`, `ScriptEvaluator`, `ParallelScriptEvaluator` (spawn external tools in temp dirs). See `examples/gcc`, `examples/riscv`, etc.

**EAs (`ea/`)**: `simple_ea` (self-adaptive operator selection via `ea/estimator.py`, rewards/temperature), `vanilla_ea`, `topk_tournament_ea`; they work on `classes/population.py`'s `Population` and support checkpointing (`tools/checkpoint.py`, documented in `docs/checkpointing.md`).

**Randomness**: always use the global `byron.rrandom` (`randy/`, a reproducible, state-saveable `Randy` wrapper) — never the `random` module directly. `test/paranoia/test_reproducibility.py` depends on this.

**Paranoia mode.** `paranoia_mode` is true when `assert` is active (i.e. not run with `-O`). Heavy consistency checks are written as `assert ...` statements and `run_paranoia_checks()` methods (`classes/paranoid.py`), with messages prefixed by `PARANOIA_VALUE_ERROR`/`PARANOIA_TYPE_ERROR`/`PARANOIA_SYSTEM_ERROR`. Follow this pattern: checks go in asserts so they vanish under `-O`; never put side effects needed in production inside an `assert`. Other auto-detected flags (`test_mode`, `notebook_mode`, `main_process`, `*_available`) live in `global_symbols.py`. User-facing warnings/errors go through `user_messages` (`logger`, `performance_warning`, `runtime_warning`, check helpers like `check_value_range`).

## Conventions

- Every source file starts with the Byron ASCII-art banner and an SPDX/Apache header; copy it from a neighbouring file.
- Modules declare `__all__` and are commonly consumed via `from byron.xxx import *`.
- Commit messages follow the [programmer-zendo commit guide](https://github.com/squillero/programmer-zendo/blob/main/git-commit.md) (Conventional Commits v1.0.0):

  ```text
  <type>[optional scope]: <short description>

  [optional long description(s)]

  [optional specification(s)]
  ```

  Allowed types: `build`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `style`, `test` (no `chore`). Add `!` after the type to flag a breaking change (e.g. `feat(ea)!: ...`). Example from history: `style(bumpver): Bump version to 0.8a1.dev67`.
- Don't credit Claude in commits or PRs: no `Co-Authored-By: Claude` trailer, no "Generated with Claude Code" line.
- Don't sign commits: always use `git commit --no-gpg-sign` (the user's global config has `commit.gpgsign = true`).
- Prefer builtins, generators and comprehensions: few lines of code, plenty of comments.

## Python style

Follow the [programmer-zendo Python style guide](https://github.com/squillero/programmer-zendo/blob/main/python/style.md). Every rule may be broken, but only for a good reason that is explained in a comment. The rules that matter most in practice:

- **Naming:** use nouns for variables and properties, and full sentences for functions and methods (`factors = factorize(formula)`). Predicates start with `is_` or `has_`. Factories that return types may be named with a noun (`percentage = safe_value(0, 100)`). Module-internal and class-private names start with a single `_`. Don't use `__foo` (name mangling) or invent new `__dunder__` names. A trailing `_` is only for avoiding clashes (`list_`, `lambda_`, `type_`). Exception: single uppercase letters are acceptable for graphs and other mathematical objects (`G`, `T`, `H`, `G1`, `I`), and so are established acronyms such as `UCB`/`LCB`.
- **Strings:** use f-strings rather than `.format()` or `%`. Use single quotes for constants, parameters and dict keys (`'utf-8'`, `data['foo']`), and double quotes for messages to the user. Ruff is configured to preserve quotes, so don't normalize them.
- **Logging:** use deferred `%`-formatting with the values passed as arguments (`logger.warning("test: %r != %r", foo, bar)`), never f-strings. Guard costly arguments with `isEnabledFor`.
- **Error and warning messages:** first state the problem, then `: expected ...`, then `— hint`. For example: `"TypeError: invalid type %s for %s: expected subclass of %s — did you add extra '()'?"`.
- **`assert`:** use it only for internal consistency and correct API usage, never for runtime events that can really happen. This matches the paranoia-mode convention above.
- **Annotations:** annotate every function; mypy is the checker. Avoid multiple statements on one line.
- **Classes:** use properties, not getters and setters, but use a method when the computation is expensive. Don't override `__repr__`. Use `ABC` and `@abstractmethod` for abstract classes. Define `__slots__` only when sure, and then also define `__getstate__`/`__setstate__` at the top of the class, before `__init__` (see `Randy`).
- **Line length:** comments and docstrings can be at most **80** characters per line, and code at most **120**. Ruff checks both limits: `line-length = 120`, plus `W505` with `max-doc-length = 80`.
- **Docstrings and comments:** write them in formal American English. Use the NumPy docstring style. Write descriptions in the descriptive mood (`"""Calculates the next Mersenne prime."""`). The first line is always a concise summary. Be terse on methods and verbose on classes, with examples and an `Attributes` section for public attributes and properties. Document `__init__` only if its parameters aren't obvious, and don't document `__str__` and similar methods.
- **Versions:** follow PEP 440 (handled by bumpver).

Some existing code breaks these rules: there are a few `__repr__` overrides and f-strings inside `logger.*` calls. Apply the rules to new and changed code, and don't do drive-by rewrites of untouched code.
