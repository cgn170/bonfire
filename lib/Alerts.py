#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os
from lib import Settings
from lib import SetupLogger
from lib import Utils


class Alerts:

    def __init__(self):

        pass

    # Here is the logic to deploy a deployment
    def process_alerts_deployment(self, config_file_path, dry_run, option):

        # Read configuration file
        config_file = Utils.read_yml_file(config_file_path)

        # Check if the configuration file exist
        if config_file is None:
            print("[error] Configuration file not found: {}, exiting ...".format(config_file_path))
            exit(1)

        config = config_file.get('config')

        # Validate if the value exist if don't use default
        if not config.get('alerts_dir', False):
            alerts_dir = Settings.CONFIGURATION_FOLDERS["alerts"].get('folder')
            SetupLogger.logger.debug("Variable alerts_dir not defined, using default value: {}".format(alerts_dir))
        else:
            alerts_dir = config.get('alerts_dir')
            SetupLogger.logger.debug("Variable alerts_dir defined, using value: {}".format(alerts_dir))
        # Validate if the dir is valid
        if not os.path.isdir(alerts_dir):
            SetupLogger.logger.fatal("Alerts directory is not valid, exiting ...")
            exit(1)

        # Check this **************
        # Validate if the value exist if don't use default
        if not config.get('passwords_file', False):
            passwords_file_path = os.path.join(
                Settings.CONFIGURATION_FOLDERS["passwords"].get('folder'), "passwords.yml")

            SetupLogger.logger.debug("Variable passwords_file not defined, using default value: {}"
                                     .format(passwords_file_path))
        else:
            passwords_file_path = config.get('passwords_file')
            SetupLogger.logger.debug("passwords_file defined, using value: {}".format(passwords_file_path))
        # Validate if the file is valid
        if not os.path.isfile(passwords_file_path):
            print("[error] Passwords file is not valid, exiting ...")
            exit(1)

        # Check alerts file
        alerts_list_file = Utils.list_files_in_directory(alerts_dir)

        if len(alerts_list_file) > 0:
            print("[-] Alerts definition file found: {}".format(len(alerts_list_file)))
        else:
            print("[warning] No alerts definition file found, exiting ...")
            exit(1)


        ######################
        # Process deployment process for each plugin
        ######################

        # Create hidden folder for plugin deployment configuration

        Utils.create_folder(overwrite=False, folder_path=Settings.CONFIGURATION_HIDDEN_FOLDER_DEPLOYMENT)

        plugin_folder_path = Settings.ALERT_PLUGINS_PATH
        plugin_package = "lib.plugins.alerts"

        # Get information about what plugins are available in the folder
        plugins_available = Utils.get_list_plugins(plugin_folder_path)

        print("[*] Plugins loaded: {}".format(",".join(plugins_available.keys())))

        plugins_modules = Utils.load_plugins(plugin_package, plugin_folder_path)

        if option == "deploy":

            for plugin in plugins_available:
                print("[plugin] Processing {} plugin".format(plugin))
                plugins_modules[plugin].deploy(alerts_list_file, passwords_file_path, dry_run)
                print("[plugin] Finished {} plugin".format(plugin))

        elif option == "remove":

            for plugin in plugins_available:
                # Call remove function inside the plugin
                print("[plugin] Processing {} plugin".format(plugin))
                plugins_modules[plugin].remove(passwords_file_path, dry_run)
                print("[plugin] Finished {} plugin".format(plugin))
        else:
            print("[error] Plugin option not available: {}".format(option))
