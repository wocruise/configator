#!/usr/bin/env python3

import unittest
# from importlib import reload

from configator.consts import ConstantMirror

class ConstantMirror__copy__test(unittest.TestCase):
    #
    def test_ok(self):
        class Constant1:
            LOGGING_MODULE_NAMES = [
                '__main__', '__CHATBOT__', '__ROUTINE__',
                'adapters', 'configator', 'controllers', 'cronjobs', 'flows', 'formatters', 'redant',
            ]
            MAX = 100
        #
        class Constant2:
            MAX = 200
        #
        ConstantMirror.copy(Constant1).copy(Constant2)
        #
        MyStore = ConstantMirror.look()
        #
        self.assertEqual(MyStore.LOGGING_MODULE_NAMES, Constant1.LOGGING_MODULE_NAMES)
        self.assertEqual(MyStore.MAX, Constant2.MAX)
    #
    def test_invalid_input(self):
        ConstantMirror.copy(100)
        ConstantMirror.copy("Hello world")
        class EmptyClass:
            pass
        ConstantMirror.copy(EmptyClass)
        self.assertEqual(ConstantMirror.keys(), [])
