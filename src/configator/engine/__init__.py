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
    #
    def connect(self):
        waiting = True
        while waiting:
            try:
                connection = self._connection
                waiting = False
                return connection
            except redis.ConnectionError:
                pass
    #
    #
    def reconnect(self):
        self._destroy()
        return self.connect()
    #
    #
    @property
    def _connection(self):
        if self.__r is None:
            pool = redis.ConnectionPool(host=self.__host, port=self.__sort, db=0)
            self.__r = redis.Redis(connection_pool=pool)
        return self.__r
    #
    #
    def _destroy(self):
        if self.__r is not None:
            self.__r.close()
            self.__r = None
