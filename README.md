# Bonfire

bonfire is an open source Monitoring and IT Operations as code framework that automates the process of deployment of custom alarms and documentation in cloud providers also this could be used as part in an Infrastructure as Code pipeline and solve the problem of the IT Operation configuration.

Installation
----

You can download bonfire by cloning the [Git](https://github.com/cgn170/bonfire) repository:

    git clone --depth 1 https://github.com/cgn170/bonfire.git bonfire-dev

and install the dependencies of the requirements.txt file:

    cd bonfire-dev
    pip install -r requirements.txt

bonfire works with [Python](http://www.python.org/download/) version **2.7.x** on any platform.


Usage
----

To get a list of basic options and switches use:

.. code:: python
    python bonfire.py -h
    Usage:
        bonfire.py [-v | -vv | -vvv] [-f] [--dry-run] [--config path] [--doc] [--mf format] <Command>
        bonfire.py -h | --help | --version
    Options:
      -h --help              - Show this message
      -f                     - Force command actions
      -v                     - Verbose mode (vvv for more detail level)
      --dry-run              - Create configuration files only, does not upload any configuration
      --config               - Configuration file path
      --doc                  - Process documentation folder, this will create the alert matrix file
      --mf format            - Define which alert matrix format to use (xlsx, csv, wiki. default: wiki)
      --version              - Version
    Command:
      init                   - Create configuration files and directories
      deploy                 - Deploy monitoring stack
      remove                 - Remove all configurations and stack deployed
      plugins                - Show a list of available plugins
