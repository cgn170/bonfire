#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
import os
import yaml
from lib import SetupLogger


# Read and parse a YML file
def read_yml_file(file_path):
    try:
        parsed_dict = yaml.safe_load(open(file_path).read())
        SetupLogger.logger.debug("YML file '{}' parsed successfully".format(file_path))
        return parsed_dict

    except yaml.YAMLError as e:
        SetupLogger.logger.error("Could parse file '{0}', error: {1}".format(file_path, e))
    # If the parsed was not possible returns None
    return None


# List of yml files in a directory
def get_list_yml_file_directory(directory_path):
    filenames = os.listdir(directory_path)
    file_list = []
    for filename in filenames:
        # Check if the filename ends with yml extension
        if filename.endswith("yml"):
            SetupLogger.logger.debug("YML file found: {}"
                                     .format(os.path.join(directory_path, filename)))
            file_list.append(filename)

    return file_list
