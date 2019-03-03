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


# Deploy function, deploy all documentation template
def deploy(dry_run):
    print("Doing something")


# Remove function, remove stacks deployed
def remove(passwords, dry_run):
    print("Doing something")
