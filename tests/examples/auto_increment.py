#!/usr/bin/env python3

import __init__

import uuid
from datetime import datetime

from configator.extensions.sequence import AutoIncrement

p = AutoIncrement()
if __name__ == "__main__":
    p.init("mykey")
    for i in range(10):
        print("[%d] - value: %d" % (i + 1, p.incr("mykey")))
    p.close()
