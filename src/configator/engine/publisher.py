#!/usr/bin/env python3

from configator.engine import RedisClient, CHANNEL_PATTERN

class SettingPublisher(RedisClient):
    #
    def __init__(self, *args, **kwargs):
        super(SettingPublisher, self).__init__(*args, **kwargs)
    #
    def publish(self, message):
        self._connection.publish(CHANNEL_PATTERN, message)
