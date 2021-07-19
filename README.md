# peodd 

[![PyPI version](https://badge.fury.io/py/peodd.svg)](https://badge.fury.io/py/peodd) 
[![Coverage Status](https://coveralls.io/repos/github/vchrombie/peodd/badge.svg?branch=master)](https://coveralls.io/github/vchrombie/peodd?branch=master)

poetry export, but only for dev-dependencies

Script to export the pyproject.toml dev-dependencies to a txt file.

This software is licensed under GPL3 or later.

**Note:** Right now, this tool supports only some poetry formats of the dependencies (specifically 
`foo = '^n.n.n'`, `foo = '>=n.n.n'`, `foo = 'n.n.n'`). I would be interested to add support 
for more formats, please [open an issue](https://github.com/vchrombie/peodd/issues/new) incase 
if you need any other. 

## Requirements

 * Python >= 3.6
 * Poetry >= 1.0
 * tomli >= 1.0.4
 * Click >= 7.0.0
 * release-tools >= 0.3.0

## Installation

### PyPI

You can install the package directly using pip.
```
$ pip install peodd
```

### Getting the source code

Clone the repository
```
$ git clone https://github.com/vchrombie/peodd/
$ cd peodd/
```

### Prerequisites

#### Poetry

We use [Poetry](https://python-poetry.org/docs/) for managing the project.
You can install it following [these steps](https://python-poetry.org/docs/#installation).

We use [Bitergia/release-tools](https://github.com/Bitergia/release-tools) for managing 
the releases. This is also used in the project, so you need not install it again.

### Installation

Install the required dependencies (this will also create a virtual environment)
```
$ poetry install
```

Activate the virtual environment
```
$ poetry shell
```

## Usage

Once you install the tool, you can use it with the `peodd` command.
```
$ peodd --help
Usage: peodd [OPTIONS]

  Script to export the pyproject.toml dev-dependencies to a txt file.

Options:
  -o, --output TEXT  Output file for the dependencies  [default: requirements-
                     dev.txt]

  --help             Show this message and exit.
```

Export the dev-dependencies to `requirements-dev.txt` file
```
$ peodd -o requirements-dev.txt
```

## Contributions

All contributions are welcome. Please feel free to open an issue or a PR. 
If you are opening any PR for the code, please be sure to add a 
[changelog](https://github.com/Bitergia/release-tools#changelog) entry.

## License

Licensed under GNU General Public License (GPL), version 3 or later.
