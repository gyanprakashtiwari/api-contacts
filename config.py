import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY',"637b4898e3234e403e9e1f2c035cdd20")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL' , "postgresql://gyan1:gyan123@localhost/contacts")
    SQLALCHEMY_TRACK_MODIFICATIONS = False




