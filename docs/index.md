# Byron v0.8a1.dev45 *"Don Juan"*

> A multi-purpose extensible self-adaptive optimizer and fuzzer

Byron is an [evolutionary tool](https://cad-polito-it.github.io/byron/evolution): given a problem, it first generates a set of random solutions, then iteratively improves them using the results of their evaluations together with structural information. It may be used as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization).

Byron internally encodes candidate solutions as [typed](https://rcor.me/papers/typed-graph-theory.pdf), [directed](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph) [multigraphs](https://en.wikipedia.org/wiki/Multigraph) and can tackle problems with complex, structured constraints. For instance, it may be used to create realistic programs with loops, flow-control structures, and subroutines. Gory detail: solutions are heterogeneous [forests](https://en.wikipedia.org/wiki/Tree_(graph_theory)#Forest) with additional edges connecting leaves, possibly between different trees.

Candidate solutions are dumped as text and then evaluated by calling a user-defined Python function or by invoking a shell script that may use external proprietary tools. Different types of parallelization are supported out of the box, from simple multithreading to the creation of temporary directories where multiple subprocesses are concurrently [spawned](https://en.wikipedia.org/wiki/Spawn_(computing)).

Byron was made possible by the contributions of [many individuals](contributors) over [many years](history). 

### Installation

**⚠️ Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active development**

The Python package is available on [PyPi](https://pypi.org/project/byron/), the source code is on [GitHub](https://github.com/cad-polito-it/byron).

### Contacts

* Giovanni Squillero — <giovanni.squillero@polito.it>
* Alberto Tonda — <alberto.tonda@inrae.fr>

### License

Copyright (c) 2023-24 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the [Apache License 2.0](https://opensource.org/license/apache-2-0/).
