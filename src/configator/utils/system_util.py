#!/usr/bin/env python3

import os
import sys

def get_app_root(with_separator=True):
    __file__ = os.path.dirname(sys.modules['__main__'].__file__)
    abs_path = os.path.dirname(os.path.realpath(__file__))
    if with_separator:
        abs_path = abs_path + os.path.sep
    return abs_path
