from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .config import Config
from nonebot import get_driver  # 导入 driver
import requests

plugin_config = Config().parse_obj(get_driver().config)  # 获取插件配置


# 查看配置是否启用
async def is_enable() -> bool:
    return plugin_config.weather_plugin_enabled


# 直接使用 nonebot.params 模块中定义的参数类型来声明依赖。
weather = on_command("天气", rule=to_me() & is_enable, aliases={"weather", "查天气"},
                     priority=plugin_config.weather_plugin_enabled,
                     block=True)


@weather.handle()
async def handle_function(args: Message = CommandArg()):
    # 提取参数为纯文本为地名，并判断是否有效。
    if location := args.extract_plain_text():
        x: tuple = get_weather(location)
        await weather.finish(f"今天{location}天气是{x[0]}，最高温度{x[1]}℃，最低温度{x[2]}℃")
    else:
        await weather.finish("你要查询的地名是？")


def get_weather(location: str):
    params = {'location': location, 'key': '5999763e5ea147b09b491ef6700d45a7', "range": "cn"}
    get_location_url = "https://geoapi.qweather.com/v2/city/lookup"
    l = requests.get(url=get_location_url, params=params)
    location_params = l.json()['location'][0]['id']
    weather_params = {'location': location_params, 'key': '5999763e5ea147b09b491ef6700d45a7'}
    get_weather_url = "https://devapi.qweather.com/v7/weather/3d"
    x = requests.get(url=get_weather_url, params=weather_params)
    return x.json()['daily'][0]['textDay'], x.json()['daily'][0]['tempMax'], x.json()['daily'][0]['tempMin']
