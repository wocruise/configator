#!/usr/bin/env python3

import __init__
import logging
import uuid

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from configator.engine.container import SettingCapsule
# from configator.legacy.container import SettingCapsule
from configator.utils.function_util import json_dumps

logger = logging.getLogger(__name__)

class Controller():
    def __init__(self, *args, **kwargs):
        self.__capsule = SettingCapsule(label='CAPSULE_EXAMPLE',
                loader=self.load,
                default=dict(uuid='553dd766-9176-4970-9a1c-aacada948b28'),
                on_refresh=self.on_refresh)
    #
    @property
    def capsule(self):
        return self.__capsule
    #
    def load(self, *args, uuid=None, **kwargs):
        if len(args) > 0:
            if logger.isEnabledFor(logging.WARN):
                logger.log(logging.WARN, 'Redundant position arguments: %s', str(args))
        if len(kwargs) > 0:
            if logger.isEnabledFor(logging.WARN):
                logger.log(logging.WARN, 'Redundant keyword arguments: %s', str(kwargs))
        return {
            "timestamp": datetime.now().timestamp(),
            "uuid": uuid
        }
    #
    def use_data(self):
        return self.capsule.payload(uuid=str(uuid.uuid4()))
    #
    def refresh(self):
        self.capsule.refresh(parameters=dict(uuid=str(uuid.uuid4())))
        return None
    #
    @staticmethod
    def on_refresh(name, timestamp):
        print('Reset the [' + name + '] @ ' + str(timestamp))


if __name__ == "__main__":

    controller = Controller()

    total = 20
    with ThreadPoolExecutor() as executor:
        futures = []
        results = list()
        for i in range(total):
            if i == 3:
                futures.append(executor.submit(controller.refresh))
            else:
                futures.append(executor.submit(controller.use_data))
        for future in as_completed(futures):
            results.append(future.result())

    cat = dict()
    for result in results:
        if isinstance(result, dict):
            timestamp = result.get('timestamp')
            if cat.get(timestamp) is None:
                cat[timestamp] = []
            cat[timestamp].append(result)

    out, err = json_dumps(cat, indent=4)
    print(err)
    print(out)

    if hasattr(controller.capsule, 'summary'):
        print(controller.capsule.summary)
    if hasattr(SettingCapsule, 'stats'):
        print(SettingCapsule.stats())
