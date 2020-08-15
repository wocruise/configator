#!/usr/bin/env python3

import __init__
import signal

from configator.engine.subscriber import SettingSubscriber
from configator.utils.function import match_by_label, transform_json_data

s = SettingSubscriber()

def c1(message, *args, **kwargs):
    print('clear the setting #1')
def r1(message, *args, **kwargs):
    print('reset the service #1: %s' % str(message))
def s1(message, *args, **kwargs):
    print('post-processing for the setting #1')

s.set_transformer(transform_json_data)
s.add_event_handler(match_by_label(b'PROXY_JOIN_SANDBOX'), c1, r1, s1)

def signal_handler(signal, frame):
    print()
    print("[-] SIGINT received")
    s.stop()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    print("[+] starting subscriber")
    s.start()
    print("[-] waiting for messages")
