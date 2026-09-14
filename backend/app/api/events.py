from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.event import Event, EventStatus
from app.schemas.event import EventOut

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    """For now: just return upcoming, published events. Filters come later."""
    query = (
        db.query(Event)
        .filter(Event.status == EventStatus.published)
        .filter(Event.start_time >= datetime.now(timezone.utc))
        .order_by(Event.start_time.asc())
    )
    return query.all()
