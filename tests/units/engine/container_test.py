#!/usr/bin/env python3

import unittest

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from configator.engine import SettingCapsule
from configator.utils.function_util import json_dumps


class SettingCapsule__test(unittest.TestCase):

    def setUp(self):
        pass

    def test_ok(self):
        controller = Controller()
        #
        total = 20
        with ThreadPoolExecutor() as executor:
            futures = []
            results = list()
            for i in range(total):
                if i == 3:
                    futures.append(executor.submit(controller.capsule.refresh))
                else:
                    futures.append(executor.submit(controller.capsule.payload))
            for future in as_completed(futures):
                results.append(future.result())
        #
        cat = dict()
        for result in results:
            if isinstance(result, dict):
                timestamp = result.get('timestamp')
                if cat.get(timestamp) is None:
                    cat[timestamp] = []
                cat[timestamp].append(result)
        #
        #
        self.assertEqual(len(cat), 2)
        parts = list(cat.values())
        part0_len = len(parts[0])
        part1_len = len(parts[1])
        #
        len_min = min(part0_len, part1_len)
        len_max = max(part0_len, part1_len)
        self.assertEqual(len_min, 3)
        self.assertEqual(len_max, total - 1 - len_min)


class Controller():
    def __init__(self, *args, **kwargs):
        self.__capsule = SettingCapsule(label='example', loader=self.__load)
    #
    @property
    def capsule(self):
        return self.__capsule
    #
    def __load(self, *args, **kwargs):
        return {
            "timestamp": datetime.now().timestamp()
        }
