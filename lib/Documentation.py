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
from lib import AlertMatrix


# Documentation class, contains methods to deploy
class Documentation:

    def __init__(self):

        pass

    # Here is the logic to deploy all documentation
    def process_documentation_deployment(self, config_file_path, alert_matrix_format, dry_run, option):

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

        # Validate if the value exist if don't use default
        if not config.get('documentation_dir', False):
            documentation_dir = Settings.CONFIGURATION_FOLDERS["documentation"].get('folder')
            SetupLogger.logger.debug(
                "Variable documentation_dir not defined, using default value: {}".format(documentation_dir))
        else:
            documentation_dir = config.get('documentation_dir')
            SetupLogger.logger.debug("documentation_dir defined, using value: {}".format(documentation_dir))
        # Validate if the dir is valid
        if not os.path.isdir(documentation_dir):
            print("[error] Documentation directory is not valid, exiting ...")
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
        documentation_list_file = Utils.list_files_in_directory(documentation_dir, "")

        if len(documentation_list_file):
            print("[-] Documentation files found: {}".format(len(documentation_list_file)))
        else:
            print("[warning] No documentation file found, is recommended to use some documentation for each alert "
                  "(Optional) ...")

        # Check if upload_documentation variable is available
        upload_documentation = config.get('upload_documentation', False)

        # Check if documentation_plugin variable is available
        documentation_plugin = config.get('documentation_plugin', Settings.DEFAULT_DOCUMENTATION_PLUGIN)

        # Process each file
        # for documentation_file_path in documentation_list_file:
        #    print(documentation_file_path)

        # Create alert matrix
        print("[-] Creating alert matrix ...")

        alert_matrix = AlertMatrix.AlertMatrix()

        # Default value is wiki
        if alert_matrix_format is None:
            alert_matrix_format = "wiki"

        matrix_output_path = os.path.join(Settings.CONFIGURATION_HIDDEN_FOLDER_DEPLOYMENT,
                                          "alert_matrix.{}".format(alert_matrix_format))

        # Create alert matrix in local directory
        alert_matrix.create_alert_matrix(alerts_dir, alert_matrix_format, matrix_output_path)

        # Deploy documentation to confluence
        if not dry_run and upload_documentation:

            plugin_folder_path = Settings.DOCUMENTATION_PLUGINS_PATH
            plugin_package = "lib.plugins.documentation"

            # Get information about what plugins are available in the folder
            # plugins_available = Utils.get_list_plugins(plugin_folder_path)
            # print("[*] Plugins loaded: {}".format(",".join(plugins_available.keys())))

            plugins_modules = Utils.load_plugins(plugin_package, plugin_folder_path)

            # Plugin configuration variables
            plugin_configuration_variables = config.get(documentation_plugin.lower(), None)

            if option == "deploy":
                print("[plugin] Processing {} plugin".format(documentation_plugin))
                plugins_modules[documentation_plugin].deploy(dry_run,
                                                             plugin_configuration_variables,
                                                             "passwords")
                print("[plugin] Finished {} plugin".format(documentation_plugin))

            elif option == "remove":

                # Call remove function inside the plugin
                print("[plugin] Processing {} plugin".format(documentation_plugin))
                plugins_modules[documentation_plugin].remove(dry_run,
                                                             plugin_configuration_variables,
                                                             "passwords")
                print("[plugin] Finished {} plugin".format(documentation_plugin))
            else:
                print("[error] Plugin option not available: {}".format(option))
