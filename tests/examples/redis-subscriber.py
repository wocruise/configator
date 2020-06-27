
import __init__
from configator.engine.subscriber import SettingSubscriber

import atexit, sys, time

if __name__ == "__main__":
    s = SettingSubscriber()
    atexit.register(s.stop)
    print("[+] starting subscriber")
    s.start()
    print("[-] waiting for messages")
    # try:
    #     # time.sleep(2)
    #     # s.stop()
    # except KeyboardInterrupt:
    #     print("Shutdown requested...exiting")
    # except Exception:
    #     # traceback.print_exc(file=sys.stdout)
    #     pass
    # # sys.exit(0)
