#!/usr/bin/env python3

import __init__

from configator.engine import SettingSubscriber
from configator.utils.function_util import match_by_label, transform_json_data
from configator.utils.signal_util import hook_signal

s = SettingSubscriber()

def c1(message, *args, **kwargs):
    print('1. clear the setting #1')
def r1(message, *args, **kwargs):
    print('2. reset the service #1: %s' % str(message))
def s1(message, *args, **kwargs):
    print('3. update the filter #1')
    print()

s.set_transformer(transform_json_data)
s.add_event_handler(match_by_label('PROXY_JOIN_SANDBOX'), c1, r1, s1)

if __name__ == "__main__":
    print("[+] starting subscriber")
    hook_signal(s.close, finished=True)
    s.start()
    print("[-] waiting for messages")
