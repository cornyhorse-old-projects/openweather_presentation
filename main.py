from database import tests as db_test
from module_owm import tests as pyowm_test, weather as w
from requests_owm import tests as request_test
from database import database as db
from database import models as m

if __name__ == "__main__":
    # db_test.test_all()
    engine, session = db.sqlalchemy_connect()
    m.recreate_models(engine, session)
    session.commit()

    w.save_utah_weather(engine, session)
