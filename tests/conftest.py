import logging

import pytest
import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from os import getenv


@pytest.fixture(scope="session", autouse=True)
def load_bot():
    # 加载适配器
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)

    config = nonebot.get_driver().config

    # 加载配置文件
    config.weather_api_key = getenv("WEATHER_API_KEY")
    config.weather_command_priority = 10
    logging.info(config.weather_command_priority)
    config.weather_plugin_enabled = bool(getenv("WEATHER_PLUGIN_ENABLED"))

    # 加载插件
    # nonebot.load_plugin("nonebot_plugin_practice")
