# file-client

[![PyPI](https://img.shields.io/pypi/v/file-client-test.svg)](https://pypi.org/project/file-client-test/)
[![Changelog](https://img.shields.io/github/v/release/cedel1/file-client-test?include_prereleases&label=changelog)](https://github.com/cedel1/file-client-test/releases)
[![Tests](https://img.shields.io/badge/Tests-Results-darkgreen.svg)](https://github.com/cedel1/file-client-test/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/cedel1/file-client-test/blob/master/LICENSE)

CLI application which retrieves and prints data about files from one of the described backends.

## Installation

Install this tool using `pip`:

    pip install file-client

## Usage

For help, run:

    file-client --help

You can also use:

    python -m file_client --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd file-client
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest

To run the tests with coverage:

    pip install coverage

    pytest --cov=file-client /tests
