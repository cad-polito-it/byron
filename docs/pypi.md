Byron is an [evolutionary tool](https://en.wikipedia.org/wiki/Evolutionary_algorithm): given a problem, it first generates a set of random solutions, then iteratively refines and improves them using the results of their evaluations together with structural information.

Byron can solve problems that require solutions with a complex structures, such as realistic assembly programs with loops, interrupts, and recursive subroutines. It may be used as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization), or as a framework for prototyping and testing new ideas.

Candidate solutions are evaluated in parallel using a Python function, an external *makefile*, or a generic shell script that may, for instance, call proprietary tools.

## Installation

**⚠️ Byron is currently in [pre-alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Pre-alpha) and under active development**

```
pip install --upgrade byron
```

Few optional dependencies can enhance byron, but are not strictly required:

```
pip install --upgrade matplotlib
pip install --upgrade joblib
pip install --upgrade psutil
```

## Contacts

* Alberto Tonda: <alberto.tonda@inra.fr>
* Giovanni Squillero: <giovanni.squillero@polito.it>

## License

Copyright © 2023 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
