from pydantic import BaseModel, validator, Extra
from nonebot import get_driver


class Config(BaseModel, extra=Extra.ignore):
    weather_api_key: str = None
    weather_command_priority: int = None
    weather_plugin_enabled: bool = False

    @validator('weather_command_priority')
    def weather_command_priority_range(cls, v):
        if isinstance(v, int) and v >= 1:
            return v
        raise ValueError('weather_command_priority must be an integer greater than or equal to 1')


plugin_config = Config.parse_obj(get_driver().config)
WEATHER_API_KEY = plugin_config.weather_api_key
WEATHER_COMMAND_PRIORITY = plugin_config.weather_command_priority
WEATHER_PLUGIN_ENABLED = plugin_config.weather_plugin_enabled
