# DEMO__SERVER_HOST=skelethon.com python3 tests/envars/demo.py

import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..', 'src'))

from configator.envars import ev
from configator.utils.function_util import json_dumps

ev.prefix = 'demo'
ev.strict = True

print('SERVER_HOST: ' + ev.getenv('SERVER_HOST'))

text, err = json_dumps(ev.get_stats(level='full'), indent=4)
print(text)
