import json

from subscribers_service.config.base import RedisConfig


class ReadCache(RedisConfig):
    def __init__(self):
        self.data_list = self.read()

    def load_data(self):
        return [json.loads(json.loads(data)) for data in self.data_list]

    def read(self):
        client = ReadCache.client()
        return client.lrange('posts', 0, -1)
