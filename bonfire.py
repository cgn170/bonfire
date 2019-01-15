#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    bonfire.py [Options] <Command>
    bonfire.py -h | --help | --version
Options:
  -h --help  - Shows this message
  -v         - Verbose mode
  -f         - Force command actions
  --config   - Configuration file path
  --version  - Version
Command:
  init       - Create configuration files and directories
  deploy     - Deploy IT Operations stack
  remove     - Remove all configurations and stack created
  plugins    - Show a list of available plugins
"""
try:
    import os
    import sys
    import warnings
    from docopt import docopt
    from lib import KickOff
    from lib import Settings

    warnings.filterwarnings(action="ignore", message=".* it was already imported", category=UserWarning)
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)

except KeyboardInterrupt:
    errMsg = "user aborted"
except ImportError as e:
    raise Exception("Error importing library: {}".format(e))


# Everything starts here
def main(args):

    path = os.getcwd()
    # Check command value
    command = args['<Command>']
    kickoff = KickOff.KickOff()
    if command == "init":
        print("init")
        kickoff.create_started_files()

    elif command == "deploy":
        print("deploy")
    elif command == "remove":
        print("remove")
    else:
        print("command not found")


# Init main
if __name__ == "__main__":
    try:
        args = docopt(__doc__, version=0.1)
        main(args)
    except KeyboardInterrupt:
        exit(0)
else:
    exit(0)
