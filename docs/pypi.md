[![License: Apache 2.0](https://img.shields.io/badge/license-apache--2.0-green.svg)](https://opensource.org/licenses/Apache-2.0) 
[![Status: Actrive](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/cad-polito-it/byron)
![Language: Python](https://img.shields.io/badge/language-python-blue.svg)
![Version: 0.1.dev2](https://img.shields.io/badge/version-0.8a1.dev30-orange.svg)
![Codename: Don Juan](https://img.shields.io/badge/codename-Don_Juan-pink.svg)
[![Documentation Status](https://readthedocs.org/projects/byron/badge/?version=pre-alpha)](https://byron.readthedocs.io/en/pre-alpha/?badge=pre-alpha)

Byron is an [evolutionary tool](https://en.wikipedia.org/wiki/Evolutionary_algorithm): given a problem, it first generates a set of random solutions, then iteratively improves them using the results of their evaluations together with structural information. It may be used as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization).

Byron internally encodes candidate solutions as [typed](https://rcor.me/papers/typed-graph-theory.pdf), [directed](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph) [multigraphs](https://en.wikipedia.org/wiki/Multigraph) and can tackle problems with complex, structured constraints. For instance, it may be used to create realistic programs with loops, flow-control structures, and subroutines. Gory detail: solutions are heterogeneous [forests](https://en.wikipedia.org/wiki/Tree_(graph_theory)#Forest) with additional edges connecting leaves, possibly between different trees.

Candidate solutions are dumped as text and then evaluated by calling a user-defined Python function or by invoking a shell script that may use external proprietary tools. Different types of parallelization are supported out of the box, from simple multithreading to the creation of temporary directories where multiple subprocesses are concurrently [spawned](https://en.wikipedia.org/wiki/Spawn_(computing)).

## Installation

**⚠️ Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active development**

As simple as

```
pip install --upgrade byron
```

Few optional dependencies can enhance Byron, but are not strictly required. You can get them with

```
pip install --upgrade "byron[full]"
```

or install optional modules one by one

```
pip install --upgrade matplotlib
pip install --upgrade joblib
pip install --upgrade psutil
```

## Documentation

None yet, but some HOWTO's and examples [are available](https://github.com/cad-polito-it/byron/tree/alpha/examples) in the repo.

## Contacts

* Giovanni Squillero — <giovanni.squillero@polito.it>
* Alberto Tonda — <alberto.tonda@inrae.fr>

## License

Copyright (c) 2023 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
