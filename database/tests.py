import database.database as db
import database.credentials as cdb


def test_database_exists():
    conn, c = db.get_conn()
    if conn and c:
        print("Database Connected.")


def test_keepass_database_exists():
    credentials = cdb.get_credentials()
    credentials = credentials.password
    if len(credentials) > 0:
        print("Keepass Database Connected.")
    else:
        print("Keepass Database not connected.")


if __name__ == "__main__":
    test_database_exists()
    test_keepass_database_exists()
