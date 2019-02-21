#!/usr/bin/env python

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

from lib import KickOff
from lib import Deployment
from lib import Settings
from lib import Documentation
import sys
sys.path.append("..")


class Menu:

    def __int__(self, args):
        pass

    # Process each available command
    def process_command(self, command="", overwrite=False, config_file_path=Settings.CONFIGURATION_FILE_PATH,
                        dry_run=True, deploy_documentation=False, alert_matrix_format="wiki"):

        kickoff = KickOff.KickOff()
        deployment = Deployment.Deployment()
        documentation = Documentation.Documentation()

        print("[-] Welcome to Bonfire Project!")

        if command == "init":
            print("[*] Creating configuration files, please wait ...")
            kickoff.create_started_files(overwrite)

        elif command == "deploy":
            print("[*] Deploying all stack, please wait ...")
            deployment.process_alerts_deployment(config_file_path, dry_run)

            if deploy_documentation:
                print("[*] Creating documentation, please wait ...")
                documentation.process_documentation_deployment(config_file_path, alert_matrix_format, dry_run)

        elif command == "remove":
            print("[*] Removing all deployments, please wait ...")
            deployment.remove_alerts_deployment(config_file_path, dry_run)

        elif command == "plugins":
            print("[+] Available plugins: ")
            for plugin in deployment.get_list_information_plugins():
                print("[-] [{0}]: {1}".format(plugin["name"], plugin["desc"]))

        else:
            print("[error] Command: '{}' not found, exiting ...".format(command))
            exit(1)
