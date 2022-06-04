# Motor Stubs

Experimental stubs for [motor](https://pypi.org/project/motor/).


**motor-stubs is NOT an officially supported MongoDB product.**


## Installation

`motor-stubs` can be installed with [pip](https://pypi.org/project/pip/)

```shell
pip install motor-stubs
```

## Dependencies

- Python >= 3.9
- Motor >= 3.0.0, < 4.0

## Note

1. You should not use this stubs package after the official `motor` package supports inline type annotations.
2. File [generator.py](/generator.py) can help to parse class `AgnosticCollection` and `AgnosticDatabase`,
   other class might not work

### Usage `generator.py`

```python
# at the project root, and get into python shell
from motor.core import AgnosticCollection
from generator import gen

gen(AgnosticCollection)
```

It will output a file in folder `pyi_tmp/`.

## Support / Feedback

motor-stubs is experimental and is not an officially supported MongoDB product.
For questions, discussions, or general technical support, visit the [MongoDB Community Forums](https://developer.mongodb.com/community/forums/tag/python).

## Contribute

### Poetry

use `poetry` as package manager, you can follow the official installation guide [here](https://github.com/python-poetry/poetry)

### Pre-Commit

use Python package `pre-commit` for style check

```shell
# after install poetry

# install project dependencies
poetry install
# then
pre-commit install
```

### Commitizen

use Python package `commitizen` for commit-msg lint and version bump tool

#### commit

```shell
cz c
# follow the description
```

#### bump version

```shell
cz bump
```
