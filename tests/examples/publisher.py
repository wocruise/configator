#!/usr/bin/env python3

import __init__
from datetime import datetime

from configator.engine.publisher import SettingPublisher

p = SettingPublisher()

if __name__ == "__main__":
    # p.publish(json.dumps({"84973407138": "dev_8091"}), label='PROXY_JOIN_SANDBOX')
    err = p.publish({"84973407138": "dev_8091", "time": datetime.now()}, label='PROXY_JOIN_SANDBOX', with_datetime=True)
    if err:
        raise err
    p.publish_or_error("Hello world", label='PROXY_STOP_SANDBOX')

    p.close()
