#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
import os
import yaml
import random
from shutil import rmtree
from lib import SetupLogger
import importlib


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
def list_files_in_directory(directory_path, extension="yml"):
    filenames = os.listdir(directory_path)
    file_list = []
    for filename in filenames:
        # Check if the filename ends with yml extension
        if filename.endswith(extension):
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


# Create a folder with a path
def create_folder(overwrite=False, folder_path=None):
    # check if any previous folder exists
    try:
        exists = os.path.exists(folder_path)
        if exists and not overwrite:
            SetupLogger.logger.warn("Directory exist: {}, "
                                    "will not be overwrite unless parameter overwrite is true"
                                    .format(folder_path))
        if exists and overwrite:
            # Remove old directory
            rmtree(folder_path)  # removes all the subdirectories!
            # Create new dir
            os.makedirs(folder_path)
            SetupLogger.logger.debug("Successfully overwrite the directory {} ".format(folder_path))
        # if the path does not exist
        if not exists:
            # Create folder
            os.mkdir(folder_path)
            SetupLogger.logger.debug("Successfully created the directory {} ".format(folder_path))

    except OSError as e:
        SetupLogger.logger.fatal("Creation of the directory {0} failed - error: {1}"
                                 .format(folder_path, e))
        exit(1)


# Get list of plugin
def get_list_plugins(plugin_path_folder):

    filenames = os.listdir(plugin_path_folder)
    plugin_list = {}
    for filename in filenames:
        if os.path.isfile(os.path.join(plugin_path_folder, filename)):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_list[filename.replace(".py", "")] = os.path.join(plugin_path_folder, filename)

    return plugin_list


# Get plugin information
def get_list_information_plugins(plugin_package, plugin_path_folder):

    plugins_modules = load_plugins(plugin_package, plugin_path_folder)
    plugin_list = []
    for plugin, path in get_list_plugins(plugin_path_folder).items():
        plugin_list.append(
            {"name": plugin,
             "path": path,
             "desc": plugins_modules[plugin].get_plugin_description()})
    return plugin_list


# Query plugin path with their name
def get_plugin_path(self, plugin_name, plugin_path_folder):
    if plugin_name in self.get_list_plugins():
        SetupLogger.logger.debug("Plugin '{0}' was found in {1}".format(plugin_name, plugin_path_folder))
        return os.path.join(plugin_path_folder, plugin_name)
    SetupLogger.logger.debug("Plugin '{0}' was not found in {1}".format(plugin_name, plugin_path_folder))
    return None


# Load all plugins in objects
def load_plugins(plugin_package, plugin_path_folder):

    # Load all plugins, i should improve this ....
    importlib.import_module(plugin_package)
    modules = {}
    plugins = get_list_plugins(plugin_path_folder)
    for plugin, path in plugins.items():
        modules[plugin] = importlib.import_module(plugin_package+"."+plugin, package=plugin_package)
        SetupLogger.logger.debug("'{0}' plugin loaded successfully".format(plugin))
    return modules

