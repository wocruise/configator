#!/usr/bin/env python3

import redis, os

CHANNEL_PATTERN = 'configator'

class RedisClient(object):
    #
    def __init__(self, *args, **kwargs):
        self.__host = os.getenv('CONFIGATOR_' + 'REDIS_HOST', 'localhost')
        self.__sort = int(os.getenv('CONFIGATOR_' + 'REDIS_PORT', '6379'))
    #
    ##
    __r = None
    #
    @property
    def _connection(self):
        if self.__r is None:
            self.__r = redis.StrictRedis(host=self.__host, port=self.__sort, db=0)
        return self.__r
    #
    @property
    def _is_connected(self):
        return self.__r is not None
    #
    def _destroy(self):
        if self.__r is not None:
            self.__r.close()
            self.__r = None
