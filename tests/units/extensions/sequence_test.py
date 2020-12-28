#!/usr/bin/env python3

import unittest

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from configator.extensions.sequence import AutoIncrement
from configator.utils.function_util import json_dumps


class AutoIncrement__test(unittest.TestCase):
    ai = None

    def setUp(self):
        self.ai = AutoIncrement(topic='testid')
        self.ai.reset()

    def tearDown(self):
        self.ai.close()

    def test_ok(self):
        total = 10
        with ThreadPoolExecutor() as executor:
            futures = []
            results = set()
            for i in range(total):
                futures.append(executor.submit(self.ai.incr))
            for future in as_completed(futures):
                results.add(future.result())
        self.assertEqual(len(results), total)
