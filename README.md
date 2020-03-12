# Az.Cli

Python [azure.cli.core](https://github.com/Azure/azure-cli/blob/dev/src/azure-cli-core/azure/cli/core/__init__.py) interface to execute `az` [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) commands in python.

## Prerequisites

- install [python3](https://www.python.org/downloads/)
- install `REQUIREMENTS.txt` use `make init`
- login to azure using `az login` (this can also be done interactively using the library) see [Sign in using a service principal](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest#sign-in-using-a-service-principalt)
- run `python3 src`

## Example

```python
from az.cli import az, ExitStatus
# AzResult = namedtuple('AzResult', ['exit_code', 'out', 'log'])
exit_code, result_dict, logs = az("group show -n test")
```

You can run the command interactively to traverse the dictionary.  
Navigate to `src`, run `python3`.  
Import the library `from az.cli import az`, run  `az` command by invoke `az("<my command>")` to invoke Azure CLI.  

```python
# cd src
# python3
from az.cli import az
az("group list") # list return tuple (exitCode, resultSet)
az("group list")[1] # return resultSet content <dict>
az("group list")[1][0]['id'] # Enumerate id of first element in resultSet
```