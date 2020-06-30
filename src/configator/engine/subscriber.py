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
