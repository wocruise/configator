import redis, time, os

class SettingSubscriber(object):
    #
    def __init__(self, *args, **kwargs):
        self.__host = os.getenv('CONFIGATOR_' + 'REDIS_HOST', 'localhost')
        self.__sort = int(os.getenv('CONFIGATOR_' + 'REDIS_HOST', '6379'))
    #
    ##
    __r = None
    #
    @property
    def _connection(self):
        if self.__r is None:
            self.__r = redis.Redis(host=self.__host, port=self.__sort, db=0)
        return self.__r
    #
    ##
    __s = None
    #
    @property
    def _sub(self):
        if self.__s is None:
            self.__s = self._connection.pubsub()
            self.__s.psubscribe(**{'configator': self.event_handler})
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
        self._connection.close()
    pass
