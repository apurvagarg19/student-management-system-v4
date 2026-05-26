import time


class SimpleCache:

    def __init__(self):

        self.cache = {}

    # ---------------- GET ----------------

    def get(self, key):

        value = self.cache.get(key)

        if value is None:
            return None

        data, expiry = value

        # Expired cache
        if expiry < time.time():

            del self.cache[key]

            return None

        return data

    # ---------------- SET ----------------

    def set(
        self,
        key,
        value,
        ttl=60
    ):

        expiry = time.time() + ttl

        self.cache[key] = (
            value,
            expiry
        )

    # ---------------- INVALIDATE ----------------

    def invalidate(self, key):

        if key in self.cache:
            del self.cache[key]

    # ---------------- CLEAR ----------------

    def clear(self):

        self.cache.clear()


# Global cache instance
cache = SimpleCache()