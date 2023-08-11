Byron is an [evolutionary tool](https://en.wikipedia.org/wiki/Evolutionary_algorithm): given a problem, it first creates a set of random solutions, then iteratively refines and enhances them using the result of their evaluations together with structural information. 

Byron is able to tackle problem those solutions are simple fixed-length bit strings, as well as to optimize realistic assembly programs including loops, interrupts and recursive sub routines. It can be exploited as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and as a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization), or as a framework for prototyping and testing new ideas.

Candidate solutions can seamlessly be evaluated in parallel using external scripts, for instance calling proprietary tools. 


### Installation

##### ⚠️ Byron is currently in [pre-alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Pre-alpha) and under active development

```
pip install --upgrade byron
```

Few optional dependencies can enhance byron, but are not strictly required:

```
pip install --upgrade matplotlib
pip install --upgrade joblib
pip install --upgrade psutil
```

### Contacts

* [Alberto Tonda](https://github.com/albertotonda/) [<alberto.tonda@inra.fr>](mailto:alberto.tonda@inra.fr)
* [Giovanni Squillero](https://github.com/squillero) [<giovanni.squillero@polito.it>](giovanni.squillero@polito.it)

### License

**Copyright © 2023 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)**  
byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
