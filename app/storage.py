# app/storage.py

import threading
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class URLMapping:
    """Data class to hold all information for a shortened URL."""
    original_url: str
    short_code: str
    created_at: datetime
    clicks: int = 0

class InMemoryStorage:
    """
    A thread-safe, in-memory storage for URL mappings.
    Uses a lock to handle concurrent requests safely.
    """
    def __init__(self):
        self._urls = {}
        self._lock = threading.Lock()

    def save(self, mapping: URLMapping) -> None:
        """Saves a URLMapping object, keyed by its short code."""
        with self._lock:
            self._urls[mapping.short_code] = mapping

    def find_by_short_code(self, short_code: str) -> URLMapping | None:
        """Retrieves a URLMapping by its short code."""
        with self._lock:
            return self._urls.get(short_code)

    def increment_click_count(self, short_code: str) -> bool:
        """Increments the click count for a given short code. Returns True if successful."""
        with self._lock:
            mapping = self._urls.get(short_code)
            if mapping:
                mapping.clicks += 1
                return True
            return False