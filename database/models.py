from sqlalchemy import (
    Column,
    INTEGER,
    TEXT,
    TIMESTAMP,
    ForeignKey,
    DECIMAL,
    UniqueConstraint,
    JSON,
    BOOLEAN,
    DATE,
    FLOAT,
    BIGINT,
    DateTime,
    SMALLINT,
    Numeric,
)
import pandas as pd
import os
from database.database import Base


class Location(Base):
    __tablename__ = "location"

    owm_city_id = Column(INTEGER, primary_key=True)
    city_name = Column(TEXT)
    state = Column(TEXT)
    country = Column(TEXT)
    latitude = Column(TEXT)
    longitude = Column(TEXT)
    timezone = Column(TEXT)


class LU_Weather_Status(Base):
    __tablename__ = "lu_weather_status"

    weather_status_id = Column(INTEGER, primary_key=True, autoincrement=True)
    weather_status_text = Column(TEXT)
    weather_status_text_detailed = Column(TEXT)
    UniqueConstraint(weather_status_text, weather_status_text_detailed)


class Weather_Event(Base):
    __tablename__ = "weather_event"

    weather_event_id = Column(INTEGER, primary_key=True, autoincrement=True)
    owm_city_id = Column(INTEGER, ForeignKey(Location.owm_city_id))
    reception_time_epoch = Column(
        BIGINT
    )  # Time when the data was received by our script.
    reception_time_gmt = Column(
        DateTime
    )  # The time the data was received by our script, converted to a timestamp.)
    reference_time_epoch = Column(BIGINT)  # The time the data was measured as an epoch.
    reference_time_gmt = Column(DateTime)  # Time when the data was measured in GMT
    weather_status_id = Column(INTEGER, ForeignKey(LU_Weather_Status.weather_status_id))
    cloud_cover_pct = Column(INTEGER)
    temperature_k = Column(Numeric(6, 2))
    temperature_c = Column(Numeric(6, 2))
    temperature_f = Column(Numeric(6, 2))
    temp_min_k = Column(Numeric(6, 2))
    temp_min_c = Column(Numeric(6, 2))
    temp_min_f = Column(Numeric(6, 2))
    temp_max_k = Column(Numeric(6, 2))
    temp_max_c = Column(Numeric(6, 2))
    temp_max_f = Column(Numeric(6, 2))
    humidity = Column(SMALLINT)
    pressure_hpa = Column(SMALLINT)
    sea_level_pressure = Column(SMALLINT)
    rain_1h_mm = Column(Numeric(25, 20))
    snow_1h_mm = Column(Numeric(25, 20))
    wind_speed_meter_second = Column(SMALLINT)
    wind_direction_degrees = Column(SMALLINT)
    dew_point = Column(SMALLINT)
    heat_index = Column(SMALLINT)
    visibility_distance = Column(INTEGER)
    weather_code = Column(INTEGER)
    weather_icon = Column(TEXT)
    UniqueConstraint(owm_city_id, reception_time_epoch)


class Sun_Schedule(Base):
    __tablename__ = "sun_schedule"

    sun_schedule_id = Column(INTEGER, primary_key=True, autoincrement=True)
    sun_date_local_tz = Column(DATE)
    owm_city_id = Column(INTEGER, ForeignKey(Location.owm_city_id))
    sunrise_local_tz = Column(DateTime)
    sunset_local_tz = Column(DateTime)
    UniqueConstraint(sun_date_local_tz, owm_city_id)


def create_utah_tables(engine, session):
    utah_id_file_path = os.path.join(os.path.abspath("."), "utah_location_ids.csv")
    utah_ids = pd.read_csv(utah_id_file_path)
    utah_ids.to_sql(con=engine, name="utah_locations", if_exists="replace")
    sql = """select owm_city_id
          ,city_name
          ,state
          ,country
          ,timezone
    from utah_locations
    """
    result = list(session.execute(sql))
    for r in result:
        location = Location(**r)
        session.merge(location)
    session.commit()


def recreate_models(engine, session):
    Base.metadata.drop_all(engine)
    create_models(engine)
    create_utah_tables(engine, session)


def create_models(engine):
    Base.metadata.create_all(engine)
