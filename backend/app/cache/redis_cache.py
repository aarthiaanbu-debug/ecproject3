class MemoryCache:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def setex(self, key, seconds, value):
        self.store[key] = value
        return True


try:
    import redis

    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
    )
    redis_client.ping()
except Exception:
    redis_client = MemoryCache()
