import sqlite3
import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

# import database.modedls as m
Base = declarative_base()


def create_conn_string():
    return os.path.join(os.path.expanduser("~"), "openweather.db")


def get_conn():
    conn_str = create_conn_string()
    conn = sqlite3.connect(conn_str)
    c = conn.cursor()
    return conn, c


def sqlalchemy_connect():
    # 1. Retrieve the Conneciton String, in the case of SQLite, this is just the file path.
    conn_str = "sqlite:///{}".format(create_conn_string())

    # 2. Create the Engine
    #    https://docs.sqlalchemy.org/en/13/core/engines.html
    # This is used to directly interface with the database.
    engine = sqlalchemy.create_engine(conn_str)

    # 3. Create a session with the database
    #    https://docs.sqlalchemy.org/en/13/orm/session.html
    #    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#what-does-the-session-do
    # The session object is an implementation of the funciton Session(), when used in conjunction with the ORM's
    # sessionmaker function, it makes one, centralized instance with which it can talk to the database.
    Session = sqlalchemy.orm.sessionmaker(autoflush=False)
    Session.configure(bind=engine)
    session = Session()

    # Return both objects to be passed around to various functions which interface with the database.
    return engine, session
