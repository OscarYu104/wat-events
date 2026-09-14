import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.event import EventStatus, EventCategory

class EventBase(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime | None = None

    location_name: str | None = None
    location_address: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    is_online: bool = False

    categories: list[EventCategory] = []

    is_free: bool = True
    cost_amount: Decimal | None = None
    cost_notes: str | None = None

    image_url: str | None = None
    external_url: str | None = None


class EventOut(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: EventStatus
    source_id: uuid.UUID
    created_at: datetime

class EventCreate(EventBase):
    """Used by manual submission — clubs won't have a source_id, just a name."""
    source_name: str