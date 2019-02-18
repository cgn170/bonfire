#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os
import yaml
import xlsxwriter
import operator
from lib import Utils
from lib import Settings
from lib import SetupLogger


# Alert object
class AlertDefinition:
    def __init__(self, name, category, subcategory, metric, severity, wi):

        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.metric = metric
        self.severity = severity
        self.wi = wi


# Documentation class, contains methods to built alert matrix
class Documentation:

    def __init__(self):

        pass

    # Here is the logic to deploy all documentation
    def process_documentation_deployment(self, config_file_path, dry_run):

        # Read configuration file
        config_file = Utils.read_yml_file(config_file_path)

        # Check if the configuration file exist
        if config_file is None:
            print("[error] Configuration file not found: {}, exiting ...".format(config_file_path))
            exit(1)

        config = config_file.get('config')

        # Validate if the value exist if don't use default
        if not config.get('documentation_dir', False):
            documentation_dir = Settings.CONFIGURATION_FOLDERS["documentation"].get('folder')
            SetupLogger.logger.debug("Variable documentation_dir not defined, using default value: {}".format(documentation_dir))
        else:
            documentation_dir = config.get('documentation_dir')
            SetupLogger.logger.debug("documentation_dir defined, using value: {}".format(documentation_dir))
        # Validate if the dir is valid
        if not os.path.isdir(documentation_dir):
            print("[error] Documentation directory is not valid, exiting ...")
            exit(1)

        # Check documentation
        documentation_list_file = Utils.list_files_in_directory(documentation_dir, "")

        if len(documentation_list_file):
            print("[-] Documentation files found: {}".format(len(documentation_list_file)))
        else:
            print("[warning] No documentation file found, is recommended to use some documentation for each alert "
                  "(Optional) ...")

