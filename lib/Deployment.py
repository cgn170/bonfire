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


class Deployment:

    def __init__(self):
        pass

    # Get list of plugin
    def get_list_plugins(self):
        filenames = os.listdir(Settings.PLUGINS_PATH)
        plugin_list = []
        for filename in filenames:
            if os.path.isdir(os.path.join(Settings.PLUGINS_PATH, filename)):
                SetupLogger.logger.debug("Plugin found: {}"
                                         .format(os.path.join(Settings.PLUGINS_PATH, filename)))
                plugin_list.append(filename)

        return plugin_list

    # Query plugin path with their name
    def get_plugin_path(self, plugin_name):
        if plugin_name in self.get_list_plugins():
            SetupLogger.logger.debug("Plugin '{0}' was found in {1}".format(plugin_name, Settings.PLUGINS_PATH))
            return os.path.join(Settings.PLUGINS_PATH, plugin_name)
        SetupLogger.logger.debug("Plugin '{0}' was not found {1}".format(plugin_name, Settings.PLUGINS_PATH))
        return None

    # Process plugin alert information
    def process_plugin(self, plugin_name, alert_content):
        # Check if the alert_content is the correct with the plugin
        if type(alert_content) is not dict:
            SetupLogger.logger.error("Variable alert_content is not a dict type, can't process plugin: {}"
                                     .format(plugin_name))
            return None
        # Check if the plugin_name is not a str type
        if type(plugin_name) is not str:
            SetupLogger.logger.error("Variable plugin_name is not a str type, can't process plugin: {}"
                                     .format(plugin_name))
            return None

        # Check if the plugin exist and process it
        if plugin_name in self.get_list_plugins():

            print("Do something with the plugin")










        else:
            SetupLogger.logger.error("Plugin '{}' was not found".format(plugin_name))
            return None

    # Here is the logic to deploy
    def process_deployment(self, config_file_path):

        # Read configuration file
        config = (Utils.read_yml_file(config_file_path)).get('config')

        # Validate if the value exist if don't use default
        if not config.get('alerts_dir', False):
            alerts_dir = Settings.CONFIGURATION_FOLDERS["alerts"].get('folder')
            SetupLogger.logger.debug("alerts_dir not defined, using default value: {}".format(alerts_dir))
        else:
            alerts_dir = config.get('alerts_dir')
            SetupLogger.logger.debug("alerts_dir defined, using value: {}".format(alerts_dir))
        # Validate if the dir is valid
        if not os.path.isdir(alerts_dir):
            SetupLogger.logger.fatal("Alerts directory is not valid")
            exit(1)

        # Validate if the value exist if don't use default
        if not config.get('documentation_dir', False):
            documentation_dir = Settings.CONFIGURATION_FOLDERS["documentation"].get('folder')
            SetupLogger.logger.debug("documentation_dir not defined, using default value: {}".format(documentation_dir))
        else:
            documentation_dir = config.get('documentation_dir')
            SetupLogger.logger.debug("documentation_dir defined, using value: {}".format(documentation_dir))
        # Validate if the dir is valid
        if not os.path.isdir(documentation_dir):
            SetupLogger.logger.fatal("Documentation directory is not valid")
            exit(1)

        # Check this **************
        # Validate if the value exist if don't use default
        if not config.get('passwords_file', False):
            passwords_file = os.path.join(Settings.CONFIGURATION_FOLDERS["passwords"].get('folder'), "passwords.yml")

            SetupLogger.logger.debug("passwords_file not defined, using default value: {}".format(passwords_file))
        else:
            passwords_file = config.get('passwords_file')
            SetupLogger.logger.debug("passwords_file defined, using value: {}".format(passwords_file))
        # Validate if the file is valid
        if not os.path.isfile(passwords_file):
            SetupLogger.logger.fatal("Passwords file is not valid")
            exit(1)

        # Get available plugins
        plugin_list = self.get_list_plugins()

        print("List of plugins: {}".format(plugin_list))
        print("List of alerts file: {}".format(Utils.get_list_yml_file_directory(alerts_dir)))
        print("List of documentation file: {}".format(Utils.get_list_yml_file_directory(documentation_dir)))
        print("Password file: {}".format(passwords_file))


        #Alerts definition path
        alerts_path = ""

        # Process each plugin
        # for plugin in plugin_list:
        #    self.process_plugin()
