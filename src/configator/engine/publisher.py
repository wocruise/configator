import redis, time, os

class SettingPublisher(object):
    #
    def __init__(self, *args, **kwargs):
        self.__host = os.getenv('CONFIGATOR_' + 'REDIS_HOST', 'localhost')
        self.__port = int(os.getenv('CONFIGATOR_' + 'REDIS_HOST', '6379'))
    #
    ##
    __r = None
    #
    @property
    def _connection(self):
        if self.__r is None:
            self.__r = redis.Redis(host=self.__host, port=self.__port, db=0)
        return self.__r
    #
    def publish(self, message):
        self._connection.publish('configator', message)
