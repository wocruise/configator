#!/usr/bin/env python3

import redis, threading

from configator.engine import RedisClient, CHANNEL_PATTERN

class SettingSubscriber(RedisClient):
    #
    def __init__(self, *args, **kwargs):
        super(SettingSubscriber, self).__init__(*args, **kwargs)
    #
    ##
    @property
    def pubsub(self):
        ps = self.connect().pubsub()
        ps.psubscribe(**{CHANNEL_PATTERN: self.event_handler})
        return ps
    #
    ##
    __t = None
    #
    def start(self):
        if self.__t is None:
            self.__t = self.__run_in_thread(sleep_time=0.001)
        return self.__t
    #
    def stop(self):
        if self.__t is not None:
            self.__t.stop()
            self.__t = None
        self._destroy()
    #
    def __run_in_thread(self, sleep_time=0):
        thread = PubSubWorkerThread(self, sleep_time)
        thread.start()
        return thread
    #
    ##
    __event_mappings = None
    #
    def register(self, match, clear, reset):
        if self.__event_mappings is None:
            self.__event_mappings = dict()
        if not (callable(match) and (callable(clear) or callable(reset))):
            raise ArgumentError('match-clear-reset must be callable')
        self.__event_mappings[match] = (clear, reset)
    #
    def event_handler(self, message):
        if self.__event_mappings is None:
            return
        for match, reaction in self.__event_mappings.items():
            clear, reset = reaction
            if match(message):
                if callable(clear):
                    clear()
                if callable(reset):
                    reset()


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
    #
    #
    def stop(self):
        self._running.clear()
