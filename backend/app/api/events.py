from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.event import Event, EventStatus
from app.models.source import Source, SourceType
from app.schemas.event import EventOut, EventCreate

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

@router.post("/submit", response_model=EventOut, status_code=201)
def submit_event(payload: EventCreate, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.name == payload.source_name).first()
    if not source:
        source = Source(name=payload.source_name, type=SourceType.manual_submission)
        db.add(source)
        db.flush()

    event = Event(
        **payload.model_dump(exclude={"source_name"}),
        source_id=source.id,
        status=EventStatus.published,  # temporary: publish immediately so you can test GET /events too
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
