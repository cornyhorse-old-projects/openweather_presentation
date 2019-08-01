import pykeepass as pyk
import os

def get_credentials():
    db_location = os.path.join(os.path.expanduser("~"), 'credentials/Passwords.kdbx')
    kp = pyk.PyKeePass(db_location, password="password")
    return kp.find_entries(title='openweathermap')[0]