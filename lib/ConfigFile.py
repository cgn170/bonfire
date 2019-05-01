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


# ConfigurationFile class, contains parsed information of the configuration file
class ConfigFIle:

    def __init__(self, config_file_path):

        self.config_file_path = config_file_path
        self.alerts_dir = None
        self.documentation_dir = None
        self.upload_documentation = None
        self.documentation_plugin = None
        self.operations_dir = None
        self.upload_operations = None
        self.operations_plugin = None
        self.config_yml = None

        self.read_config_file()

    # Get alert dir variable from configuration file
    def read_config_file(self):

        # Read configuration file
        config_file = Utils.read_yml_file(self.config_file_path)

        # Check if the configuration file exist
        if config_file is None:
            print("[error] Configuration file not found: {}, exiting ...".format(self.config_file_path))
            exit(1)

        self.config_yml = config_file.get('config')

        # Validate if the value exist if don't use default
        if not self.config_yml.get('alerts_dir', False):
            self.alerts_dir = Settings.CONFIGURATION_FOLDERS["alerts"].get('folder')
            SetupLogger.logger.debug("Variable alerts_dir not defined, using default value: {}".format(self.alerts_dir))
        else:
            self.alerts_dir = self.config_yml.get('alerts_dir')
            SetupLogger.logger.debug("Variable alerts_dir defined, using value: {}".format(self.alerts_dir))
        # Validate if the dir is valid
        if not os.path.isdir(self.alerts_dir):
            SetupLogger.logger.fatal("Alerts directory is not valid, exiting ...")
            exit(1)

        # Validate if the value exist if don't use default
        if not self.config_yml.get('documentation_dir', False):
            self.documentation_dir = Settings.CONFIGURATION_FOLDERS["documentation"].get('folder')
            SetupLogger.logger.debug(
                "Variable documentation_dir not defined, using default value: {}".format(self.documentation_dir))
        else:
            self.documentation_dir = self.config_yml.get('documentation_dir')
            SetupLogger.logger.debug("documentation_dir defined, using value: {}".format(self.documentation_dir))
        # Validate if the dir is valid
        if not os.path.isdir(self.documentation_dir):
            print("[error] Documentation directory is not valid, exiting ...")
            exit(1)

        # Validate if the value exist if don't use default
        if not self.config_yml.get('operations_dir', False):
            self.operations_dir = Settings.CONFIGURATION_FOLDERS["operations"].get('folder')
            SetupLogger.logger.debug(
                "Variable operations_dir not defined, using default value: {}".format(self.operations_dir))
        else:
            self.operations_dir = self.config_yml.get('operations_dir')
            SetupLogger.logger.debug("operations_dir defined, using value: {}".format(self.operations_dir))
        # Validate if the dir is valid
        if not os.path.isdir(self.operations_dir):
            print("[error] Operations directory is not valid, exiting ...")
            exit(1)

        # Check if upload_documentation variable is available
        self.upload_documentation = self.config_yml.get('upload_documentation', False)

        # Check if documentation_plugin variable is available
        self.documentation_plugin = self.config_yml.get('documentation_plugin', Settings.DEFAULT_DOCUMENTATION_PLUGIN)

        # Check if upload_operations variable is available
        self.upload_operations = self.config_yml.get('upload_operations', False)

        # Check if operations_plugin variable is available
        self.operations_plugin = self.config_yml.get('operations_plugin', Settings.DEFAULT_OPERATIONS_PLUGIN)