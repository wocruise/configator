#!/usr/bin/env python3

def get_type_name(obj):
    return type(obj).__name__

def get_type_fullname(o):
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    return module + '.' + o.__class__.__name__

def str_to_int(value):
    try:
        return int(value), None
    except ValueError as err:
        return value, err
