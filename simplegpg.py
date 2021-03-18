"""
SimpleGPG is a thin wrapper over `OpenPGP` respective the `gpg` command in linux.
SimpleGPG provides a simple text user interface where it guides the user through.

All crypto operation inputs and outputs are based
on the PGP format. Therefore SimpleGPG can be used in addition to OpenPGP or other PGP
tools.
"""
import os
import argparse
from simplegpgimpl import SimpleGPG

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--homedir", help="Set the name of the home directory to HOMEDIR. If this option is not used, "
                                          "the default home directory ‘~/.gnupg’ will be selected.")
    args = parser.parse_args()
    home_dir = os.path.expanduser("~/.gnupg")
    if args.homedir:
        home_dir = args.homedir

    SimpleGPG(home_dir).main_menu()
