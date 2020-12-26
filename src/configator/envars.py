#!/usr/bin/env python3

import os
import time

from inspect import currentframe, getframeinfo
from configator.utils.string_util import remove_prefix
from configator.utils.system_util import get_app_root

class EnvHelper():
    #
    __freeze = False
    __uppercase = True
    __prefix = None
    __strict = None
    __tracking_enabled = None
    __footprint = None
    __app_root_dir = get_app_root()
    #
    def __init__(self, *args, **kwargs):
        self.__prefix = None
        self.__strict = True
        self.__tracking_enabled = True
        self.__footprint = None
    #
    def _track_env(self, key, value, info=None):
        if not self.__tracking_enabled:
            return self
        #
        record = dict(value=value, time=time.time(), info=info)
        if self.__footprint is None:
            self.__footprint = dict()
        if key not in self.__footprint:
            self.__footprint[key] = dict(
                count=1,
                current=record,
                history=[]
            )
        else:
            store = self.__footprint[key]
            store['count'] = store['count'] + 1
            store['history'].append(store['current'])
            store['current'] = record
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
                return item.get('current').get('value')
            return { k: v for k, v in item.get('current').items() if k in fields }
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
        #
        val = os.getenv(used_key, default)
        #
        if self.__tracking_enabled:
            cf_back = currentframe().f_back
            self._track_env(label, val, info=dict(
                with_prefix=with_prefix,
                prefixed_key=prefixed_key,
                used_key=used_key,
                is_default=is_default,
                module= self.__remove_app_root_dir(getframeinfo(cf_back).filename),
                lineno=cf_back.f_lineno
            ))
        #
        return val
    #
    #
    def __remove_app_root_dir(self, module_file):
        return remove_prefix(module_file, self.__app_root_dir)

ev = EnvHelper()
