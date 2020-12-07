#!/usr/bin/env python3

import __init__

import uuid
from datetime import datetime

from configator.engine import SettingPublisher

p = SettingPublisher()

if __name__ == "__main__":
    err = p.publish({"84973407138": "dev_8091", "time": datetime.now()}, label='PROXY_JOIN_SANDBOX', with_datetime=True)
    if err:
        print(err)
    p.publish("Hello world", label='PROXY_STOP_SANDBOX', raise_on_error=True)
    p.publish({ "id": "empty", "uuid": str(uuid.uuid4()) }, label='CAPSULE_EXAMPLE', raise_on_error=True)
    p.publish({ "change_level_tasks": [{"module_name": "__main__", "level": "DEBUG"}] }, label='LOGGING_CONFIG', raise_on_error=True)
    p.close()
