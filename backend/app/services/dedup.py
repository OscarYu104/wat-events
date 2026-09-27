import hashlib
import re
from datetime import datetime


def compute_dedup_hash(source_id: str, title: str, start_time: datetime | None) -> str:
    normalized_title = re.sub(r"[^a-z0-9]+", "", title.lower())
    date_part = start_time.strftime("%Y%m%d") if start_time else "nodate"
    raw = f"{source_id}:{normalized_title}:{date_part}"
    return hashlib.sha256(raw.encode()).hexdigest()