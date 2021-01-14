#!/usr/bin/env python3

import threading
import time

from abc import abstractmethod
from inspect import currentframe
from typing import Dict, List, Optional, Union
from configator.utils.datetime_util import fromtimestamp, strftime
from configator.utils.trackback_util import CodeLocation

HISTORY_LENGTH = 10

class CapsuleObserver():
    #
    __thread_safe = None
    __lock = None
    __skip_duplication = None
    __capsule_store = None
    #
    #
    def __init__(self, *args, **kwargs):
        self.__thread_safe = True
        self.__lock = threading.Lock()
        self.__capsule_store = dict()
    #
    #
    @property
    def thread_safe(self):
        return self.__thread_safe
    #
    @thread_safe.setter
    def thread_safe(self, val):
        if isinstance(val, bool):
            self.__thread_safe = val
        return val
    #
    #
    def track(self, capsule, location=None):
        if not self.__thread_safe:
            return self.track_unsafe_threading(capsule=capsule, location=location)
        with self.__lock:
            return self.track_unsafe_threading(capsule=capsule, location=location)
    #
    def track_unsafe_threading(self, capsule, location=None):
        #
        key = capsule.label
        #
        if key not in self.__capsule_store:
            self.__capsule_store[key] = dict(
                count=1,
                capsule=capsule,
                timestamp=time.time(),
                history=[]
            )
        else:
            store = self.__capsule_store[key]
            self.__capsule_store[key] = dict(
                count=store['count'] + 1,
                capsule=capsule,
                timestamp=time.time(),
                history=store['history']
            )
            del store['history']
            self.__capsule_store[key]['history'].append(store)
            history = self.__capsule_store[key]['history']
            while len(history) > HISTORY_LENGTH:
                history.pop(0)
        #
        if isinstance(location, dict):
            self.__capsule_store[key]['location'] = location
        #
        return capsule
    #
    #
    def reset(self):
        info = dict()
        for k, v in self.__capsule_store.items():
            capsule = v.get('capsule')
            if capsule:
                capsule.reset()
                result = dict(ok=True)
            else:
                result = dict(ok=False)
            info[k] = result
        return info
    #
    #
    def stats(self, **kwargs):
        trails = self.__extract_active_capsules(**kwargs)
        return dict(
            total=len(trails),
            store=trails
        )
    #
    def __extract_active_capsules(self, **kwargs):
        def extract(trail):
            info = dict()
            for name, obj in trail.items():
                if name == 'capsule':
                    info[name] = obj.summarize(**kwargs)
                    continue
                if name == 'timestamp':
                    info[name] = strftime(fromtimestamp(obj))
                    continue
                if name == 'history':
                    continue
                info[name] = obj
            return info
        return { k: extract(v) for k, v in self.__capsule_store.items() }


class CapsuleObservable(CodeLocation):
    __observer = CapsuleObserver()
    #
    #
    def _observe(self):
        filename, lineno = self._get_filename_and_lineno(currentframe(), depth=2)
        self.__observer.track(self, location=dict(filename=filename, lineno=lineno))
    #
    #
    @property
    def summary(self):
        return self.summarize()
    #
    @abstractmethod
    def summarize(self, *args, **kwargs):
        pass
    #
    #
    @abstractmethod
    def reset(self, parameters: Optional[Union[Dict,List]] = None, lazy_load:bool=False, **kwargs):
        pass
    #
    #
    @classmethod
    def stats(cls, **kwargs):
        return cls.__observer.stats(**kwargs)
    #
    #
    @classmethod
    def observer(cls):
        return cls.__observer
