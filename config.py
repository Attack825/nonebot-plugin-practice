from pydantic import BaseModel, validator


class Config(BaseModel):
    # weather_api_key: str
    weather_command_priority: int = 10
    weather_plugin_enabled: bool = True

    @validator('weather_command_priority')
    def weather_command_priority_range(cls, v):
        if isinstance(v, int) and v >= 1:
            return v
        raise ValueError('weather_command_priority must be an integer greater than or equal to 1')
