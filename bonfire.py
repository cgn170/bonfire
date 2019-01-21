#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    bonfire.py [-f] [-v level] [--config path] <Command>
    bonfire.py -h | --help | --version
Options:
  -h --help  - Show this message
  -v         - Verbose mode level [ 1(info), 2(warning), 3(debug)]
  -f         - Force command actions
  --config   - Configuration file path
  --version  - Version
Command:
  init       - Create configuration files and directories
  deploy     - Deploy monitoring stack
  remove     - Remove all configurations and stack deployed
  plugins    - Show a list of available plugins
"""
try:
    import os
    import sys
    import warnings
    from lib import Menu
    from lib import Settings
    from lib import SetupLogger
    from docopt import docopt
    import logging

    warnings.filterwarnings(action="ignore", message=".* it was already imported", category=UserWarning)
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)

except KeyboardInterrupt:
    SetupLogger.logger.error("User aborted")
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

    # Verbose level
    verbose = args['-v']

    # Configuration file

    if args['--config']:
        config_file_path = args['--config']
    else:
        config_file_path = Settings.CONFIGURATION_FILE_PATH

    # Process command
    if command:
        menu.process_command(command, overwrite=overwrite, config_file_path=config_file_path)


# Init main
if __name__ == "__main__":
    try:
        args = docopt(__doc__, version=0.1)
        main(args)
    except KeyboardInterrupt:
        exit(0)
else:
    exit(0)
