import sqlite3
import os


def get_conn():
    conn_str = os.path.join(os.path.expanduser("~"), "openweather.db")
    conn = sqlite3.connect(conn_str)
    c = conn.cursor()
    return conn, c
