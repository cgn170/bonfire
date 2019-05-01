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
from lib import ConfigFile


# Documentation class, contains methods to deploy
class Operations:

    def __init__(self):
        pass

    # Here is the logic to deploy all documentation
    def process_operations_deployment(self, config_file_path, dry_run, option):

        # Read configuration file
        config_obj = ConfigFile.ConfigFIle(config_file_path)

        # Load path list file documentation from documentation folder
        documentation_list_file = Utils.list_files_in_directory(config_obj.operations_dir, "")

        if len(documentation_list_file):
            print("[-] Documentation files found: {}".format(len(documentation_list_file)))
        else:
            print("[warning] No documentation file found, is recommended to use some documentation for each alert "
                  "(Optional) ...")

        # Deploy operations file to plugin service
        if not dry_run and config_obj.upload_operations:

            plugin_folder_path = Settings.OPERATION_PLUGINS_PATH
            plugin_package = "lib.plugins.operations"

            # Get information about what plugins are available in the folder
            # plugins_available = Utils.get_list_plugins(plugin_folder_path)
            # print("[*] Plugins loaded: {}".format(",".join(plugins_available.keys())))

            plugins_modules = Utils.load_plugins(plugin_package, plugin_folder_path)

            # Plugin configuration variables
            plugin_configuration_variables = config_obj.config_yml.get(config_obj.operations_plugin.lower(), None)

            if option == "deploy":
                print("[plugin] Processing {} plugin".format(config_obj.operations_plugin))
                plugins_modules[config_obj.operations_plugin].deploy(dry_run,
                                                                     plugin_configuration_variables,
                                                                     "passwords")
                print("[plugin] Finished {} plugin".format(config_obj.operations_plugin))

            elif option == "remove":

                # Call remove function inside the plugin
                print("[plugin] Processing {} plugin".format(config_obj.operations_plugin))
                plugins_modules[config_obj.operations_plugin].remove(dry_run,
                                                                     plugin_configuration_variables,
                                                                     "passwords")
                print("[plugin] Finished {} plugin".format(config_obj.operations_plugin))
            else:
                print("[error] Plugin option not available: {}".format(option))
