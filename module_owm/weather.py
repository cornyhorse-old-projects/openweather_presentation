import pyowm
from database.credentials import get_credentials


def owm_connect():
    api_key = get_credentials().password
    return pyowm.OWM(api_key)


def get_owm_id(owm, location_name="Salt Lake City"):
    reg = owm.city_id_registry()
    return reg.ids_for(location_name)


def get_current_weather_by_id(owm, location_id):
    return owm.weather_at_id(location_id)
