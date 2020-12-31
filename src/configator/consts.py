#!/usr/bin/env python3

class ConstantMirror:
    #
    class _Store:
        pass
    #
    @classmethod
    def copy(cls, constants):
        for name in constants.__dict__:
            if name.startswith( '__' ) : continue
            setattr(cls._Store, name, constants.__dict__[name])
        return cls
    #
    @classmethod
    def look(cls):
        return cls._Store
