#!/usr/bin/env python3

import threading

class ConstantMirror:
    #
    class _Store:
        pass
    #
    __lock = threading.Lock()
    #
    @classmethod
    def copy(cls, constants):
        with cls.__lock:
            if hasattr(constants, '__dict__'):
                const__dict__ = getattr(constants, '__dict__')
                for name in const__dict__:
                    if name.startswith( '__' ) : continue
                    setattr(cls._Store, name, const__dict__[name])
            return cls
    #
    @classmethod
    def look(cls):
        return cls._Store
    #
    @classmethod
    def keys(cls):
        keys = list()
        for name in cls._Store.__dict__:
            if name.startswith( '__' ) : continue
            keys.append(name)
        return keys
