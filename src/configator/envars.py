#!/usr/bin/env python3

import os
import time

from inspect import currentframe
from configator.utils.trackback_util import CodeLocation
from configator.utils.function_util import dict_update

EMPTY_DICT = dict()

class EnvHelper(CodeLocation):
    #
    __freeze = False
    __uppercase = True
    __prefix = None
    __strict = None
    __tracking_enabled = None
    __footprint = None
    #
    def __init__(self, *args, **kwargs):
        self.__prefix = None
        self.__strict = True
        self.__tracking_enabled = True
        self.__footprint = dict()
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
        return self.get_stats()
    #
    def get_stats(self, level=None):
        trails = None
        if level == 'current':
            trails = self.__extract_current_states()
        elif level == 'full':
            trails = self.__extract_full_footprint()
        #
        return dict_update(
            dict(
                prefix=self.prefix,
                strict=self.strict,
                values=self.__extract_values()
            ),
            dict(trails=trails), trails is not None)
    #
    def __extract_values(self):
        def extract(trail):
            return trail.get('current', EMPTY_DICT).get('value')
        return { k: extract(v) for k, v in self.__footprint.items() }
    #
    def __extract_current_states(self):
        def extract(trail):
            return trail.get('current')
        return { k: extract(v) for k, v in self.__footprint.items() }
    #
    def __extract_full_footprint(self):
        def extract(trail):
            return dict(trail)
        return { k: extract(v) for k, v in self.__footprint.items() }
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
    @property
    def tracking_enabled(self):
        return self.__tracking_enabled
    #
    @tracking_enabled.setter
    def tracking_enabled(self, val):
        if isinstance(val, bool):
            self.__tracking_enabled = val
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
            filename, lineno = self._get_filename_and_lineno(currentframe())
            self._track_env(label, val, info=dict(
                with_prefix=with_prefix,
                prefixed_key=prefixed_key,
                used_key=used_key,
                is_default=is_default,
                module= filename,
                lineno=lineno
            ))
        #
        return val

ev = EnvHelper()
