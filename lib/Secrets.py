#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
from lib import SetupLogger


# Read password file
def read_password_file(file_path):

    SetupLogger.logger.debug("Reading password file: {}".format(file_path))

    """
    # Validate if the value exist if don't use default
    if not config.get('passwords_file', False):
        passwords_file_path = os.path.join(
            Settings.CONFIGURATION_FOLDERS["passwords"].get('folder'), "passwords.yml")

        SetupLogger.logger.debug("Variable passwords_file not defined, using default value: {}"
                                 .format(passwords_file_path))
    else:
        passwords_file_path = config.get('passwords_file')
        SetupLogger.logger.debug("passwords_file defined, using value: {}".format(passwords_file_path))
    """