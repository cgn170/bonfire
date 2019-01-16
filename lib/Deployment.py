#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
import os
import Settings


class Deployment:

    def __init__(self):
        pass

    def get_list_plugins(self):
        filenames = os.listdir(Settings.PLUGINS_PATH)
        plugin_list = []
        for filename in filenames:
            if os.path.isdir(os.path.join(Settings.PLUGINS_PATH, filename)):
                plugin_list.append(filename)

        return plugin_list

