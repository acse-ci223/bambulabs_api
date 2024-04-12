# Bambulabs API

This package provides a Python API for the Bambulabs 3D Printers.

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

## Examples

```python
import bambulabs_api as bl

IP = '192.168.1.200'
SERIAL = 'AC12309BH109'
ACCESS_CODE = '12347890'

if __name__ == '__main__':
    print('Starting bambulabs_api example')
    print('Connecting to Bambulabs 3D printer')
    print(f'IP: {IP}')
    print(f'Serial: {SERIAL}')
    print(f'Access Code: {ACCESS_CODE}')

    # Create a new instance of the API
    printer = bl.Printer(IP, SERIAL, ACCESS_CODE)

    # Connect to the Bambulabs 3D printer
    printer.connect()

    # Get the printer status
    status = printer.get_state()
    print(f'Printer status: {status}')

    # Disconnect from the Bambulabs 3D printer
    printer.disconnect()
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