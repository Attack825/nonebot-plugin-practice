import pytest
import nonebot
# 导入适配器
from nonebot.adapters.console import Adapter as ConsoleAdapter
import os
from nonebug import NONEBOT_INIT_KWARGS

os.environ["ENVIRONMENT"] = "prod"


def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {"secret": os.getenv("INPUT_SECRET")}


@pytest.fixture(scope="session", autouse=True)
def load_bot():
    # 加载适配器
    driver = nonebot.get_driver()
    driver.register_adapter(ConsoleAdapter)

    # 加载插件
    nonebot.load_from_toml("D:\\Project\QQbot\\bot_xiaojie\\xiaojie\\pyproject.toml")
