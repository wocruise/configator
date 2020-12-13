#!/usr/bin/env python3

import __init__

import uuid
from datetime import datetime

from configator.extensions.storage import SettingStorage

p = SettingStorage()
if __name__ == "__main__":
    p.store("conversation_settings", {
        "ttl": {
            "minutes": 30
        }
    })
    p.close()
    settings = p.get("conversation_settings")
    print(settings)
    p.close()
