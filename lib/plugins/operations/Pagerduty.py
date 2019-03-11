#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission

This plugin process operation files and deploy them in pagerduty
configuration

"""

# Plugin information, useful to know what it does
plugin_description = "Plugin to deploy operations configuration in pagerduty, check operations.yml " \
                     "and passwords.yml examples file for more information"


# Get plugin description
def get_plugin_description():
    return plugin_description


# Deploy function, deploy all operations template
def deploy(dry_run, plugin_configuration_variables, passwords):
    print("[plugin: Pagerduty] Doing something: {}".format(plugin_configuration_variables))


# Remove function, remove stacks deployed
def remove(dry_run, plugin_configuration_variables, passwords):
    print("[plugin: Pagerduty] Doing something")
