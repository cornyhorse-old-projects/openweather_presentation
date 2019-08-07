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
from . import database as db


def recreate_models(engine):
    db.Base.metadata.drop_all(engine)
    create_models(engine)
    utah_id_file_path = os.path.join(os.path.abspath("."), "utah_location_ids.csv")
    utah_ids = pd.read_csv(utah_id_file_path)
    utah_ids.to_sql(con=engine, name='utah_locations')

def create_models(engine):
    db.Base.metadata.create_all(engine)
