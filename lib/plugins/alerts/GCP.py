#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission

This plugin process GCP alerts configuration files, build a custom terraform template with stackdriver API
configuration

"""

import os
from lib import SetupLogger
from lib import Settings
from lib import Utils
import yaml
import json

# Check if hidden folder exist and create GCP folder inside
_path_deployment_plugin = os.path.join(Settings.CONFIGURATION_HIDDEN_FOLDER_DEPLOYMENT, "GCP")

# Plugin information, useful to know what it does
plugin_description = "Plugin to process GCP stackdriver alerts, check alerts.yml " \
                     "and passwords.yml example files for more information"


# Get plugin description
def get_plugin_description():
    return plugin_description


# Deploy function, create and deploy cloudformation template with alerts configuration
def deploy(dry_run, list_alerts_file, passwords):
    pass


# Remove function, remove stacks deployed
def remove(dry_run, passwords):
    pass
