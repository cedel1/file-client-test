# file-client

[![PyPI](https://img.shields.io/pypi/v/file-client.svg)](https://pypi.org/project/file-client/)
[![Changelog](https://img.shields.io/github/v/release/cedel1/file-client?include_prereleases&label=changelog)](https://github.com/cedel1/file-client/releases)
[![Tests](https://github.com/cedel1/file-client/workflows/Test/badge.svg)](https://github.com/cedel1/file-client/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/cedel1/file-client/blob/master/LICENSE)

CLI application which retrieves and prints data from one of the described backends

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
