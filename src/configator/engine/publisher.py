#!/usr/bin/env python3

import logging

from configator.engine import RedisClient, CHANNEL_GROUP

LOG = logging.getLogger(__name__)

class SettingPublisher(RedisClient):
    #
    CHANNEL_PREFIX = CHANNEL_GROUP + ':'
    #
    #
    def __init__(self, *args, **kwargs):
        super(SettingPublisher, self).__init__(**kwargs)
    #
    #
    def publish(self, message, postfix=None):
        if postfix is None:
            channel_name = CHANNEL_GROUP + postfix
        else:
            channel_name = self.CHANNEL_PREFIX + postfix
        #
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "publish() a message [%s] to channel [%s]", str(message), channel_name)
        #
        try:
            self.connect().publish(channel_name, message)
        except Exception as err:
            raise err
