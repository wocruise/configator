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
    __p = None
    __r = None
    #
    @property
    def _connection(self):
        if self.__p is None:
            self.__p = redis.BlockingConnectionPool(timeout=120, host=self.__host, port=self.__sort, db=0)
        if self.__r is None:
            self.__r = redis.Redis(connection_pool=self.__p)
        return self.__r
    #
    @property
    def _is_connected(self):
        return self.__r is not None
    #
    def _destroy(self):
        if self.__p is not None:
            self.__p.disconnect()
        if self.__r is not None:
            self.__r.close()
            self.__r = None
