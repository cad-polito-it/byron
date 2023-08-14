`byron` 🖋
==========

[![License: Apache 2.0](https://img.shields.io/badge/license-apache--2.0-green.svg)](https://opensource.org/licenses/Apache-2.0) 
[![Status: Actrive](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/squillero/byron)
![Language: Python](https://img.shields.io/badge/language-python-blue.svg)
![Version: 0.1.dev2](https://img.shields.io/badge/version-0.1.dev11-orange.svg)
![Codename: Don Juan](https://img.shields.io/badge/codename-Don_Juan-pink.svg)
[![Documentation Status](https://readthedocs.org/projects/byron/badge/?version=pre-alpha)](https://byron.readthedocs.io/en/pre-alpha/?badge=pre-alpha)

Byron is an [evolutionary tool](https://en.wikipedia.org/wiki/Evolutionary_algorithm): given a problem, it first generates a set of random solutions, then iteratively refines and improves them using the results of their evaluations together with structural information. It may be used as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization).

Byron internally encodes candidate solutions as [directed](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph) [multigraphs](https://en.wikipedia.org/wiki/Multigraph) and can tackle problems with complex, structured constraints. For instance, it may be used to create realistic programs with loops, interrupts, and recursive subroutines. 

Candidate solutions are evaluated by calling a user Python function or a shell script, that, for instance, may use proprietary tools. Different types of parallelization are supported out of the box, from simple multithreading to the creation of temporary directories where multiple subprocesses are concurrently [spawned](https://en.wikipedia.org/wiki/Spawn_(computing)).

### Installation

**⚠️ Byron is currently in [pre-alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Pre-alpha) and under active development**

```
pip install --upgrade byron
```

Few optional dependencies can enhance Byron, but are not strictly required:

```
pip install --upgrade matplotlib
pip install --upgrade joblib
pip install --upgrade psutil
```

### TL;DR

This repo is only useful if you want to hack the code (see: [CONTRIBUTING](CONTRIBUTING.md)). 

* The default branch is always the more stable
* Do not clone experimental branches `exp/*` unless you know what you are doing
* Follow this [style guide](https://github.com/squillero/style/blob/master/python.md) and keep the code formatted with [Black](https://black.readthedocs.io/en/stable/)
* Write as few lines of code and as many lines of comments as possible (ie. use builtins, exploit generators and list comprehension)
* Use [pytest](https://docs.pytest.org/) and [Coverage.py](https://coverage.readthedocs.io/) for unit testing (ie. `coverage run -m pytest`)
* Use [pylint](https://mypy-lang.org/) for basic linting and [mypy](https://mypy-lang.org/) for additional type checking
* Be [paranoid](./PARANOIA.md) (cit. *"I need someone to show me the things"*)
* It may be wise to contact Alberto or Giovanni before trying to change anything

### Contacts

* [Giovanni Squillero](https://github.com/squillero) [:email:](mailto:squillero@polito.it) [:house:](https://staff.polito.it/giovanni.squillero/)
* [Alberto Tonda](https://github.com/albertotonda/) [:email:](mailto:alberto.tonda@inra.fr) [:house:](https://www.researchgate.net/profile/Alberto_Tonda)

### Licence
Copyright © 2023 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
