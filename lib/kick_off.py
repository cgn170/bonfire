#!/usr/bin/env python

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""
import settings
import yaml
import os.path


def create_global_configuration_file(path=settings.CONFIGURATION_FILE_PATH, overwrite=False):
    try:
        exists = os.path.exists(path)
        if not exists:
            with open(path, 'w') as output:
                yaml.dump(settings.GLOBAL_SETTINGS,
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


def create_configuration_folders(overwrite=False):
    folders = settings.CONFIGURATION_FOLDERS
    for folder in folders:
        try:
            exists = os.path.exists(folder)
            if exists:
                print("[Error] folder exists: {}"
                      "\nIf you want to overwrite the folder please run again with the -f option"
                      .format(folder))
            if not exists or overwrite:
                os.mkdir(folder)
        except OSError:
            raise Exception("Creation of the directory {} failed".format(folder))
        else:
            print ("Successfully created the directory {} ".format(folder))
