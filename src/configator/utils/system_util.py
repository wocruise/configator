#!/usr/bin/env python3

import os
import sys

def get_app_root(with_separator=True):
    main_module = sys.modules.get('__main__')
    if main_module and hasattr(main_module, '__file__'):
        dir_path = os.path.dirname(main_module.__file__)
        abs_path = os.path.dirname(os.path.realpath(dir_path))
        if with_separator:
            abs_path = abs_path + os.path.sep
        return abs_path
    return None
