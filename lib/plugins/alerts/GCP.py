#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission

This plugin process GCP alerts configuration files, build a custom terraform template with stackdriver API
configuration

"""

from lib import SetupLogger
from lib import Settings
from lib import Utils
from jinja2 import Environment, FileSystemLoader
import os

# Check if hidden folder exist and create GCP folder inside
_path_deployment_plugin = os.path.join(Settings.CONFIGURATION_HIDDEN_FOLDER_DEPLOYMENT, "GCP")

# Plugin information, useful to know what it does
plugin_description = "Plugin to process GCP stackdriver alerts, check alerts_example2.yml " \
                     "and passwords.yml example files for more information"


# Get plugin description
def get_plugin_description():
    return plugin_description


# Create terraform template for each alert definition file
def create_terraform_template_alerts(alert_yml_data=None, gcp_keys=None, dry_run=True):
    print("[plugin: GCP] Creating cloudformation alerts template")

    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, '')
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('GCP_template.tf')

    # Query all categories inside the yml alert file
    for category in alert_yml_data:
        # Must use
        _category = str(category)

        # Get Monitoring System
        for monitoring_system in alert_yml_data.get(_category):
            # print 'Monitoring System:',  monitoring_system
            _monitoring_system = str(monitoring_system)

            # Check if the monitor tool is AWS
            if _monitoring_system == "GCP":
                _account = str(alert_yml_data[_category][_monitoring_system]['Account'])

                stack_name = "{0}-{1}-alerts-stack".format(_account, category)
                stack_file_path = os.path.join(_path_deployment_plugin, stack_name + ".tf")
                with open(stack_file_path, 'w') as fh:
                    fh.write(template.render(
                        project="HEEEEEEEEEEY",
                    ))
                print("[plugin: GCP] '{0}' stack created in directory '{1}'".format(stack_name, stack_file_path))

# Deploy function, create and deploy cloudformation template with alerts configuration
def deploy(list_alerts_file, passwords, dry_run):

    # Create deployment folder
    Utils.create_folder(overwrite=True, folder_path=_path_deployment_plugin)

    # Create template and wait until is finish
    for alert_file in list_alerts_file:
        alert_file_parsed = Utils.read_yml_file(alert_file)
        create_terraform_template_alerts(alert_yml_data=alert_file_parsed,
                                         gcp_keys=None,
                                         dry_run=dry_run)


# Remove function, remove stacks deployed
def remove(dry_run, passwords):
    pass
