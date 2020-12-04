#!/usr/bin/env python3

import __init__
from datetime import datetime

from configator.engine import SettingPublisher

p = SettingPublisher()

if __name__ == "__main__":
    err = p.publish({"84973407138": "dev_8091", "time": datetime.now()}, label='PROXY_JOIN_SANDBOX', with_datetime=True)
    if err:
        print(err)
    p.publish("Hello world", label='PROXY_STOP_SANDBOX', raise_on_error=True)

    p.close()
