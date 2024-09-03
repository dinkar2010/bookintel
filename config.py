import os
import configparser

config = configparser.ConfigParser()
config.read('app/intel/bookintel.conf')

USER = config.get("DATABASE", "USER")
PASSWORD = config.get("DATABASE", "PASSWORD")
HOST = config.get("DATABASE", "HOST")
PORT = config.get("DATABASE", "PORT")
DATABASE = config.get("DATABASE", "INTEL_DB")

SECRET_KEY = config.get("APP_SECRET", "SECRET_KEY")

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "postgresql://{}:{}@{}:{}/{}".format(
        USER, PASSWORD, HOST, PORT, DATABASE))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)