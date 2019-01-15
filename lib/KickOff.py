#!/usr/bin/env python

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
import Settings
import yaml
import os.path
from shutil import copy


class KickOff:

    def __init__(self):
        self.settings = Settings

    # Create started configuration file
    def create_global_configuration_file(self, overwrite=False):
        try:
            path = self.settings.CONFIGURATION_FILE_PATH
            exists = os.path.exists(path)
            if not exists:
                with open(path, 'w') as output:
                    yaml.dump(self.settings.GLOBAL_SETTINGS,
                              output, default_flow_style=False)
            if exists:
                print("[Error] init file exist: {}"
                      "\nIf you want to overwrite the global configuration file please run again with the -f option"
                      .format(path))
            if overwrite:
                # Must overwrite the file
                print("Overwriten")

        except yaml.YAMLError as e:
            raise Exception("YAML error: {}".format(e))
        except Exception as e:
            raise Exception("Fatal error: {}".format(e))

    # Create started configuration folders
    def create_configuration_folders(self, overwrite=False):
        folders = self.settings.CONFIGURATION_FOLDERS
        for folder in folders:
            try:
                exists = os.path.exists(folder.get("folder"))
                if exists:
                    print("[Error] folder exists: {}"
                          "\nIf you want to overwrite the folder please run again with the -f option"
                          .format(folder.get("folder")))
                if not exists or overwrite:
                    # Create folder
                    os.mkdir(folder.get("folder"))
                    # Copy example file
                    copy(folder.get("example"), folder.get("folder"))
            except OSError as e:
                raise Exception("Creation of the directory {0} failed - error: {1}".format(folder.get("folder"), e))
            else:
                print ("Successfully created the directory {} ".format(folder.get("folder")))

    # Create all started files
    def create_started_files(self):
        self.create_configuration_folders(overwrite=True)

        self.create_global_configuration_file(overwrite=True)
