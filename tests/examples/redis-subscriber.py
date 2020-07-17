
import __init__
from configator.engine.subscriber import SettingSubscriber
from typing import Dict, Tuple, Any
import atexit, sys, time

class ExampleController():
    #
    def __init__(self, *args, **kwargs):
        pass
    #

s = SettingSubscriber()

# def t1(message:Dict) -> Tuple[Any, Any]:
#     print(str(message))
#     return message, None

def t1(message):
    print(str(message))
    return message, None

def m1(message, *args, **kwargs):
    return isinstance(message, dict) and message.get('data') == b'UPDATE_CONFIG_1'
def c1(message, *args, **kwargs):
    print('clear the setting #1')
def r1(message, *args, **kwargs):
    print('reset the service #1')

s.set_transformer(t1)
s.add_event_handler(m1, c1, r1)
atexit.register(s.stop)

if __name__ == "__main__":
    try:
        print("[+] starting subscriber")
        s.start()
        print("[-] waiting for messages")
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        s.stop()
    except Exception:
        # traceback.print_exc(file=sys.stdout)
        sys.exit(0)
