import hashlib
import re
from datetime import datetime


def compute_dedup_hash(title: str, start_time: datetime | None) -> str:
    """
    normalize the title and round to the day.
    """
    normalized_title = re.sub(r"[^a-z0-9]+", "", title.lower())
    date_part = start_time.strftime("%Y%m%d") if start_time else "nodate"
    raw = f"{normalized_title}:{date_part}"
    return hashlib.sha256(raw.encode()).hexdigest()