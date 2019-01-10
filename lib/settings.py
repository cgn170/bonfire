#!/usr/bin/env python

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os

GIT_REPOSITORY = "https://github.com/cgn170/bonfire.git"
GIT_PAGE = "https://github.com/cgn170/bonfire"

CONFIGURATION_PATH = os.getcwd()
CONFIGURATION_FOLDERS = [
    os.path.join(CONFIGURATION_PATH, "Alerts"),
    os.path.join(CONFIGURATION_PATH, "Documentation"),
    os.path.join(CONFIGURATION_PATH, "Credentials")
]

CONFIGURATION_FILE_NAME = "bonfire.yml"
CONFIGURATION_FILE_PATH = os.path.join(CONFIGURATION_PATH, CONFIGURATION_FILE_NAME)

GLOBAL_SETTINGS = {

}

