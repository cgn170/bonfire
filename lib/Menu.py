#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

from lib import Settings
from lib import KickOff
from lib import Alerts
from lib import Documentation
from lib import Operations
from lib import Utils


# Menu class, contains methods for menu
class Menu:

    def __init__(self):
        pass

    # Process each available command
    def process_command(self, command="", overwrite=False, config_file_path=Settings.CONFIGURATION_FILE_PATH,
                        dry_run=True, deploy_command="all", alert_matrix_format="wiki"):

        kickoff = KickOff.KickOff()
        alerts = Alerts.Alerts()
        documentation = Documentation.Documentation()
        operations = Operations.Operations()

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
                operations.process_operations_deployment(config_file_path,
                                                         dry_run,
                                                         "deploy")

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
                operations.process_operations_deployment(config_file_path,
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
                operations.process_operations_deployment(config_file_path,
                                                         dry_run,
                                                         "remove")

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
                operations.process_operations_deployment(config_file_path,
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

            print("\n")

        else:
            print("[error] Command: '{}' not found, exiting ...".format(command))
            exit(1)
