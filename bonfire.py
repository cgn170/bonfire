#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    bonfire.py [-vf] [--config path] <Command>
    bonfire.py -h | --help | --version
Options:
  -h --help  - Shows this message
  -v         - Verbose mode
  -f         - Force command actions
  --config   - Configuration file path
  --version  - Version
Command:
  init       - Create configuration files and directories
  deploy     - Deploy IT Operations stack
  remove     - Remove all configurations and stack created
  plugins    - Show a list of available plugins
"""
try:
    import os
    import sys
    import warnings
    from lib import Menu
    from lib import SetupLogger
    from docopt import docopt
    import logging

    warnings.filterwarnings(action="ignore", message=".* it was already imported", category=UserWarning)
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)

except KeyboardInterrupt:
    errMsg = "user aborted"
except ImportError as e:

    SetupLogger.logger.error("Error importing library: {}".format(e))

    raise Exception("Error importing library: {}".format(e))


# Everything starts here
def main(args):

    # Check command value
    command = args['<Command>']
    menu = Menu.Menu()

    # Force option
    overwrite = args['-f']

    # Process command
    if command:
        menu.process_command(command, overwrite)


# Init main
if __name__ == "__main__":
    try:
        args = docopt(__doc__, version=0.1)
        main(args)
    except KeyboardInterrupt:
        exit(0)
else:
    exit(0)
