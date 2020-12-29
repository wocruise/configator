#!/usr/bin/env python3

import logging
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..', 'src'))

from configator.envars import ev

# ev.prefix = 'EXAMPLE'
# ev.strict = True

DEFAULT_LOG_FORMAT = '%(asctime)s - pid:%(process)d - tid:%(thread)d - [%(levelname)-.1s] %(funcName)s:%(lineno)d - %(message)s'

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))

logging.basicConfig(level=logging.DEBUG, handlers=[consoleHandler])
