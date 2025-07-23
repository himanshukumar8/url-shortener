# app/services.py

from datetime import datetime, timezone
from .storage import InMemoryStorage, URLMapping
from .utils import generate_short_code, is_valid_url

class URLShortenerService:
    """Encapsulates the core business logic for the URL shortener."""
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_shortened_url(self, original_url: str) -> URLMapping:
        """
        Creates a new shortened URL.
        Raises ValueError if the URL is invalid.
        """
        if not is_valid_url(original_url):
            raise ValueError("Invalid URL provided.")

        while True:
            short_code = generate_short_code()
            if not self.storage.find_by_short_code(short_code):
                break

        mapping = URLMapping(
            original_url=original_url,
            short_code=short_code,
            created_at=datetime.now(timezone.utc)
        )
        self.storage.save(mapping)
        return mapping

    def get_and_track_url(self, short_code: str) -> str | None:
        """
        Retrieves the original URL for a short code and tracks the click.
        Returns the original URL or None if not found.
        """
        mapping = self.storage.find_by_short_code(short_code)
        if mapping:
            self.storage.increment_click_count(short_code)
            return mapping.original_url
        return None

    def get_url_stats(self, short_code: str) -> URLMapping | None:
        """Retrieves the statistics for a short code."""
        return self.storage.find_by_short_code(short_code)