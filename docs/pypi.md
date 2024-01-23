[![License](https://img.shields.io/badge/license-apache--2.0-green.svg)](https://opensource.org/licenses/Apache-2.0) 
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/cad-polito-it/byron)
![Language](https://img.shields.io/badge/language-python-blue.svg)
![Version](https://img.shields.io/badge/version-0.8a1.dev41-orange.svg)
![Codename](https://img.shields.io/badge/codename-Don_Juan-pink.svg)
[![Documentation Status](https://readthedocs.org/projects/byron/badge/?version=pre-alpha)](https://byron.readthedocs.io/en/pre-alpha/?badge=pre-alpha)


Byron is an [evolutionary tool](https://cad-polito-it.github.io/byron/evolution): given a problem, it first generates a set of random solutions, then iteratively improves them using the results of their evaluations together with structural information. It may be used as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization).

**⚠️ Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active development**

## Installation

As simple as

```
pip install --upgrade byron
```

Few dependencies can enhance Byron, but are not strictly required. You can get them with

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
