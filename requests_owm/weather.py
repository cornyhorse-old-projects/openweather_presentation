import requests
from database import credentials
from pprint import pprint
import json


def parse_content(content):
    content = content.decode()
    content = json.loads(content)

    content_dict = {
        'lat': content.get('coord').get('lat'),
        'lon': content.get('coord').get('lon'),
        'dt': content.get('dt'),
        'temp': content.get('main').get('temp'),
        'temp_max': content.get('main').get('temp_max'),
        'temp_min': content.get('main').get('temp_min'),
        'pressure': content.get('main').get('pressure'),
        'humidity': content.get('main').get('humidity'),
        'id': content.get('id'),
        'cod': content.get('cod'),
        'clouds': content.get('all'),
        'city': content.get('name'),
        'country': content.get('sys').get('country'),
        'sunrise': content.get('sys').get('sunrise'),
        'sunset': content.get('sys').get('sunset'),
        'visibility': content.get('sys').get('visibility'),
        'weather_description': content.get('weather')[0].get('description'),
        'weather_icon': content.get('weather')[0].get('icon'),
        'weather_type': content.get('weather')[0].get('main'),
        'weather_id': content.get('weather')[0].get('id'),
        'wind_degrees':content.get('wind').get('deg'),
        'wind_speed_kmh': content.get('wind').get('speed')
    }

    if content.get('rain'):
        content['rain'] = content.get('rain').get('1h')

    return content_dict

def get_current_weather_by_id(id=5780993):
    app_id = credentials.get_credentials().password
    api_string = 'http://api.openweathermap.org/data/2.5/weather?id={id}&APPID={app_id}'.format(id=id,app_id=app_id)
    weather = requests.get(api_string)
    content_dict = parse_content(weather.content)
    return content_dict