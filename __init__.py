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
        x: tuple = await get_weather(location)
        await weather.finish(f"今天{location}天气是{x[0]}，最高温度{x[1]}℃，最低温度{x[2]}℃")
    else:
        await weather.finish("你要查询的地名是？")


async def get_location_id(location: str):
    params = {'location': location, 'key': WEATHER_API_KEY, "range": "cn"}
    get_location_url = "https://geoapi.qweather.com/v2/city/lookup"
    async with AsyncClient() as client:
        resp = await client.get(url=get_location_url, params=params)
    location_params = resp.json()['location'][0]['id']
    logger.info(f"查询地名为{location}的id为{location_params}")
    return location_params


async def get_weather(location: str):
    location_params = await get_location_id(location)
    weather_params = {'location': location_params, 'key': WEATHER_API_KEY}
    get_weather_url = "https://devapi.qweather.com/v7/weather/3d"
    async with AsyncClient() as client:
        pokemon = await client.get(url=get_weather_url, params=weather_params)
    return pokemon.json()['daily'][0]['textDay'], pokemon.json()['daily'][0]['tempMax'], pokemon.json()['daily'][0][
        'tempMin']


