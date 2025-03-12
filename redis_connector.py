from dotenv import load_dotenv
import os
import redis

load_dotenv(dotenv_path="/.env", override=True)

class RedisConnector:

    def __init__(self):

        self.redis_cli = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            charset="utf-8",
            decode_responses=True
            )

    def set(self, key, value):

        if type(value) == dict:
            self.redis_cli.hmset(key, mapping=value)
        else:
            raise Exception("Value must be a dictionary")

    def get(self, key):
        if not self.redis_cli.exists(key):
            raise Exception(f"Key {key} does not exist in Redis")
        if self.redis_cli.ping() == False:
            raise Exception("Redis server is not reachable")
        return self.redis_cli.hgetall(key)
    

