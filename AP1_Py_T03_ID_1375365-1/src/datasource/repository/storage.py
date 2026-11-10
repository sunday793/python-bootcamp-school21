import threading


class Storage:
    """Thread-safe in-memory storage for games."""
    def __init__(self):
        self._lock = threading.RLock()
        self._games = {}

    def put(self, uuid, entity):
        with self._lock:
            self._games[uuid] = entity

    def get(self, uuid):
        with self._lock:
            return self._games.get(uuid)