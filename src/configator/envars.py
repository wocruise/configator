#!/usr/bin/env python3

import os

class EnvHelper():
    #
    __freeze = False
    __prefix = None
    __uppercase = True
    __strict = False
    #
    @property
    def prefix(self):
        self.__freeze = True
        if self.__prefix is None:
            self.__prefix = os.getenv('PYTHON_ENV_VAR_PREFIX')
        return self.__prefix
    #
    @prefix.setter
    def prefix(self, val):
        if self.__freeze:
            raise ValueError('Environment prefix has used')
        if isinstance(val, str) and val:
            self.__prefix = val
            if self.__uppercase:
                self.__prefix = self.__prefix.upper()
        return val
    #
    @property
    def strict(self):
        return self.__strict
    #
    @strict.setter
    def strict(self, val):
        if isinstance(val, bool):
            self.__strict = val
        return val
    #
    def getenv(self, label, default=None, with_prefix=True):
        key = label
        if with_prefix:
            if self.prefix:
                prefix_key = self.prefix + '__' + label
                if prefix_key in os.environ or self.__strict:
                    key = prefix_key
        return os.getenv(key, default)

ev = EnvHelper()
