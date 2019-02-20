#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    bonfire.py [-v | -vv | -vvv] [-f] [--dry-run] [--config path] [--doc] [--mf format] <Command>
    bonfire.py -h | --help | --version
Options:
  -h --help              - Show this message
  -f                     - Force command actions
  -v                     - Verbose mode (vvv for more detail level)
  --dry-run              - Create configuration files only, does not upload any configuration
  --config               - Configuration file path
  --doc                  - Process documentation folder, this will create an alert matrix file
  --mf format            - Define which alert matrix format to use (xlsx, csv, wiki. default: wiki)
  --version              - Version
Command:
  init                   - Create configuration files and directories
  deploy                 - Deploy monitoring stack
  remove                 - Remove all configurations and stack deployed
  plugins                - Show a list of available plugins
"""
"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
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

    raise Exception("[critical] Error importing library: {}".format(e))


# Everything starts here
def main(args):

    # Check command value
    command = args['<Command>']
    menu = Menu.Menu()

    # Force option
    overwrite = args['-f']

    # Deploy documentation
    deploy_documentation = args['--doc']

    # Alert matrix format
    alert_matrix_format = args['--mf']

    # Verbose level
    if args['-v'] == 0:
        logging.getLogger().setLevel(logging.CRITICAL)
        SetupLogger.logger.info("Setting logging level to CRITICAL")
    if args['-v'] == 1:
        logging.getLogger().setLevel(logging.INFO)
        SetupLogger.logger.info("Setting logging level to INFO")
    if args['-v'] == 2:
        logging.getLogger().setLevel(logging.WARN)
        SetupLogger.logger.info("Setting logging level to WARNNING")
    if args['-v'] == 3:
        logging.getLogger().setLevel(logging.DEBUG)
        SetupLogger.logger.info("Setting logging level to DEBUG")

    # Dry run option
    dry_run = args['--dry-run']

    # Configuration file

    if args['--config']:
        config_file_path = args['--config']
    else:
        config_file_path = Settings.CONFIGURATION_FILE_PATH

    # Process command
    if command:
        menu.process_command(command, overwrite=overwrite, config_file_path=config_file_path, dry_run=dry_run,
                             deploy_documentation=deploy_documentation, alert_matrix_format=alert_matrix_format)


# Init main
if __name__ == "__main__":
    try:
        args = docopt(__doc__, version=0.1)
        main(args)
    except KeyboardInterrupt:
        exit(0)
else:
    exit(0)
