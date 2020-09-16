
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'

import sys
from os import environ, path

import yaml

from pythonpath import add_dir_to_pythonpath


def main(mode=0):
    """
    Main function. 
    
    """

    from worker import NFCWorker
    from definitions import ROOT_DIR


    nfcworker = NFCWorker()
    nfcworker.run()



if __name__ == "__main__":

    mode = 0

    if 'local' in sys.argv:
        mode = 1

    add_dir_to_pythonpath()
    main(mode=mode)