#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
import os
import yaml
import random
from lib import SetupLogger


# Read and parse a YML file
def read_yml_file(file_path):
    try:
        parsed_dict = yaml.safe_load(open(file_path).read())
        SetupLogger.logger.debug("YML file '{}' parsed successfully".format(file_path))
        return parsed_dict

    except yaml.YAMLError as e:
        SetupLogger.logger.error("Could not parse file '{0}', error: {1}".format(file_path, e))
    except IOError as e:
        SetupLogger.logger.error("File error {}".format(e))
    # If the parsed was not possible returns None
    return None


# List of yml files in a directory
def list_yml_files_in_directory(directory_path):
    filenames = os.listdir(directory_path)
    file_list = []
    for filename in filenames:
        # Check if the filename ends with yml extension
        if filename.endswith("yml"):
            SetupLogger.logger.debug("YML file found: {}"
                                     .format(os.path.join(directory_path, filename)))
            file_list.append(os.path.join(directory_path, filename))

    return file_list


# Generate word with random values
def generate_random_word(number_letters=3):
    if number_letters > 0:
        base = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
        random_word = ""
        for i in range(0, number_letters, 1):
            random_word += base[random.randint(0, 57)]
        return random_word
    else:
        return None
