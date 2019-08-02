import module_owm.weather as weather


def test_connection():
    owm = weather.owm_connect()
    if owm:
        print("Connected to the weather api!")
        return owm

def test_location_fetch(owm):
    city_id = weather.get_owm_id(owm, 'Salt Lake City')
    if city_id[0][0] == 5780993 and city_id[0][1] == 'Salt Lake City' and city_id[0][2] == 'US':
        print("Salt Lake ID Correct! ({})".format(5780993))

def test_weather_fetch(owm):
    current_weather = weather.get_current_weather_by_id(owm, 5780993)
    w = current_weather.get_weather()

    clouds = w.get_clouds()
    humidity = w.get_humidity()
    # Ensure that temperature is returned in freedom units.
    temp = w.get_temperature('fahrenheit')['temp']
    status = w.get_status()
    if temp:
        print("Weather Retrieved. Verify the following on the website:")
        print("Temperature: {}F".format(temp))
        print("Weather Status: {}".format(status))
        print("Humidity: {}".format(humidity))
        print("Clouds: {}".format(clouds))

if __name__ == '__main__':
    owm = test_connection()
    test_location_fetch(owm)
    test_weather_fetch(owm)