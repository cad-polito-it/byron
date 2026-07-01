# Byron v0.8a1.dev67 *"Don Juan"*

Byron is a source code [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) designed to support assembly or higher level languages. It starts by generating a set of random programs, which are then iteratively improved by an [evolutionary algorithm](https://cad-polito-it.github.io/byron/evolution). Internally, it encodes candidate solutions as [typed](https://rcor.me/papers/typed-graph-theory.pdf), [directed](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph) [multigraphs](https://en.wikipedia.org/wiki/Multigraph), and can effectively handle complex, realistic structures containing local and global variables, conditional and looping statements, and subroutines.

Programs can be evaluated using a user-defined Python function or an external tool, such as an interpreter or a simulator. Different types of parallelization are supported out of the box, from simple multithreading to the creation of temporary directories where multiple subprocesses are concurrently [spawned](https://en.wikipedia.org/wiki/Spawn_(computing)).

Byron, formerly known as [MicroGP](https://github.com/microgp) v4, was made possible by the contributions of [many individuals](contributors) over [many years](history). 

### Installation and Usage

**⚠️ Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active development**

The Python package is available on [PyPi](https://pypi.org/project/byron/), the source code is on [GitHub](https://github.com/cad-polito-it/byron).

### Contacts

* Giovanni Squillero — <giovanni.squillero@polito.it>
* Alberto Tonda — <alberto.tonda@inrae.fr>

### License

Copyright (c) 2023-24 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the [Apache License 2.0](https://opensource.org/license/apache-2-0/).
