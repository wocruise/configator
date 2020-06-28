#!/usr/bin/env python3

from configator.engine import RedisClient, CHANNEL_PATTERN

class SettingSubscriber(RedisClient):
    #
    def __init__(self, *args, **kwargs):
        super(SettingSubscriber, self).__init__(*args, **kwargs)
    #
    ##
    __s = None
    #
    @property
    def _sub(self):
        if self.__s is None:
            self.__s = self._connection.pubsub()
            self.__s.psubscribe(**{CHANNEL_PATTERN: self.event_handler})
        return self.__s
    #
    def event_handler(self, message):
        print(message)
    #
    ##
    __t = None
    #
    def start(self):
        if self.__t is None:
            self.__t = self._sub.run_in_thread(sleep_time=0.001)
        return self.__t
    #
    def stop(self):
        if self.__t is not None:
            self.__t.stop()
            self.__t = None
        self._sub.unsubscribe()
        self._destroy()
    pass
