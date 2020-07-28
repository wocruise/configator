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
    def publish(self, message, label=None):
        try:
            self.publish_or_error(message, label=label)
            return None
        except Exception as err:
            return err
    #
    #
    def publish_or_error(self, message, label=None):
        if label is None:
            channel_name = CHANNEL_GROUP
        else:
            channel_name = self.CHANNEL_PREFIX + label
        #
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "publish() a message [%s] to channel [%s]", str(message), channel_name)
        #
        self.connect().publish(channel_name, message)
