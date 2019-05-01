#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os
from lib import Utils
from lib import Settings
from lib import AlertMatrix
from lib import ConfigFile


# Documentation class, contains methods to deploy
class Documentation:

    def __init__(self):

        pass

    # Here is the logic to deploy all documentation
    def process_documentation_deployment(self, config_file_path, alert_matrix_format, dry_run, option):

        config_obj = ConfigFile.ConfigFIle(config_file_path)

        # Load path list file documentation from documentation folder
        documentation_list_file = Utils.list_files_in_directory(config_obj.documentation_dir, "")

        if len(documentation_list_file):
            print("[-] Documentation files found: {}".format(len(documentation_list_file)))
        else:
            print("[warning] No documentation file found, is recommended to use some documentation for each alert "
                  "(Optional) ...")

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
        alert_matrix.create_alert_matrix(config_obj.alerts_dir, alert_matrix_format, matrix_output_path)

        # Deploy documentation to confluence
        if not dry_run and config_obj.upload_documentation:

            plugin_folder_path = Settings.DOCUMENTATION_PLUGINS_PATH
            plugin_package = "lib.plugins.documentation"

            # Get information about what plugins are available in the folder
            # plugins_available = Utils.get_list_plugins(plugin_folder_path)
            # print("[*] Plugins loaded: {}".format(",".join(plugins_available.keys())))

            plugins_modules = Utils.load_plugins(plugin_package, plugin_folder_path)

            # Plugin configuration variables
            plugin_configuration_variables = config_obj.config_yml.get(config_obj.documentation_plugin.lower(), None)

            if option == "deploy":
                print("[plugin] Processing {} plugin".format(config_obj.documentation_plugin))
                plugins_modules[config_obj.documentation_plugin].deploy(dry_run,
                                                                        plugin_configuration_variables,
                                                                        "passwords")
                print("[plugin] Finished {} plugin".format(config_obj.documentation_plugin))

            elif option == "remove":

                # Call remove function inside the plugin
                print("[plugin] Processing {} plugin".format(config_obj.documentation_plugin))
                plugins_modules[config_obj.documentation_plugin].remove(dry_run,
                                                                        plugin_configuration_variables,
                                                                        "passwords")
                print("[plugin] Finished {} plugin".format(config_obj.documentation_plugin))
            else:
                print("[error] Plugin option not available: {}".format(option))
