from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import configparser

config = configparser.ConfigParser()
config.read('app/intel/bookintel.conf')
USER = config.get("DATABASE", "USER")
PASSWORD = config.get("DATABASE", "PASSWORD")
HOST = config.get("DATABASE", "HOST")
PORT = config.get("DATABASE", "PORT")
DATABASE = config.get("DATABASE", "INTEL_DB")

engine = create_engine(url="postgresql://{0}:{1}@{2}:{3}/{4}".format(USER, PASSWORD, HOST, PORT, DATABASE))

Base = declarative_base()

Base.metadata.reflect(engine)

class BOOKS(Base):
    __table__ = Base.metadata.tables['books']

class REVIEWS(Base):
    __table__ = Base.metadata.tables['reviews']

