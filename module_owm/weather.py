import pyowm
from database.credentials import get_credentials
from database import models as m
import pytz
import datetime
from dateutil import tz


def owm_connect():
    api_key = get_credentials().password
    return pyowm.OWM(api_key)


def get_owm_id(owm, location_name="Salt Lake City"):
    reg = owm.city_id_registry()
    return reg.ids_for(location_name)


def get_current_weather_by_id(owm, location_id):
    return owm.weather_at_id(location_id)


def get_owm_ids_by_state(engine, session, state="UT"):
    sql = """
    select owm_city_id
    from utah_locations
    where state = {state}
    """.format(
        state=state
    )
    # JK, don't do that. You should paramaterize your query:
    sql = """
    select owm_city_id
    from utah_locations
    where state = :state
    """
    result = session.execute(sql, {"state": state})
    result = list(a[0] for a in result)
    return result


def check_weather_status(engine, session, weather_status, weather_status_detailed):
    exists = session.query(m.LU_Weather_Status).filter(
        m.LU_Weather_Status.weather_status_text == weather_status,
        m.LU_Weather_Status.weather_status_text_detailed == weather_status_detailed,
    )
    # Checks to see if the row already exists in the table
    if exists.first():
        # print("Status Exists: {}".format(exists.first().__dict__))
        return exists.first().weather_status_id

    # Otherwise, it doesn't exist and must add it first.
    else:
        status = m.LU_Weather_Status(
            weather_status_text=weather_status,
            weather_status_text_detailed=weather_status_detailed,
        )
        session.add(status)
        session.commit()

        # print("Status Added: {}".format(status.__dict__))
        return status.weather_status_id


def add_weather_event_to_database(engine, session, weather):
    from pprint import pprint

    # ...__dict__ is actually just as easy as using the various "get" methods for this particular API, but
    # I'll play ball and use all functions for this.
    # https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html#owm-weather-api-version-2-5-usage-examples
    w = weather.get_weather()
    l = weather.get_location()

    weather_event = m.Weather_Event(
        owm_city_id=l.get_name(),
        reception_time_epoch=weather.get_reception_time(),
        reception_time_gmt=weather.get_reception_time("date"),
        reference_time_epoch=w.get_reference_time(),
        reference_time_gmt=w.get_reference_time(timeformat="date"),
        weather_status_id=check_weather_status(
            engine=engine,
            session=session,
            weather_status=w.get_status(),
            weather_status_detailed=w.get_detailed_status(),
        ),
        cloud_cover_pct=w.get_clouds(),
        # Temperature in freedom units
        temperature_f=w.get_temperature(unit="fahrenheit").get("temp"),
        temperature_c=w.get_temperature(unit="celsius").get("temp"),
        temperature_k=w.get_temperature().get("temp"),
        temp_min_f=w.get_temperature(unit="fahrenheit").get("temp_min"),
        temp_min_c=w.get_temperature(unit="celsius").get("temp_min"),
        temp_min_k=w.get_temperature().get("temp_min"),
        temp_max_f=w.get_temperature(unit="fahrenheit").get("temp_max"),
        temp_max_c=w.get_temperature(unit="celsius").get("temp_max"),
        temp_max_k=w.get_temperature().get("temp_max"),
        humidity=w.get_humidity(),
        pressure_hpa=w.get_pressure().get("press"),
        sea_level_pressure=w.get_pressure().get("sea_level"),
        rain_1h_mm=w.get_rain().get("1h"),
        snow_1h_mm=w.get_snow().get("1h"),
        wind_speed_meter_second=w.get_wind().get("speed"),
        wind_direction_degrees=w.get_wind().get("deg"),
        dew_point=w._dewpoint,
        heat_index=w._heat_index,
        visibility_distance=w._visibility_distance,
        weather_code=w.get_weather_code(),
        weather_icon=w.get_weather_icon_name(),
    )
    session.merge(weather_event)
    session.commit()
    # pprint(weather.__dict__)
    # pprint(weather._weather.__dict__)


def adjust_epoch_date_for_tz(engine, session, owm_city_id, epoch_time):
    timezone = (
        session.query(m.Location).filter(m.Location.owm_city_id == owm_city_id).first()
    )
    tz_offset = pytz.timezone(timezone.timezone)
    dt = datetime.datetime.fromtimestamp(epoch_time)
    return dt.astimezone(tz_offset)


def add_sun_schedule_to_database(engine, session, weather):
    l = weather.get_location()
    w = weather.get_weather()

    sunrise = adjust_epoch_date_for_tz(
        engine=engine,
        session=session,
        owm_city_id=l._ID,
        epoch_time=w.get_sunrise_time(),
    )
    sunset = adjust_epoch_date_for_tz(
        engine=engine,
        session=session,
        owm_city_id=l._ID,
        epoch_time=w.get_sunset_time(),
    )

    sun_schedule = m.Sun_Schedule(
        sun_date_local_tz=sunrise.date(),
        owm_city_id=l._ID,
        sunrise_local_tz=sunrise,
        sunset_local_tz=sunset,
    )
    session.merge(sun_schedule)
    session.commit()


def save_utah_weather(engine, session):
    utah_owm_ids = get_owm_ids_by_state(engine, session, "UT")
    owm = owm_connect()
    for id in utah_owm_ids:
        weather = get_current_weather_by_id(owm, id)
        print("Fetching Weather for: {}".format(weather.get_location()._name))
        add_weather_event_to_database(engine, session, weather)
        add_sun_schedule_to_database(engine, session, weather)
