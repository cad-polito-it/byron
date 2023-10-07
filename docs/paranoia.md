> *All day long I think of things*  
> *But nothing seems to satisfy*  
> *Think I'll lose my mind if I don't*  
> *Find something to pacify*  
> 
> *Can you help me occupy my brain?*  
> *Oh, yeah*  

In **production**, Byron is typically run from a non-interactive script, for example on a server with ssh access. In this context, performance is critical, while verbosity should be minimal. During **setup**, on the other hand, the user needs to check the various parameters and the coherence of the constraints. Here, speed is not essential, while warnings and hints can be quite useful. 

Byron's *paranoia checks* are computationally intensive routines that thoroughly analyze and verify both the integrity of internal data structures and parameter values, and provide error messages and hints. *Paranoia checks* are intended to be used during setup and are automatically removed when an optimization flag is specified..

## Terminal

If *paranoia checks* are enabled, the user is warned of the potential, indeed almost certain, loss in performance:

> Paranoia checks are enabled: performances can be significantly impaired — consider using '-O'

Possible solutions:

### Use `-O` flag

Using an optimization flag will disable *Paranoia Checks*:

```sh
$ python -O ./super-fuzzer.py
```

### Set `PYTHONOPTIMIZE`

Setting the environment variable [`PYTHONOPTIMIZE`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE) to a non-empty string it is equivalent to specifying the `-O` option:

```sh
$ PYTHONOPTIMIZE=1 python ./super-fuzzer.py
```

## Jupyter Notebooks

By default, code run in IPython is not optimized. Byron should detect when it is executed within a Jupyter Notebook and show a warning:

> Paranoia checks are enabled in this notebook: performances can be significantly impaired

Possible solutions:

### Export to a script

Probably the best solution:

* In Jupyter, from menu `File`, choose `Save and Export Notebook As...`, and then `Executable Script`.
* Enable optimization when running the script from the terminal (see above).

### Set `PYTHONOPTIMIZE`

Set [`PYTHONOPTIMIZE`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE) before starting Jupyter:

```shell
$ PYTHONOPTIMIZE=1 jupyter-notebook
```

⚠️ This will disable every single `assert` in notebooks: the behavior of other modules will be affected as well.

### Use magic

Jupyter allows some of the IPython's [magics](https://ipython.readthedocs.io/en/stable/interactive/magics.html), and a *cell magic* (`%%`) can be used to start a Python interpreter with an optimization flag:

```jupyterpython
%%python -O

import byron

# Fuzzer code
```

* 👍 May be used in remote Notebooks (e.g., [Google's Colab](https://colab.research.google.com/))
* 👎 All the code must be packed into one single cell
* 👍 Byron will not detect Jupyter anymore

### Tamper with the bytecode cache 💣

⚠️ This hack may cause your system to become unstable and provide incorrect results. You acknowledge that you are solely responsible for any harm or damage that may result.

* Generate the optimized bytecode (e.g., run `python -O -m pytest`)
* Locate all the folders that contain compiled bytecode (e.g., `**/__pycache__`)
* Substitute all bytecode-compiled files (e.g., `*.pyc`) with their optimized versions (e.g., `*.opt-1.pyc`)
