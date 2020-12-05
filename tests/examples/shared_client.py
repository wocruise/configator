#!/usr/bin/env python3

import __init__

from datetime import datetime

from configator.engine.connector import RedisClient
from configator.engine import SettingSubscriber
from configator.utils.function import match_by_label, transform_json_data
from configator.utils.signfunc import hook_signal

#------------------------------------------------------------------------------

c = RedisClient()

#------------------------------------------------------------------------------

def trigger1(message, *args, **kwargs):
    print('1. clear the config')
def trigger2(message, *args, **kwargs):
    print('2. update the config: %s' % str(message))
def trigger3(message, *args, **kwargs):
    print('3. reset the engine')
    print()

s1 = SettingSubscriber(connector=c)
s1.set_transformer(transform_json_data)
s1.add_event_handler(match_by_label('PROXY_JOIN_SANDBOX'), trigger1, trigger2, trigger3)

s2 = SettingSubscriber(connector=c)
s2.set_transformer(transform_json_data)
s2.add_event_handler(match_by_label('PROXY_QUIT_SANDBOX'), trigger1, trigger2, trigger3)

def on_shutdown():
    s1.close()
    s2.close()

#------------------------------------------------------------------------------

from configator.engine import SettingPublisher

p = SettingPublisher(connector=c)

#------------------------------------------------------------------------------

if __name__ == "__main__":
    print("[+] starting subscriber")
    hook_signal(on_shutdown, finished=True)
    s1.start()
    s2.start()

    print("[-] send message to the s1")
    p.publish({"84973407138": "dev_8091", "time": datetime.now()}, label='PROXY_JOIN_SANDBOX',
            with_datetime=True, raise_on_error=True)

    print("[-] close the s1")
    s1.close()
    print()

    print("[-] send message to the s2")
    p.publish(["84973407138", "84982880412"], label='PROXY_QUIT_SANDBOX', raise_on_error=True)
    p.close()

    print("[-] finished")
