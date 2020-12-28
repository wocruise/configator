#!/usr/bin/env python3

import unittest

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from configator.extensions.storage import SettingStorage
from configator.utils.function_util import json_dumps


class SettingStorage__test(unittest.TestCase):
    ai = None

    def setUp(self):
        self.ai = SettingStorage(topic='test_store')

    def tearDown(self):
        self.ai.clear(key="my_config")
        self.ai.close()

    def test_ok(self):
        config = {
            "id": "1234567890",
            "width": 800,
            "height": 600,
            "enabled": True,
            "PI": 3.14159
        }
        self.ai.store(key="my_config", obj=config)
        result = self.ai.get(key="my_config")
        self.assertEqual(result, config)
