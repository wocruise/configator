#!/usr/bin/env python3

import atexit
import logging
import redis, threading, traceback, sys

from configator.engine import RedisClient, CHANNEL_GROUP
from typing import Any, Callable, List, Tuple, Dict, Optional

LOG = logging.getLogger(__name__)

class SettingSubscriber(RedisClient):
    #
    CHANNEL_PATTERN = CHANNEL_GROUP + '*'
    #
    def __init__(self, *args, auto_stop=True, **kwargs):
        if auto_stop:
            atexit.register(self.stop)
        super(SettingSubscriber, self).__init__(**kwargs)
    #
    ##
    @property
    def pubsub(self):
        ps = self.connect().pubsub()
        ps.psubscribe(**{self.CHANNEL_PATTERN: self.__process_event})
        return ps
    #
    ##
    __t = None
    #
    def start(self):
        if self.__t is None:
            self.__t = self.__run_in_thread(sleep_time=0.001)
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.log(logging.DEBUG, "SettingSubscriber has started")
        return self.__t
    #
    def stop(self):
        if self.__t is not None:
            self.__t.stop()
            self.__t = None
        self._destroy()
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "SettingSubscriber has stopped")
    #
    def __run_in_thread(self, sleep_time=0):
        thread = PubSubWorkerThread(self, sleep_time)
        thread.start()
        return thread
    #
    ##
    __transformer = None
    #
    def set_transformer(self, transformer: Callable[[Dict], Tuple[Dict, Any]]):
        if callable(transformer):
            self.__transformer = transformer
        return self
    #
    ##
    __event_mappings = None
    #
    def add_event_handler(self, match: Callable[[Dict, Any], bool],
            clear: Optional[Callable[[Dict, Any], None]],
            reset: Optional[Callable[[Dict, Any], None]]):
        if self.__event_mappings is None:
            self.__event_mappings = dict()
        if not (callable(match) and (callable(clear) or callable(reset))):
            raise ArgumentError('match-clear-reset must be callable')
        self.__event_mappings[match] = (clear, reset)
        return self
    #
    def __process_event(self, message):
        if self.__event_mappings is None:
            return
        #
        if self.__transformer is not None:
            msg, err = self.__transformer(message)
        else:
            msg, err = (message, None)
        #
        for match, reaction in self.__event_mappings.items():
            clear, reset = reaction
            if match(msg, err):
                if callable(clear):
                    clear(msg, err)
                if callable(reset):
                    reset(msg, err)


class PubSubWorkerThread(threading.Thread):
    def __init__(self, redis_client, sleep_time, daemon=False):
        super(PubSubWorkerThread, self).__init__()
        self.daemon = daemon
        #
        self.redis_client = redis_client
        self.sleep_time = sleep_time
        #
        self._running = threading.Event()
    #
    #
    def run(self):
        if self._running.is_set():
            return
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "PubSubWorkerThread is starting")
        self._running.set()
        while self._running.is_set():
            try:
                pubsub = self.redis_client.pubsub
                while self._running.is_set():
                    pubsub.get_message(ignore_subscribe_messages=True, timeout=self.sleep_time)
                pubsub.close()
            except redis.ConnectionError:
                self.redis_client.reconnect()
            except Exception as err:
                traceback.print_exc(file=sys.stdout)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "PubSubWorkerThread has stopped")
    #
    #
    def stop(self):
        self._running.clear()
