#!/usr/bin/env python3

import __init__
import json

from configator.engine.publisher import SettingPublisher

p = SettingPublisher()

p.publish(json.dumps({"84973407138": "dev_8091"}), label='PROXY_JOIN_SANDBOX')
p.publish('Hello world', label='PROXY_STOP_SANDBOX')
