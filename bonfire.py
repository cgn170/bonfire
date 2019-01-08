#!/usr/bin/env python
"""
Usage: bonfire.py [OPTIONS] COMMAND
Arguments:
  OPTIONS   - Options to run the framework
  COMMAND   - Command to execute
Options:
  -h --help  - Shows this message
  -v         - Verbose mode
  --config   - Configuration file path
Commands:
  init       - Create configuration files and directories
  deploy     - Deploy IT Operations stack
  destroy    - Remove all configurations and stack created
"""

try:
    import sys
    import warnings
    from docopt import docopt

    warnings.filterwarnings(action="ignore", message=".* it was already imported", category=UserWarning)
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)

except KeyboardInterrupt:
    errMsg = "user aborted"


# Everything starts here
def main(arg):
    print(arg)


# Init main
if __name__ == "__main__":
    try:
        arguments = docopt(__doc__)
        main(arguments)
    except KeyboardInterrupt:
        exit(0)
else:
    exit(0)
