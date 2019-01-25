#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os
import importlib
from lib import Settings
from lib import SetupLogger
from lib import Utils


class Deployment:

    def __init__(self):
        pass

    # Get list of plugin
    def get_list_plugins(self):
        filenames = os.listdir(Settings.PLUGINS_PATH)
        plugin_list = {}
        for filename in filenames:
            if os.path.isdir(os.path.join(Settings.PLUGINS_PATH, filename)):
                SetupLogger.logger.debug("Plugin found: {}"
                                         .format(os.path.join(Settings.PLUGINS_PATH, filename)))
                plugin_list[filename] = os.path.join(Settings.PLUGINS_PATH, filename)

        return plugin_list

    # Query plugin path with their name
    def get_plugin_path(self, plugin_name):
        if plugin_name in self.get_list_plugins():
            SetupLogger.logger.debug("Plugin '{0}' was found in {1}".format(plugin_name, Settings.PLUGINS_PATH))
            return os.path.join(Settings.PLUGINS_PATH, plugin_name)
        SetupLogger.logger.debug("Plugin '{0}' was not found {1}".format(plugin_name, Settings.PLUGINS_PATH))
        return None

    ##################################
    # Import and process plugin for all alert files
    ##################################
    def process_plugin(self, plugin_name, list_alerts_file, password_file):

        SetupLogger.logger.debug("Processing plugin: {}".format(plugin_name))

        # Check if the alert_content is the correct with the plugin
        if type(list_alerts_file) is not list:
            SetupLogger.logger.error("Variable alert_content is not a dict type, can't process plugin: {}"
                                     .format(plugin_name))
            return None
        # Check if the plugin_name is not a str type
        if type(plugin_name) is not str:
            SetupLogger.logger.error("Variable plugin_name is not a str type, can't process plugin: {}"
                                     .format(plugin_name))
            return None

        # Get information about what plugins are available in the folder
        plugins_available = self.get_list_plugins()

        ##########################################
        # Check if the plugin exist and process it
        ##########################################

        if plugin_name.lower() in [plugin.lower() for plugin, path in plugins_available.items()]:

            print("Do something with the plugin")

            # plugin_module.Main("aaaa","bbb")



            from plugins import AWS





        else:
            SetupLogger.logger.error("Plugin '{}' was not found".format(plugin_name))
            return None

    # Here is the logic to deploy
    def process_deployment(self, config_file_path):

        # Read configuration file
        config_file = Utils.read_yml_file(config_file_path)

        # Check if the configuration file exist
        if config_file is None:
            SetupLogger.logger.error("Configuration file not found: {}, exiting ...".format(config_file_path))
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
            SetupLogger.logger.debug("Variable documentation_dir not defined, using default value: {}".format(documentation_dir))
        else:
            documentation_dir = config.get('documentation_dir')
            SetupLogger.logger.debug("documentation_dir defined, using value: {}".format(documentation_dir))
        # Validate if the dir is valid
        if not os.path.isdir(documentation_dir):
            SetupLogger.logger.fatal("Documentation directory is not valid, exiting ...")
            exit(1)

        # Check this **************
        # Validate if the value exist if don't use default
        if not config.get('passwords_file', False):
            passwords_file = os.path.join(Settings.CONFIGURATION_FOLDERS["passwords"].get('folder'), "passwords.yml")

            SetupLogger.logger.debug("Variable passwords_file not defined, using default value: {}".format(passwords_file))
        else:
            passwords_file = config.get('passwords_file')
            SetupLogger.logger.debug("passwords_file defined, using value: {}".format(passwords_file))
        # Validate if the file is valid
        if not os.path.isfile(passwords_file):
            SetupLogger.logger.fatal("Passwords file is not valid, exiting ...")
            exit(1)

        # Get available plugins
        # plugin_list = self.get_list_plugins()

        # if len(plugin_list) > 0:
        #    print("List of plugins: {}".format(plugin_list))

        # Check alerts file
        alerts_list_file = Utils.list_yml_files_in_directory(alerts_dir)

        if len(alerts_list_file) > 0:
            print("List of alerts file: {}".format(alerts_list_file))

        documentation_list_file = Utils.list_yml_files_in_directory(documentation_dir)

        if len(documentation_list_file):
            print("List of documentation file: {}".format(documentation_list_file))
        print("Password file: {}".format(passwords_file))

        ######################
        # Process each plugin
        ######################
        for plugin in ['AWS']: # Only process AWS
            self.process_plugin(plugin, alerts_list_file, passwords_file)
