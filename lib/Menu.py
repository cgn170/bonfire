#!/usr/bin/env python

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

from lib import KickOff
from lib import Deployment
from lib import SetupLogger
from lib import Settings
import sys
sys.path.append("..")

class Menu:

    def __int__(self, args):
        print("test")

    # Process each available command
    def process_command(self, command, overwrite=False, config_file_path=Settings.CONFIGURATION_FILE_PATH):

        kickoff = KickOff.KickOff()
        deployment = Deployment.Deployment()

        if command == "init":
            SetupLogger.logger.info("Creating configuration files ...")
            kickoff.create_started_files(overwrite)

        elif command == "deploy":
            SetupLogger.logger.info("Deploying, please wait ...")
            deployment.process_deployment(config_file_path)

        elif command == "remove":
            SetupLogger.logger.info("Removing all deployments, please wait ...")

        elif command == "plugins":

            SetupLogger.logger.info("Available Plugins: {}".format(", ".join(deployment.get_list_plugins())))

        else:
            SetupLogger.logger.error("Command '{}' not found, exiting ...".format(command))
            exit(1)