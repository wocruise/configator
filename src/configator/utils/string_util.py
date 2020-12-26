#!/usr/bin/env python3

def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s
