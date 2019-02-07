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
import importlib


class Deployment:

    def __init__(self):

        pass

    # Load all plugins in objects
    def load_plugins(self):

        # Load all plugins, i should improve this ....
        importlib.import_module('lib.plugins')
        modules = {}
        plugins = self.get_list_plugins()
        for plugin, path in plugins.items():
            modules[plugin] = importlib.import_module("lib.plugins."+plugin, package="lib.plugins")
            SetupLogger.logger.debug("'{0}' plugin loaded successfully".format(plugin))
        return modules

    # Get list of plugin
    def get_list_plugins(self):

        filenames = os.listdir(Settings.PLUGINS_PATH)
        plugin_list = {}
        for filename in filenames:
            if os.path.isfile(os.path.join(Settings.PLUGINS_PATH, filename)):
                if filename.endswith(".py") and not filename.startswith("__"):
                    plugin_list[filename.replace(".py", "")] = os.path.join(Settings.PLUGINS_PATH, filename)
            # if os.path.isdir(os.path.join(Settings.PLUGINS_PATH, filename)):
                # SetupLogger.logger.debug("Plugin found: {}"
                #                         .format(os.path.join(Settings.PLUGINS_PATH, filename)))
            #    plugin_list[filename] = os.path.join(Settings.PLUGINS_PATH, filename)

        return plugin_list

    # Get plugin information
    def get_list_information_plugins(self):

        plugins_modules = self.load_plugins()
        plugin_list = []
        for plugin, path in self.get_list_plugins().items():
            plugin_list.append(
                {"name": plugin,
                 "path": path,
                 "desc": plugins_modules[plugin].get_plugin_description()})
        return plugin_list

    # Query plugin path with their name
    def get_plugin_path(self, plugin_name):
        if plugin_name in self.get_list_plugins():
            SetupLogger.logger.debug("Plugin '{0}' was found in {1}".format(plugin_name, Settings.PLUGINS_PATH))
            return os.path.join(Settings.PLUGINS_PATH, plugin_name)
        SetupLogger.logger.debug("Plugin '{0}' was not found in {1}".format(plugin_name, Settings.PLUGINS_PATH))
        return None

    ##################################
    # Import and process plugin for all alert files
    ##################################
    def process_alert_plugin(self, plugin_name, list_alerts_file, plugin_modules, password_file_path, dry_run):

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

        #####################################
        # We call external plugin

        plugin_modules[plugin_name].deploy(list_alerts_file, password_file_path, dry_run)

        ##########################################
        # Check if the plugin exist and process it
        ##########################################

        SetupLogger.logger.debug("Finished plugin execution")

    # Here is the logic to deploy a deployment
    def process_alerts_deployment(self, config_file_path, dry_run):

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

        # Check alerts file
        alerts_list_file = Utils.list_files_in_directory(alerts_dir)

        if len(alerts_list_file) > 0:
            print("Number of alerts file found : {}".format(len(alerts_list_file)))
        else:
            print("No alerts file found, exiting ...")
            exit(1)

        # Check documentation
        documentation_list_file = Utils.list_files_in_directory(documentation_dir, "")

        if len(documentation_list_file):
            print("Number of documentation file found: {}".format(len(documentation_list_file)))
        else:
            print("No documentation file found, is recommended to use some documentation for each alert "
                  "(Optional) ...")

        ######################
        # Process deployment process for each plugin
        ######################

        # Create hidden folder for plugin deployment configuration

        Utils.create_folder(overwrite=False, folder_path=Settings.CONFIGURATION_HIDDEN_FOLDER_DEPLOYMENT)

        # Get information about what plugins are available in the folder
        plugins_available = self.get_list_plugins()

        SetupLogger.logger.debug("Loading plugins ...")
        plugins_modules = self.load_plugins()

        for plugin in plugins_available:
            self.process_alert_plugin(plugin, alerts_list_file, plugins_modules, passwords_file, dry_run)

    # Here is the logic to delete a deployment
    def remove_alerts_deployment(self, config_file_path, dry_run):

        # Read configuration file
        config_file = Utils.read_yml_file(config_file_path)

        # Check if the configuration folder exists
        config_deployment_path = Settings.CONFIGURATION_HIDDEN_FOLDER_DEPLOYMENT

        # Check if the configuration file exist
        if config_file is None:
            SetupLogger.logger.error("Configuration file not found: {}, exiting ...".format(config_file_path))
            exit(1)

        config = config_file.get('config')

        # Validate if the dir is valid
        if not os.path.isdir(config_deployment_path):
            SetupLogger.logger.fatal("Configuration deployment directory is not valid, exiting ...")
            exit(1)

        # Check this **************
        # Validate if the value exist if don't use default
        if not config.get('passwords_file', False):
            passwords_file = os.path.join(Settings.CONFIGURATION_FOLDERS["passwords"].get('folder'),
                                          "passwords.yml")

            SetupLogger.logger.debug(
                "Variable passwords_file not defined, using default value: {}".format(passwords_file))
        else:
            passwords_file = config.get('passwords_file')
            SetupLogger.logger.debug("passwords_file defined, using value: {}".format(passwords_file))
        # Validate if the file is valid
        if not os.path.isfile(passwords_file):
            SetupLogger.logger.fatal("Passwords file is not valid, exiting ...")
            exit(1)

        ######################
        # Process each deletion process for each plugin
        ######################

        # Get information about what plugins are available in the folder
        plugins_available = self.get_list_plugins()

        SetupLogger.logger.debug("Loading plugins ...")
        plugins_modules = self.load_plugins()

        for plugin in plugins_available:

            # Call remove function inside the plugin
            SetupLogger.logger.debug("Processing plugin: {}".format(plugin))
            plugins_modules[plugin].remove(passwords_file, dry_run)
            SetupLogger.logger.debug("Finished plugin execution")