#!/usr/bin/env python

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

try:
    import sys

    import warnings

    warnings.filterwarnings(action="ignore", message=".* it was already imported", category=UserWarning)
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)

except KeyboardInterrupt:
    errMsg = "user aborted"


# Everything starts here
def main():
    print("Hey!")


# Init main
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
else:
    exit(0)
