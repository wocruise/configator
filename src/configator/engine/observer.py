#!/usr/bin/env python3

import time

from abc import abstractproperty, abstractmethod

class CapsuleObserver():
    #
    __tracking_enabled = None
    __skip_duplication = None
    __capsule_store = None
    #
    #
    def __init__(self, *args, **kwargs):
        self.__capsule_store = dict()
    #
    #
    def track(self, capsule):
        #
        key = capsule.label
        #
        if key not in self.__capsule_store:
            self.__capsule_store[key] = dict(
                timestamp=time.time(),
                count=1,
                capsule=capsule,
                history=[]
            )
        else:
            store = self.__capsule_store[key]
            store['count'] = store['count'] + 1
            store['history'].append(store['capsule'])
            store['capsule'] = capsule
        #
        return capsule
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
                else:
                    info[name] = str(obj)
            return info
        return { k: extract(v) for k, v in self.__capsule_store.items() }


class CapsuleObservable():
    __observer = CapsuleObserver()
    #
    #
    def _observe(self):
        self.__observer.track(self)
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
    @classmethod
    def stats(cls, **kwargs):
        return cls.__observer.stats(**kwargs)
