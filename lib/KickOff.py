#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

from lib import Settings
import os.path

from shutil import copy
from shutil import rmtree
from lib import SetupLogger


class KickOff:

    def __init__(self):
        self.settings = Settings

    # Create started configuration file
    def create_global_configuration_file(self, overwrite=False):
        try:
            path = self.settings.CONFIGURATION_FILE_PATH
            exists = os.path.exists(path)
            # if the path exist and overwrite flag is False
            if exists and not overwrite:
                SetupLogger.logger.warn("Init file exist: {},"
                                        "If you want to overwrite the global configuration file please run again "
                                        "with the -f option".format(path))
            # if the path exist and overwrite flag is True
            if exists and overwrite:
                os.remove(self.settings.CONFIGURATION_FILE_PATH)
                copy(self.settings.CONFIGURATION_FILE_EXAMPLE, self.settings.CONFIGURATION_PATH)
                SetupLogger.logger.info("Successfully overwrite the file {} "
                                        .format(path))
            # if the path not exist
            if not exists:
                # Copy example file
                copy(self.settings.CONFIGURATION_FILE_EXAMPLE, self.settings.CONFIGURATION_PATH)
                SetupLogger.logger.info("Successfully created the directory {} "
                                        .format(path))
        except OSError as e:
            SetupLogger.logger.fatal("Creation of the file {0} failed - error: {1}".format(path, e))
            exit(1)

    # Create started configuration folders
    def create_configuration_folders(self, overwrite=False):
        folders = self.settings.CONFIGURATION_FOLDERS
        for folder in folders:
            try:
                exists = os.path.exists(folder.get("folder"))
                # if the path exist and overwrite flag is False
                if exists and not overwrite:
                    SetupLogger.logger.warn("Folder exists: {}, "
                                            "if you want to overwrite the folder please run again with the -f option"
                                            .format(folder.get("folder")))
                # if the path exist and overwrite flag is True
                if exists and overwrite:
                    rmtree(folder.get("folder"))  # removes all the subdirectories!
                    os.makedirs(folder.get("folder"))
                    SetupLogger.logger.info("Successfully overwrite the directory {} ".format(folder.get("folder")))
                # if the path not exist
                if not exists:
                    # Create folder
                    os.mkdir(folder.get("folder"))
                    # Copy example file
                    copy(folder.get("example"), folder.get("folder"))
                    SetupLogger.logger.info("Successfully created the directory {} ".format(folder.get("folder")))
            except OSError as e:
                SetupLogger.logger.fatal("Creation of the directory {0} failed - error: {1}"
                                         .format(folder.get("folder"), e))
                exit(1)

    # Create all started files
    def create_started_files(self, overwrite=False):

        self.create_configuration_folders(overwrite)

        self.create_global_configuration_file(overwrite)
