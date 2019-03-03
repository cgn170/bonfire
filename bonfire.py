#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    bonfire.py [-v | -vv | -vvv] [-f] [--dry-run] [--config path] [--mf format] <Command> [<Deploy>]
    bonfire.py -h | --help | --version
Options:
  -h --help              - Show this message
  -f                     - Force command actions
  -v                     - Verbose mode (vvv for more detail level)
  --dry-run              - Create configuration files only, does not upload any configuration
  --config               - Configuration file path
  --version              - Version
Command:
  init                   - Create configuration files and directories.
  deploy                 - Deploy monitoring stack.
  remove                 - Remove all configurations and stack deployed.
  plugins                - Show a list of available plugins.
Deploy:
  all                    - Default option (Can be empty), deploy everything.
  alerts                 - Deploy only alerts.
  documentation          - Create the alert matrix and upload all documentation (Deploy only documentation).
  operations             - Deploy operation stack configuration.
Documentation:
  --mf format            - Define which alert matrix format to use (xlsx, csv, wiki. default: wiki)

"""
"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
try:
    import os
    import sys
    import warnings
    from lib import Settings
    from lib import SetupLogger
    from docopt import docopt
    from lib import KickOff
    from lib import Alerts
    from lib import Documentation
    from lib import Operations
    from lib import Utils
    import logging
    sys.path.append("..")

    warnings.filterwarnings(action="ignore", message=".* it was already imported", category=UserWarning)
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)

except KeyboardInterrupt:
    raise Exception("[critical] User aborted")
except ImportError as e:
    raise Exception("[critical] Error importing library: {}".format(e))


# Everything starts here
def main(args):

    # Check command value
    command = args['<Command>']

    # Force option
    overwrite = args['-f']

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

    # Deploy command
    if args['<Deploy>']:
        deploy_command = args['<Deploy>']
    else:
        deploy_command = "all"

    # Process command
    if command:
        process_command(command, overwrite=overwrite, config_file_path=config_file_path, dry_run=dry_run,
                        deploy_command=deploy_command, alert_matrix_format=alert_matrix_format)


# Process each available command
def process_command(command="", overwrite=False, config_file_path=Settings.CONFIGURATION_FILE_PATH,
                    dry_run=True, deploy_command="all", alert_matrix_format="wiki"):

    kickoff = KickOff.KickOff()
    alerts = Alerts.Alerts()
    documentation = Documentation.Documentation()

    print("[-] Welcome to Bonfire Project!")

    if command == "init":
        print("[init] Creating configuration files, please wait ...")
        kickoff.create_started_files(overwrite)

    elif command == "deploy":

        if deploy_command == "documentation":
            print("[deploy] Deploying documentation, please wait ...")
            documentation.process_documentation_deployment(config_file_path,
                                                           alert_matrix_format,
                                                           dry_run,
                                                           "deploy")

        elif deploy_command == "operations":
            print("[deploy] Deploying operations, please wait ...")

        elif deploy_command == "alerts":
            print("[deploy] Deploying alerts, please wait ...")
            alerts.process_alerts_deployment(config_file_path,
                                             dry_run,
                                             "deploy")

        elif deploy_command == "all":
            print("[deploy] Deploying all stack, please wait ...")

            documentation.process_documentation_deployment(config_file_path,
                                                           alert_matrix_format,
                                                           dry_run,
                                                           "deploy")

            alerts.process_alerts_deployment(config_file_path,
                                             dry_run,
                                             "deploy")

        else:
            print("[error] Deploy command: '{}' not found, exiting ...".format(deploy_command))
            exit(1)

    elif command == "remove":

        if deploy_command == "documentation":
            print("[deploy] Removing documentation, please wait ...")
            documentation.process_documentation_deployment(config_file_path,
                                                           alert_matrix_format,
                                                           dry_run,
                                                           "remove")

        elif deploy_command == "operations":
            print("[deploy] Removing operations, please wait ...")

        elif deploy_command == "alerts":
            print("[deploy] Removing alerts, please wait ...")
            alerts.process_alerts_deployment(config_file_path,
                                             dry_run,
                                             "remove")

        elif deploy_command == "all":
            print("[deploy] Removing all stack, please wait ...")

            documentation.process_documentation_deployment(config_file_path,
                                                           alert_matrix_format,
                                                           dry_run,
                                                           "remove")
            alerts.process_alerts_deployment(config_file_path,
                                             dry_run,
                                             "remove")

    elif command == "plugins":

        print("\n[plugins] Documentation plugins available: ")
        for plugin in Utils.get_list_information_plugins("lib.plugins.documentation",
                                                         Settings.DOCUMENTATION_PLUGINS_PATH):
            print("[{0}]: {1}".format(plugin["name"], plugin["desc"]))

        print("\n[plugins] Operation plugins available: ")
        for plugin in Utils.get_list_information_plugins("lib.plugins.operations",
                                                         Settings.OPERATION_PLUGINS_PATH):
            print("[{0}]: {1}".format(plugin["name"], plugin["desc"]))

        print("\n[plugins] Alert plugins available: ")
        for plugin in Utils.get_list_information_plugins("lib.plugins.alerts", Settings.ALERT_PLUGINS_PATH):
            print("[{0}]: {1}".format(plugin["name"], plugin["desc"]))

    else:
        print("[error] Command: '{}' not found, exiting ...".format(command))
        exit(1)


# Init main
if __name__ == "__main__":
    try:
        args = docopt(__doc__, version=0.1)
        main(args)
    except KeyboardInterrupt:
        exit(0)
else:
    exit(0)
