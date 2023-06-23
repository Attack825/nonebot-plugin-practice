from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .config import WEATHER_PLUGIN_ENABLED, WEATHER_COMMAND_PRIORITY, WEATHER_API_KEY, Config
import requests
from nonebot import logger
from httpx import AsyncClient, Response


# 查看配置是否启用
async def is_enable() -> bool:
    if WEATHER_PLUGIN_ENABLED is False:
        logger.info("天气插件未启用")
    return WEATHER_PLUGIN_ENABLED


# 直接使用 nonebot.params 模块中定义的参数类型来声明依赖。
weather = on_command("天气", rule=is_enable, aliases={"weather", "查天气"},
                     priority=WEATHER_COMMAND_PRIORITY,
                     block=True)


@weather.handle()
async def handle_function(args: Message = CommandArg()):
    # 使用了 args 作为注入参数名，注入的内容为 CommandArg()，也就是消息命令后跟随的内容。
    # 提取参数为纯文本为地名，并判断是否有效。
    if location := args.extract_plain_text():
        logger.info(f"查询地名为{location}")
        w_date = Weather(location, WEATHER_API_KEY)
        x = await w_date.get_weather()
        await weather.finish(f"今天{location}天气是{x[0]}，最高温度{x[1]}℃，最低温度{x[2]}℃")
    else:
        await weather.finish("你要查询的地名是？")


class Weather:
    def __init__(self, location: str, api_key: str):
        self.location = location
        self.api_key = api_key
        self.location_id = ""
        self.location_url = "https://geoapi.qweather.com/v2/city/lookup"
        self.weather_url = "https://devapi.qweather.com/v7/weather/3d"

    async def get_location_id(self):
        location_params = {'location': self.location, 'key': self.api_key, "range": "cn"}
        async with AsyncClient() as client:
            resp = await client.get(url=self.location_url, params=location_params)
        self.location_id = resp.json()['location'][0]['id']

    async def get_weather(self) -> tuple:
        await self.get_location_id()
        weather_params = {'location': self.location_id, 'key': self.api_key}
        async with AsyncClient() as client:
            resp = await client.get(url=self.weather_url, params=weather_params)
        return resp.json()['daily'][0]['textDay'], resp.json()['daily'][0]['tempMax'], resp.json()['daily'][0][
            'tempMin']


