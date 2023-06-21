from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .config import Config
from nonebot import get_driver  # 导入 driver

plugin_config = Config().parse_obj(get_driver().config)  # 获取插件配置


async def is_enable() -> bool:
    return plugin_config.weather_plugin_enabled


# 直接使用 nonebot.params 模块中定义的参数类型来声明依赖。
weather = on_command("天气", rule=is_enable(), aliases={"weather", "查天气"}, priority=plugin_config.weather_plugin_enabled, block=True)


@weather.handle()
async def handle_function(args: Message = CommandArg()):
    # 提取参数为纯文本为地名，并判断是否有效。
    if location := args.extract_plain_text():
        await weather.finish(f"今天{location}天气是。。。")
    else:
        await weather.finish("你要查询的地名是？")
