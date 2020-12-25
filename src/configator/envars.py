#!/usr/bin/env python3

import os
import time

class EnvHelper():
    #
    __freeze = False
    __prefix = None
    __uppercase = True
    __strict = False
    __footprint = None
    #
    def __init__(self, *args, **kwargs):
        self.__tracking_enabled = True
        self.__footprint = None
    #
    def _track_env(self, key, value, info=None):
        if not self.__tracking_enabled:
            return self
        if self.__footprint is None:
            self.__footprint = dict()
        self.__footprint[key] = dict(value=value, time=time.time(), info=info)
        return self
    #
    @property
    def active_env_vars(self):
        return self.get_stats(includes=[])
    #
    def get_stats(self, includes=None):
        if self.__footprint is None:
            return dict()
        if includes is None:
            fields = None
        else:
            fields = ['value']
            if isinstance(includes, list) and includes and 'value' not in includes:
                fields = fields + includes
        def transform_env_var(item):
            if fields is None:
                return item
            if len(fields) == 1 and 'value' in fields:
                return item.get('value')
            return { k: v for k, v in item.items() if k in fields }
        return dict(
            prefix=self.prefix,
            strict=self.strict,
            values={ k: transform_env_var(v) for k, v in self.__footprint.items() }
        )
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
        used_key = label
        prefixed_key = None
        is_default = False
        if with_prefix:
            if self.prefix:
                prefixed_key = self.prefix + '__' + label
                if self.__strict:
                    used_key = prefixed_key
                else:
                    if prefixed_key not in os.environ and label in os.environ:
                        used_key = label
                    else:
                        used_key = prefixed_key
                if used_key not in os.environ:
                    is_default = True
        val = os.getenv(used_key, default)
        self._track_env(label, val, info=dict(
            with_prefix=with_prefix,
            prefixed_key=prefixed_key,
            used_key=used_key,
            is_default=is_default
        ))
        return val

ev = EnvHelper()
