# app/utils.py

import random
import string
from urllib.parse import urlparse

def generate_short_code(length: int = 6) -> str:
    """Generates a random alphanumeric string of a given length."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

def is_valid_url(url: str) -> bool:
    """Validates a URL by checking for a scheme and a netloc."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except (ValueError, AttributeError):
        return False