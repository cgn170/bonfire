#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    bonfire.py [-v | -vv | -vvv] [-f] [--config path] [--dry-run] <Command>
    bonfire.py -h | --help | --version
Options:
  -h --help   - Show this message
  -f          - Force command actions
  -v          - Verbose mode (vvv for more detail level)
  --dry-run   - Create configuration files only, does not upload any configuration
  --config    - Configuration file path
  --version   - Version
Command:
  init        - Create configuration files and directories
  deploy      - Deploy monitoring stack
  remove      - Remove all configurations and stack deployed
  plugins     - Show a list of available plugins
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
    if args['-v'] == 0:
        logging.getLogger().setLevel(logging.CRITICAL)
    if args['-v'] == 1:
        logging.getLogger().setLevel(logging.INFO)
    if args['-v'] == 2:
        logging.getLogger().setLevel(logging.WARN)
    if args['-v'] == 3:
        logging.getLogger().setLevel(logging.DEBUG)


    # Dry run option
    dry_run = args['--dry-run']

    # Configuration file

    if args['--config']:
        config_file_path = args['--config']
    else:
        config_file_path = Settings.CONFIGURATION_FILE_PATH

    # Process command
    if command:
        menu.process_command(command, overwrite=overwrite, config_file_path=config_file_path, dry_run=dry_run)


# Init main
if __name__ == "__main__":
    try:
        args = docopt(__doc__, version=0.1)
        main(args)
    except KeyboardInterrupt:
        exit(0)
else:
    exit(0)
