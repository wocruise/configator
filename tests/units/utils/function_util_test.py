#!/usr/bin/env python3

import unittest

from configator.utils.function import build_url


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
