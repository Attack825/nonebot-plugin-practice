from datetime import datetime

import pytest
from nonebug import App
from nonebot.adapters.console import User, Message, MessageEvent


# @pytest.mark.asyncio
# async def test_practice(app: App):
#     from xiaojie.plugins.nonebot_plugin_practice import Weather, CityNotFoundError
#
#     async with app.test_server():
#         config = get_driver().config
#         # api_key = config.weather_api_key
#         api_key = "5999763e5ea147b09b491ef6700d45a7"
#         w_data = Weather(location="上海", api_key=api_key)
#         try:
#             await w_data.get_weather()
#             assert w_data.location == "上海"
#             assert w_data.location_id == "101020100"
#         except CityNotFoundError:
#             pass


@pytest.mark.asyncio
async def test_weather(app: App):
    from xiaojie.plugins.nonebot_plugin_practice import weather

    event = MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message("/天气 北京"),
        user=User(id=123465789),
    )
    async with app.test_matcher(weather) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, message="今天北京天气是小雨，最高温度34℃，最低温度24℃", result=None)
        ctx.should_finished(weather)
# 修改后的配置无法导入测试
