#!/usr/bin/env python3

import unittest

from functools import wraps
from configator.utils.function_util import apply_sequence_decorators

from configator.utils.function_util import build_url

class build_url__test(unittest.TestCase):

    def setUp(self):
        pass

    def test_ok(self):
        self.assertEqual(build_url(dict(host='localhost', port='4379', db=0)),
                'redis://localhost:4379/0')
        self.assertEqual(build_url(dict(scheme='redis-sentinel', host='localhost', port='4379', db=0)),
                'redis-sentinel://localhost:4379/0')
        self.assertEqual(build_url(dict(password='t0ps3cr3t', host='localhost', port='4379', db=0), hide_secret=True),
                'redis://*********@localhost:4379/0')
        self.assertEqual(build_url(dict(username='user', password='t0ps3cr3t', host='localhost', port='4379', db=0)),
                'redis://user:t0ps3cr3t@localhost:4379/0')


class apply_sequence_decorators__test(unittest.TestCase):

    def setUp(self):
        pass

    def test_ok(self):

        def makebold(fn):
            @wraps(fn)
            def wrapped(*args, **kwargs):
                return "<b>" + fn(*args, **kwargs) + "</b>"
            return wrapped

        def makeitalic(fn):
            @wraps(fn)
            def wrapped(*args, **kwargs):
                return "<i>" + fn(*args, **kwargs) + "</i>"
            return wrapped

        @apply_sequence_decorators(makebold, makeitalic)
        def say():
            return "hello world"

        self.assertEqual(say(), "<b><i>hello world</i></b>")
        self.assertEqual(say.__name__, "say")
