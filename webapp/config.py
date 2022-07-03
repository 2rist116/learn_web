from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

WEATHER_DEFAULT_CITY = "Moscow,Russia"
WEATHER_URL = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
WEATHER_API_KEY = '6319abdc786d470ab78171232222905'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SECRET_KEY = "slgjn9482jto2mf2lkmed19-139"

REMEMBER_COOKIE_DURATION = timedelta(days=5)
SQLALCHEMY_TRACK_MODIFICATIONS = False
