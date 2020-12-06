#!/usr/bin/env python

import logging
import threading
import time

from readerwriterlock import rwlock
from typing import Callable, Dict, Optional

LOG = logging.getLogger(__name__)

class SettingCapsule():
    __name = None
    __load = None
    __data = None
    __on_reset = None
    __on_pre_load = None
    __on_load_error = None
    __on_post_load = None
    #
    #
    def __init__(self, name: str, load: Callable,
            on_reset:Optional[Callable]=None,
            on_pre_load:Optional[Callable]=None,
            on_post_load:Optional[Callable]=None,
            on_load_error:Optional[Callable]=None):
        assert isinstance(name, str) and name, "[name] must be a string and not empty"
        self.__name = name
        #
        assert callable(load), "[load] must be a function"
        self.__load = load
        #
        if callable(on_reset):
            self.__on_reset = on_reset
        else:
            self.__on_reset = default_on_reset
        #
        if callable(on_pre_load):
            self.__on_pre_load = on_pre_load
        else:
            self.__on_pre_load = default_on_pre_load
        #
        if callable(on_post_load):
            self.__on_post_load = on_post_load
        else:
            self.__on_post_load = default_on_post_load
        #
        if callable(on_load_error):
            self.__on_load_error = on_load_error
        else:
            self.__on_load_error = default_on_load_error
        #
        self.__load_lock = threading.RLock()
        self.__rwhandler = rwlock.RWLockFairD()
    #
    #
    @property
    def name(self):
        return self.__name
    #
    #
    @property
    def data(self):
        with self.__rwhandler.gen_rlock():
            if self.__data is None:
                self.__reload()
            return self.__data
    #
    #
    def reset(self, message: Optional[Dict] = None, err: Optional[Exception] = None):
        with self.__rwhandler.gen_wlock():
            self.__data = None
            if callable(self.__on_reset):
                self.__on_reset(self.__name, time.time())
        return self
    #
    #
    def __reload(self):
        with self.__load_lock:
            if self.__data is None:
                try:
                    if callable(self.__on_pre_load):
                        self.__on_pre_load(self.__name, time.time())
                    #
                    self.__data = self.__load()
                    #
                    if callable(self.__on_post_load):
                        self.__on_post_load(self.__name, time.time())
                except Exception as exception:
                    if callable(self.__on_load_error):
                        self.__on_load_error(self.__name, time.time(), exception)
                    raise exception


def default_on_reset(name, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] reset the [data] to None', name)

def default_on_pre_load(name, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] invoke the load() to load the data', name)

def default_on_post_load(name, timestamp):
    if LOG.isEnabledFor(logging.DEBUG):
        LOG.log(logging.DEBUG, 'SettingCapsule[%s] save result of load() to the store', name)

def default_on_load_error(name, timestamp, error):
    if LOG.isEnabledFor(logging.ERROR):
        LOG.log(logging.ERROR, 'SettingCapsule[%s] error on call to load() function', name)
