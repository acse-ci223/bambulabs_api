# Bambulabs API

This package provides a Python API for the Bambulabs 3D Printers via MQTT.

## Status

[![flake8](https://github.com/acse-ci223/bambulabs_api/actions/workflows/flake8.yml/badge.svg)](https://github.com/acse-ci223/bambulabs_api/actions/workflows/flake8.yml)

[![pytest-unit-tests](https://github.com/acse-ci223/bambulabs_api/actions/workflows/pytest-unit-tests.yml/badge.svg)](https://github.com/acse-ci223/bambulabs_api/actions/workflows/pytest-unit-tests.yml)

[![GitHub Pages](https://github.com/acse-ci223/bambulabs_api/actions/workflows/static.yml/badge.svg)](https://github.com/acse-ci223/bambulabs_api/actions/workflows/static.yml)



## Documentation

The documentation for this package can be found [here](https://acse-ci223.github.io/bambulabs_api/).

## Usage

To use the package, run the following command in the terminal:

```bash
pip install bambulabs_api
```

## Development

To install the package, make sure conda is installed and then run the following commands in the terminal:

```bash
# Clone the repository
git clone https://github.com/acse-ci223/bambulabs_api.git

# Change directory
cd bambulabs_api

# Create the 'parally' environment
conda env create -f environment.yml

# Activate the environment
conda activate blapi

# Install the package
pip install -e .
```

## Examples

