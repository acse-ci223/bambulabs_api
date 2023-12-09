# parally
A python package to distribute CPU-intensive tasks by sending workload to other connected computers

## Status

[![flake8](https://github.com/acse-ci223/parally/actions/workflows/flake8.yml/badge.svg)](https://github.com/acse-ci223/parally/actions/workflows/flake8.yml)

[![pytest-unit-tests](https://github.com/acse-ci223/parally/actions/workflows/pytest-unit-tests.yml/badge.svg)](https://github.com/acse-ci223/parally/actions/workflows/pytest-unit-tests.yml)

## Documentation

The documentation for this package can be found [here](https://acse-ci223.github.io/parally/).

## Usage

To use the package, run the following command in the terminal:

```bash
pip install parally
```

## Development

To install the package, make sure conda is installed and then run the following commands in the terminal:

```bash
# Clone the repository
git clone https://github.com/acse-ci223/parally.git

# Change directory
cd parally

# Create the 'parally' environment
conda env create -f environment.yml

# Activate the environment
conda activate parally

# Install the package
pip install -e .
```

## Examples

### Example 1: Distributing a simple task

server.py
```python
from parally import Server

HOST = "localhost"
PORT = 5000

parameters = [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 6}]

def completed_task(result):
    print(result)

server = Server(HOST, PORT)
server.bind_parameters(parameters)
server.on_completed(completed_task)
server.on_error(lambda error: print(error))
server.start()
```

<hr>
client.py

```python
from parally import Client

HOST = "localhost"
PORT = 5000


def my_function(params):
    a = params['a']
    b = params['b']
    return a + b

client = Client(HOST, PORT)
client.run_function(my_function)
client.start()
```