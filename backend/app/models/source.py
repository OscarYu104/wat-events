import enum
import uuid

from sqlalchemy import Column, String, Enum, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class SourceType(str, enum.Enum):
    manual_submission = "manual_submission"
    instagram = "instagram"
    website_scrape = "website_scrape"
    rss_feed = "rss_feed"
    ics_feed = "ics_feed"
    university_calendar = "university_calendar"

class Source(Base):
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum(SourceType), nullable=False)
    url = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_trusted = Column(Boolean, default=False)
    last_scraped_at = Column(DateTime(timezone=True), nullable=True)
    last_scraped_success = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
