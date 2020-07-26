#!/usr/bin/env python3

import __init__
import sys, traceback

from configator.engine.subscriber import SettingSubscriber
from configator.utils.function import match_by_label, transform_json_data

s = SettingSubscriber()

def c1(message, *args, **kwargs):
    print('clear the setting #1')
def r1(message, *args, **kwargs):
    print('reset the service #1: %s' % str(message))

s.set_transformer(transform_json_data)
s.add_event_handler(match_by_label(b'PROXY_JOIN_SANDBOX'), c1, r1)

if __name__ == "__main__":
    try:
        print("[+] starting subscriber")
        s.start()
        print("[-] waiting for messages")
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        s.stop()
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)
