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
CONFIGURATION_FOLDERS = {

    "alerts": {
        "folder": os.path.join(CONFIGURATION_PATH, "alerts"),
        "example": os.path.join(EXAMPLES_PATH, "alerts.yml")
    },
    "documentation": {
        "folder": os.path.join(CONFIGURATION_PATH, "documentation"),
        "example": os.path.join(EXAMPLES_PATH, "WI_unhealthyhostcount_AWS.wiki")
    },
    "passwords": {
        # Is a good practice to not save this directory in any version system, example git
        "folder": os.path.join(CONFIGURATION_PATH, "passwords"),
        "example": os.path.join(EXAMPLES_PATH, "passwords.yml")
    }
}

CONFIGURATION_FILE_EXAMPLE = os.path.join(EXAMPLES_PATH, "bonfire.yml")
CONFIGURATION_FILE_NAME = "bonfire.yml"
CONFIGURATION_FILE_PATH = os.path.join(CONFIGURATION_PATH, CONFIGURATION_FILE_NAME)

PLUGINS_PATH = os.path.join(PROJECT_PATH, "plugins")
