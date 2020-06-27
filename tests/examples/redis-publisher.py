import __init__

from configator.engine.publisher import SettingPublisher

p = SettingPublisher()

p.publish('UPDATE_CONFIG_1')
p.publish('UPDATE_CONFIG_2')
