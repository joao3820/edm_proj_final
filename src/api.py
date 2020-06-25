from time import sleep
import urequests
from ujson import dumps

def getTime():
    url = "http://worldtimeapi.org/api/timezone/Europe/Lisbon"
    r = urequests.get(url).json()
    r = r["datetime"][11:16]
    return(r)