import os
import redis
from datetime import timedelta


BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIRS, 'media')


class Config:
    SECRET_KEY = 'this is private'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    JWT_SECRET_KEY = 'super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    SECURITY_PASSWORD_SALT = 'my_precious_two'


class RedisConfig:
    HOST = os.environ.get('REDIS_HOST', 'localhost')
    PORT = os.environ.get('REDIS_PORT', 6379)
    CHANNEL_NAME = 'events'
    PASSWORD = os.environ.get('REDIS_PASSWORD', '12345')

    @classmethod
    def client(cls):
        return redis.Redis(host=cls.HOST, port=cls.PORT, password=cls.PASSWORD, db=0)