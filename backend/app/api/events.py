from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.event import Event, EventStatus, EventCategory
from app.models.source import Source, SourceType
from app.schemas.event import EventOut, EventCreate

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventOut])
def list_events(
    db: Session = Depends(get_db),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    category: list[EventCategory] | None = Query(default=None),
    is_free: bool | None = None,
    max_cost: Decimal | None = None,
    is_online: bool | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20,
):
    query = db.query(Event).filter(Event.status == EventStatus.published)

    if date_from:
        query = query.filter(Event.start_time >= date_from)
    else:
        query = query.filter(Event.start_time >= datetime.now(timezone.utc))
    if date_to:
        query = query.filter(Event.start_time <= date_to)

    if category:
        query = query.filter(Event.categories.overlap(category))

    if is_free is not None:
        query = query.filter(Event.is_free == is_free)

    if max_cost is not None:
        query = query.filter(
            (Event.is_free == True) | (Event.cost_amount <= max_cost)  
        )

    if is_online is not None:
        query = query.filter(Event.is_online == is_online)

    if search:
        query = query.filter(
            Event.title.ilike(f"%{search}%") | Event.description.ilike(f"%{search}%")
        )

    query = query.order_by(Event.start_time.asc())
    query = query.offset((page - 1) * page_size).limit(page_size)

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
        status=EventStatus.pending_review,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
