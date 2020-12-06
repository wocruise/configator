#!/usr/bin/env python3

import logging
import time, threading
from configator.engine import SettingSubscriber
from configator.utils.function import transform_json_data
from configator.utils.signfunc import hook_signal
from capsule1 import Controller

logger = logging.getLogger(__name__)

class SimpleServerThread(threading.Thread):
    def __init__(self, controller, sleep_time=0.01, daemon=False):
        super(SimpleServerThread, self).__init__()
        self.daemon = daemon
        #
        self._controller = controller
        self._sleep_time = sleep_time
        #
        self._running = threading.Event()
    #
    #
    def run(self):
        if self._running.is_set():
            return
        self._running.set()
        while self._running.is_set():
            time.sleep(1)
            print('Ping: ' + str(self._controller.use_data()))
    #
    #
    def stop(self):
        self._running.clear()

if __name__ == "__main__":
    controller = Controller()
    subscriber = SettingSubscriber()
    subscriber.set_transformer(transform_json_data)
    subscriber.register_receiver(controller.capsule)
    server = SimpleServerThread(controller)
    def shutdown():
        server.stop()
        subscriber.close()
    hook_signal(shutdown, finished=True)
    subscriber.start()
    server.start()
