from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RawEvent:
    """Before normalization."""
    title: str
    raw_source_id: str  # Use later for dedup
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    location_name: str | None = None
    is_online: bool = False
    is_free: bool | None = None
    cost_amount: float | None = None
    external_url: str | None = None
    extra: dict = field(default_factory=dict)


class BaseConnector(ABC):
    source_name: str

    @abstractmethod
    def fetch(self) -> list[RawEvent]:
        raise NotImplementedError