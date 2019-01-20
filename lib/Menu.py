#!/usr/bin/env python

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

from lib import KickOff
from lib import Deployment
from lib import SetupLogger


class Menu:

    def __int__(self, args):
        print("test")

    # Process each available command
    def process_command(self, command, overwrite=False):

        kickoff = KickOff.KickOff()
        deployment = Deployment.Deployment()

        if command == "init":
            SetupLogger.logger.info("Creating configuration for the first time")
            kickoff.create_started_files(overwrite)

        elif command == "deploy":
            SetupLogger.logger.info("Deploying, please wait ...")

        elif command == "remove":
            SetupLogger.logger.info("Removing all deployments, please wait ...")

        elif command == "plugins":

            SetupLogger.logger.info("Available Plugins: {}".format(", ".join(deployment.get_list_plugins())))
        else:
            SetupLogger.logger.error("Command '{}' not found".format(command))
