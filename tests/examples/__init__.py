#!/usr/bin/env python

import logging
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..', 'src'))

DEFAULT_LOG_FORMAT = '%(asctime)s - pid:%(process)d - tid:%(thread)d - [%(levelname)-.1s] %(funcName)s:%(lineno)d - %(message)s'

logging.basicConfig(level=logging.DEBUG, format=DEFAULT_LOG_FORMAT)
