from requests_owm import weather


def test_weather_fetch():
    w = weather.get_current_weather_by_id(5780993)

    if w:
        print("Weather Retrieved. Verify the following on the website:")
        print("Temperature: {}K".format(w["temp"]))
        print("Weather Status: {}".format(w["weather_description"]))
        print("Humidity: {}".format(w["humidity"]))
        print("Clouds: {}".format(w["clouds"]))


def test_all():
    test_weather_fetch()


if __name__ == "__main__":
    test_all()
