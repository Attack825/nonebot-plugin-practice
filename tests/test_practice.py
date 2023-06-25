import pytest
from nonebug import App
from nonebot import get_driver


@pytest.mark.asyncio
async def test_practice(app: App):
    from xiaojie.plugins.nonebot_plugin_practice import Weather, CityNotFoundError

    async with app.test_server():
        config = get_driver().config
        # api_key = config.weather_api_key
        api_key = "5999763e5ea147b09b491ef6700d45a7"
        w_data = Weather(location="上海", api_key=api_key)
        try:
            await w_data.get_weather()
            assert w_data.location == "上海"
            assert w_data.location_id == "101020100"
        except CityNotFoundError:
            pass
