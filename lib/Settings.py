#!/usr/bin/env python

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os
import sys

GIT_REPOSITORY = "https://github.com/cgn170/bonfire.git"
GIT_PAGE = "https://github.com/cgn170/bonfire"

CONFIGURATION_PATH = os.getcwd()
PROJECT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
EXAMPLES_PATH = os.path.join(PROJECT_PATH, "examples")
CONFIGURATION_FOLDERS = [
    {
        "folder": os.path.join(CONFIGURATION_PATH, "Alerts"),
        "example": os.path.join(EXAMPLES_PATH, "alerts.yml")
    },
    {
        "folder": os.path.join(CONFIGURATION_PATH, "Documentation"),
        "example": os.path.join(EXAMPLES_PATH, "WI_unhealthyhostcount_AWS.wiki")
    },
    {
        "folder": os.path.join(CONFIGURATION_PATH, "Credentials"),
        "example": os.path.join(EXAMPLES_PATH, "credentials.yml")
    }
]

CONFIGURATION_FILE_EXAMPLE = os.path.join(EXAMPLES_PATH, "bonfire.yml")
CONFIGURATION_FILE_NAME = "bonfire.yml"
CONFIGURATION_FILE_PATH = os.path.join(CONFIGURATION_PATH, CONFIGURATION_FILE_NAME)

PLUGINS_PATH = os.path.join(PROJECT_PATH, "plugins")
