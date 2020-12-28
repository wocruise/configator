#!/usr/bin/env python3

def remove_prefix(s, prefix):
    if not s or not prefix:
        return s
    return s[len(prefix):] if s.startswith(prefix) else s
