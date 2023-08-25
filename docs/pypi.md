Byron is an [evolutionary tool](https://en.wikipedia.org/wiki/Evolutionary_algorithm): given a problem, it first generates a set of random solutions, then iteratively refines and improves them using the results of their evaluations together with structural information. It may be used as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization).

Byron internally encodes candidate solutions as [typed](https://rcor.me/papers/typed-graph-theory.pdf), [directed](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph) [multigraphs](https://en.wikipedia.org/wiki/Multigraph) and can tackle problems with complex, structured constraints. For instance, it may be used to create realistic programs with loops, interrupts, and recursive subroutines. Gory detail: solutions are heterogeneous [forests](https://en.wikipedia.org/wiki/Tree_(graph_theory)#Forest) with additional edges connecting leaves to generic nodes, possibly not in the same tree.

Candidate solutions are dumped as text and then evaluated by calling a user-defined Python function or by invoking a shell script that may use external proprietary tools. Different types of parallelization are supported out of the box, from simple multithreading to the creation of temporary directories where multiple subprocesses are concurrently [spawned](https://en.wikipedia.org/wiki/Spawn_(computing)).

## Installation

**⚠️ Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active development**

```
pip install --upgrade byron
```

Few optional dependencies can enhance Byron, but are not strictly required:

```
pip install --upgrade matplotlib
pip install --upgrade joblib
pip install --upgrade psutil
```

## Documentation

Some HOWTO's and examples are available as Jupyter notebooks in the [examples directory](https://github.com/cad-polito-it/byron/tree/pre-alpha/examples/notebooks).

## Contacts

* Giovanni Squillero — <giovanni.squillero@polito.it>
* Alberto Tonda — <alberto.tonda@inrae.fr>

## License

Copyright (c) 2023 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
