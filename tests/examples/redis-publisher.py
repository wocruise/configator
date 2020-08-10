#!/usr/bin/env python3

import __init__
import json

from configator.engine.publisher import SettingPublisher

p = SettingPublisher()

# p.publish(json.dumps({"84973407138": "dev_8091"}), label='PROXY_JOIN_SANDBOX')
err = p.publish({"84973407138": "dev_8091"}, label='PROXY_JOIN_SANDBOX')
if err:
  raise err
p.publish_or_error("Hello world", label='PROXY_STOP_SANDBOX')
