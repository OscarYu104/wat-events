import enum
import uuid

from sqlalchemy import(
    Column, String, Text, DateTime, Enum, Numeric, Boolean, ForeignKey, func, Index
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TSVECTOR
from sqlalchemy.orm import relationship

from app.core.database import Base

class EventStatus(str, enum.Enum):
    pending_review = "pending_review"
    published = "published"
    rejected = "rejected"
    expired = "expired"

class EventCategory(str, enum.Enum):
    academic = "academic"
    career = "career"
    social = "social"
    sports = "sports"
    arts_culture = "arts_culture"
    volunteering = "volunteering"
    workshop = "workshop"
    food = "food"
    other = "other"

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=True)

    location_name = Column(String, nullable=True)
    location_address = Column(String, nullable=True)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    is_online = Column(Boolean, default=False)

    categories = Column(ARRAY(Enum(EventCategory)), default=list)

    is_free = Column(Boolean, default=True)
    cost_amount = Column(Numeric(8, 2), nullable=True)
    cost_notes = Column(String, nullable=True)

    image_url = Column(String, nullable=True)
    external_url = Column(String, nullable=True)

    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    source = relationship("Source")
    status = Column(Enum(EventStatus), default=EventStatus.pending_review, nullable=False, index=True)
    raw_source_id = Column(String, nullable=True)

    dedup_hash = Column(String, nullable=True, index=True)
    search_vector = Column(TSVECTOR, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_events_search_vector", "search_vector", postgresql_using="gin"),
    )