# Imports
from os.path import dirname, abspath

# Parent Config Class For Common Attributes
class Config(object):
    DEBUG = False
    TESTING = False
    APP_NAME = "PlagPatrol"
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    DOWNLOAD_FOLDER = dirname(abspath(__file__)) + '/tmp/'

# Config For Production, Inherits From Config
class ProductionConfig(Config):
    SECRET_KEY = "37a310667be5c8a3e7946712b5f2d930378da07a0b919b58"

# Config For Development, Inherits From Config
class DevelopmentConfig(Config):
    ENV = "development"
    SECRET_KEY = "69535ae0bbbcaf0e3ab71bbb626e36541b8c0c61d9180f6e"
    DEBUG = True

# Config for Testing, Inherits From Config
class TestingConfig(Config):
    TESTING = True