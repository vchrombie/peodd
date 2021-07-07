# peodd

poetry export, but only for dev-dependencies

Script to export the pyproject.toml dev-dependencies to a txt file.

This software is licensed under GPL3 or later.

## Requirements

 * Python >= 3.6
 * Poetry >= 1.0
 * tomlkit >= 0.5.8
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
