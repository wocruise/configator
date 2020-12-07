#!/usr/bin/env python3

from capsule1 import Controller

import logging
import time, threading
from configator.engine import SettingSubscriber
from configator.extensions.logging import LoggingConfigUpdater
from configator.utils.function import transform_json_data
from configator.utils.signfunc import hook_signal

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
        self._counter = 0
    #
    #
    def run(self):
        if self._running.is_set():
            return
        self._running.set()
        while self._running.is_set():
            time.sleep(1)
            self._counter += 1
            if logger.isEnabledFor(logging.DEBUG):
                logger.log(logging.DEBUG, 'Ping[%d]: %s' % (self._counter, str(self._controller.use_data())))
    #
    #
    def stop(self):
        self._running.clear()

if __name__ == "__main__":
    subscriber = SettingSubscriber()
    #
    controller = Controller()
    subscriber.register_receiver(controller.capsule)
    #
    logging_updater = LoggingConfigUpdater()
    subscriber.register_receiver(logging_updater.capsule)
    #
    server = SimpleServerThread(controller)
    def shutdown():
        server.stop()
        subscriber.close()
    hook_signal(shutdown, finished=True)
    subscriber.start()
    server.start()
