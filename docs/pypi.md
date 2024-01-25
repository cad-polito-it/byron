[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/cad-polito-it/byron/pytest.yml?label=pytest)
](https://github.com/cad-polito-it/byron/actions)
[![Documentation Status](https://readthedocs.org/projects/byron/badge/?version=pre-alpha)](https://byron.readthedocs.io/en/pre-alpha/?badge=pre-alpha)
[![GitHub last commit (alpha)](https://img.shields.io/github/last-commit/cad-polito-it/byron/alpha?label=github+update)](https://github.com/cad-polito-it/byron/pulse)
![PyPI - Downloads](https://img.shields.io/pypi/dm/byron?label=pypi+downloads)



Byron is an [evolutionary tool](https://cad-polito-it.github.io/byron/evolution): given a problem, it first generates a set of random solutions, then iteratively improves them using the results of their evaluations together with structural information. It may be used as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization).

**⚠️ Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active development**

## Installation

As simple as

```
pip install --upgrade byron
```

A few dependencies can enhance Byron functionalities, but are not strictly required. You can get them all with

```
pip install --upgrade "byron[full]"
```

## Documentation

None yet, but some HOWTO's and examples [are available](https://github.com/cad-polito-it/byron/tree/alpha/examples) in the development repo.

## Contacts

* Giovanni Squillero — <giovanni.squillero@polito.it>
* Alberto Tonda — <alberto.tonda@inrae.fr>

## License

Copyright (c) 2023-24 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
