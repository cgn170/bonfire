#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
import os
import Settings
from SetupLogger import logger


class Deployment:

    def __init__(self):
        pass

    # Get list of plugin
    def get_list_plugins(self):
        filenames = os.listdir(Settings.PLUGINS_PATH)
        plugin_list = []
        for filename in filenames:
            if os.path.isdir(os.path.join(Settings.PLUGINS_PATH, filename)):
                plugin_list.append(filename)

        return plugin_list

    # Query plugin path with their name
    def get_plugin_path(self, plugin_name):
        if plugin_name in self.get_list_plugins():
            logger.debug("Plugin")
            return os.path.join(Settings.PLUGINS_PATH, plugin_name)
        return None

    # Process plugin alert information
    def process_plugin(self, plugin_name, alert_content):
        # Check if the alert_content is the correct with the plugin
        if type(alert_content) is not dict:
            logger.error("Variable alert_content is not a dict type, can't process plugin: {}".format(plugin_name))
            return None
        if type(plugin_name) is not str:
            logger.error("Variable plugin_name is not a str type, can't process plugin: {}".format(plugin_name))
            return None

        # Check if the plugin exist

        if plugin_name in self.get_list_plugins():
            print("Do something with the plugin")

        else:
            logger.error("Plugin '{}' not found".format(plugin_name))
            return None
