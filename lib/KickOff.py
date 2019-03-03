#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os.path
from lib import Settings
from lib import SetupLogger
from shutil import copy
from shutil import rmtree


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
                print("[warning] Config file exist: {}, "
                      "if you want to overwrite the global configuration file please run again "
                      "with the -f option".format(path))
                return False
            # if the path exist and overwrite flag is True
            if exists and overwrite:
                os.remove(self.settings.CONFIGURATION_FILE_PATH)
                copy(self.settings.CONFIGURATION_FILE_EXAMPLE, self.settings.CONFIGURATION_PATH)
                SetupLogger.logger.info("Successfully overwrite the file {} "
                                        .format(path))
                return True
            # if the path not exist
            if not exists:
                # Copy example file
                copy(self.settings.CONFIGURATION_FILE_EXAMPLE, self.settings.CONFIGURATION_PATH)
                SetupLogger.logger.info("Successfully created the directory {} "
                                        .format(path))
                return True
        except OSError as e:
            print("[error] Creation of the file {0} failed - error: {1}".format(path, e))
            exit(1)

    # Create started configuration folders
    def create_configuration_folders(self, overwrite=False):
        error = False
        folders = self.settings.CONFIGURATION_FOLDERS
        for key, val in folders.items():
            try:
                if val.get("folder") is not None:
                    exists = os.path.exists(val.get("folder"))
                else:
                    exists = False
                # if the path exist and overwrite flag is False
                if exists and not overwrite:
                    print("[warning] Folder exists: {}, "
                          "if you want to overwrite the folder please run again with the -f option"
                          .format(val.get("folder")))
                    error = True
                # if the path exist and overwrite flag is True
                if exists and overwrite:
                    # Remove old directory
                    rmtree(val.get("folder"))  # removes all the subdirectories!
                    # Create new dir
                    os.makedirs(val.get("folder"))
                    # Copy example
                    copy(val.get("example"), val.get("folder"))
                    SetupLogger.logger.info("Successfully overwrite the directory {} ".format(val.get("folder")))

                # if the path not exist
                if not exists:
                    if val.get("folder"):
                        # Create folder
                        os.mkdir(val.get("folder"))
                        # Copy example file
                        copy(val.get("example"), val.get("folder"))
                        SetupLogger.logger.info("File successfully copy {0} in {1}"
                                                .format(val.get("example"),
                                                        val.get("folder")))
                    else:
                        # Copy example file
                        copy(val.get("example"), Settings.CONFIGURATION_PATH)
                        SetupLogger.logger.info("File successfully copied {0} in {1}"
                                                .format(val.get("example"),
                                                        Settings.CONFIGURATION_PATH))

            except OSError as e:
                print("[error] Creation of the directory {0} failed - error: {1}"
                                         .format(val.get("folder"), e))
                exit(1)
        if error:
            return False
        else:
            return True

    # Create all started files
    def create_started_files(self, overwrite=False):

        print("[-] Creating template folders.")
        folders_created = self.create_configuration_folders(overwrite)

        print("[-] Creating configuration file.")
        config_file_created = self.create_global_configuration_file(overwrite)

        if folders_created and config_file_created:
            print("[-] Initialization files created successfully!")
        else:
            print("[error] Error creating initialization files")
