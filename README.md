`byron` 🖋
==========

![Version](https://img.shields.io/badge/version-0.8a1.dev40_(Don_Juan)-orange.svg)
[![GitHub last commit (alpha)](https://img.shields.io/github/last-commit/cad-polito-it/byron/alpha)](https://github.com/cad-polito-it/byron/pulse)
[![License](https://img.shields.io/badge/license-apache--2.0-green.svg)](https://opensource.org/licenses/Apache-2.0) 
[![Language](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org/)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/cad-polito-it/byron/pytest.yml?label=pytest)
](https://github.com/cad-polito-it/byron/actions)
[![Documentation Status](https://readthedocs.org/projects/byron/badge/?version=pre-alpha)](https://byron.readthedocs.io/en/pre-alpha/?badge=pre-alpha)

Byron is an [evolutionary tool](https://cad-polito-it.github.io/byron/evolution): given a problem, it first generates a set of random solutions, then iteratively improves them using the results of their evaluations together with structural information. It may be used as a coverage-driven [fuzzer](https://en.wikipedia.org/wiki/Fuzzing) and a general-purpose [optimizer](https://en.wikipedia.org/wiki/Engineering_optimization).

:package: The Python package is available on [PyPi](https://pypi.org/project/byron/); this repo is only useful if you want to hack the code. 

### TL;DR

* Byron is currently in [alpha](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha) and under active development
* The default branch is always the more stable
* Do not clone experimental branches `exp/*` unless you know what you are doing
* Follow this [style guide](https://github.com/squillero/style/blob/master/python.md) and keep the code formatted with [Black](https://black.readthedocs.io/en/stable/)
* Write as few lines of code and as many lines of comments as possible (i.e., use builtins, exploit generators and list comprehension)
* Be [paranoid](https://cad-polito-it.github.io/byron/paranoia) (cit. *"I need someone to show me the things"*)
* Use [pytest](https://docs.pytest.org/) and [Coverage.py](https://coverage.readthedocs.io/) for unit testing (ie. `coverage run -m pytest`)
* Use [pylint](https://mypy-lang.org/) for basic linting and [mypy](https://mypy-lang.org/) for additional type checking
* Use [direnv](https://direnv.net) to patch environment variables 
* And remember that it may be wise to contact [Giovanni](https://github.com/squillero) before trying to change anything

### Contacts

* [Giovanni Squillero](https://github.com/squillero) [:email:](mailto:giovanni.squillero@polito.it) [:house:](https://staff.polito.it/giovanni.squillero/)
* [Alberto Tonda](https://github.com/albertotonda/) [:email:](mailto:alberto.tonda@inrae.fr) [:house:](https://www.researchgate.net/profile/Alberto_Tonda)

### Licence
Copyright (c) 2023 [Giovanni Squillero](https://github.com/squillero) and [Alberto Tonda](https://github.com/albertotonda/)  
Byron is [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software), and it is distributed under the permissive [Apache License 2.0](https://opensource.org/license/apache-2-0/).
