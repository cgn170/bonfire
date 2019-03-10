#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os
from lib import Utils
from lib import Settings
from lib import SetupLogger


# Documentation class, contains methods to deploy
class Operations:

    def __init__(self):
        pass

    # Here is the logic to deploy all documentation
    def process_operations_deployment(self, config_file_path, dry_run, option):

        # Read configuration file
        config_file = Utils.read_yml_file(config_file_path)

        # Check if the configuration file exist
        if config_file is None:
            print("[error] Configuration file not found: {}, exiting ...".format(config_file_path))
            exit(1)

        config = config_file.get('config')

        # Validate if the value exist if don't use default
        if not config.get('operations_dir', False):
            operations_dir = Settings.CONFIGURATION_FOLDERS["operations"].get('folder')
            SetupLogger.logger.debug(
                "Variable operations_dir not defined, using default value: {}".format(operations_dir))
        else:
            operations_dir = config.get('operations_dir')
            SetupLogger.logger.debug("operations_dir defined, using value: {}".format(operations_dir))
        # Validate if the dir is valid
        if not os.path.isdir(operations_dir):
            print("[error] Operations directory is not valid, exiting ...")
            exit(1)

        # Validate if the value exist if don't use default
        if not config.get('passwords_file', False):
            passwords_file_path = os.path.join(
                Settings.CONFIGURATION_FOLDERS["passwords"].get('folder'), "passwords.yml")

            SetupLogger.logger.debug("Variable passwords_file not defined, using default value: {}"
                                     .format(passwords_file_path))
        else:
            passwords_file_path = config.get('passwords_file')
            SetupLogger.logger.debug("passwords_file defined, using value: {}".format(passwords_file_path))

        # Load path list file documentation from documentation folder
        documentation_list_file = Utils.list_files_in_directory(operations_dir, "")

        if len(documentation_list_file):
            print("[-] Documentation files found: {}".format(len(documentation_list_file)))
        else:
            print("[warning] No documentation file found, is recommended to use some documentation for each alert "
                  "(Optional) ...")

        # Check if upload_operations variable is available
        upload_operations = config.get('upload_operations', False)

        # Check if operations_plugin variable is available
        operations_plugin = config.get('operations_plugin', Settings.DEFAULT_OPERATIONS_PLUGIN)

        # Deploy operations file to plugin service
        if not dry_run and upload_operations:

            plugin_folder_path = Settings.OPERATION_PLUGINS_PATH
            plugin_package = "lib.plugins.operations"

            # Get information about what plugins are available in the folder
            # plugins_available = Utils.get_list_plugins(plugin_folder_path)
            # print("[*] Plugins loaded: {}".format(",".join(plugins_available.keys())))

            plugins_modules = Utils.load_plugins(plugin_package, plugin_folder_path)

            # Plugin configuration variables
            plugin_configuration_variables = config.get(operations_plugin.lower(), None)

            if option == "deploy":
                print("[plugin] Processing {} plugin".format(operations_plugin))
                plugins_modules[operations_plugin].deploy(dry_run,
                                                          plugin_configuration_variables,
                                                          "passwords")
                print("[plugin] Finished {} plugin".format(operations_plugin))

            elif option == "remove":

                # Call remove function inside the plugin
                print("[plugin] Processing {} plugin".format(operations_plugin))
                plugins_modules[operations_plugin].remove(dry_run,
                                                          plugin_configuration_variables,
                                                          "passwords")
                print("[plugin] Finished {} plugin".format(operations_plugin))
            else:
                print("[error] Plugin option not available: {}".format(option))
