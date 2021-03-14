# --------------------------------------------------------------------------------------------
# Copyright (c) Mark Warneke <warneke.mark@gmail.com> 2020
# Licensed under the MIT License. See License.txt in the project root for license information.
# Contribution Jiashuo Li https://github.com/jiasli/pyaz
# Based on https://github.com/Azure/azure-cli/blob/dev/src/azure-cli-core/azure/cli/core/__init__.py
# commit 8e369b9d2d63ddf5c6678ee710905bf9e5028f99
# --------------------------------------------------------------------------------------------

import sys
from io import StringIO
import json
import shlex
import logging
from collections import namedtuple

from azure.cli.core import get_default_cli
from knack.log import CLI_LOGGER_NAME



AzResult = namedtuple('AzResult', ['exit_code', 'result_dict', 'log'])

# adjust the logging level if you want INFO or DEBUG log
logging_level = logging.WARNING

SUCCESS_CODE = 0


def main():
    error_code, result_dict, log = az(sys.argv[1])

    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    if error_code == SUCCESS_CODE:
        pp.pprint(result_dict)
    else:
        print(log)


def az(command):
    """
    Invoke Azure CLI command with a Python function call "az" command based on argument
    Reference can be found here:
    https://github.com/Azure/azure-cli/blob/dev/src/azure-cli-testsdk/azure/cli/testsdk/base.py#L252
    commit fc532b4dee320e7f20994d548f284729a0c66ae8

    exit_code can be one of
        0: succeed
        1: request error
        2: command parsing error
        3: resource doesn't exist

    For example:
        `az("group show -n mygroup")`

    :param command: the command string, without az
    :return: a named tuple consisting of exit_code, out and log
    """

    # Create default shell to run commands
    _cli = get_default_cli()

    # Create string buffer to get the result and logs
    stdout_buf = StringIO()
    log_buf = StringIO()

    # root logger only keeps CRITICAL
    root_logger = logging.getLogger()
    root_handler = logging.StreamHandler(stream=log_buf)
    root_handler.setLevel(logging.CRITICAL)
    root_logger.addHandler(root_handler)

    # cli logger keeps WARNING and above
    cli_logger = logging.getLogger(CLI_LOGGER_NAME)
    cli_handler = logging.StreamHandler(stream=log_buf)
    cli_handler.setLevel(logging_level)
    cli_logger.addHandler(cli_handler)

    try:
        # Split command https://docs.python.org/3/library/shlex.html#shlex.split
        args = shlex.split(command)

        # FIXME: Intercept 'loging' command, it blocks the execution

        # exit code 0 or 1
        exit_code = _cli.invoke(
            args, out_file=stdout_buf) or SUCCESS_CODE

    except SystemExit as ex:
        # exit code 2 or 3, generated by sys.exit()
        exit_code = ex.code
        pass

    root_logger.removeHandler(root_handler)
    cli_logger.removeHandler(cli_handler)

    return AzResult(exit_code, _parseResult(stdout_buf), log_buf.getvalue())


def _parseResult(buffer):
    """
    Parse the string buffer content into a dict using json.loads

    :param buffer: The StringIO buffer to retrieve value

    :return: dict of values
    """
    try:
        # Retrieve output buffer
        output = buffer.getvalue()

        # Turn json string from output into dict
        if output != "":    
            return json.loads(output)
        else:
            return json.loads("{}")
    except SystemExit as ex:
        raise BaseException("Error load value from StringIO {}".format(ex))


if __name__ == "__main__":
    main()
