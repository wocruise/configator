import __init__
import json

from configator.engine.publisher import SettingPublisher

p = SettingPublisher()

p.publish(json.dumps({}), postfix='UPDATE_CONFIG_1')
p.publish('Hello world', postfix='UPDATE_CONFIG_2')
