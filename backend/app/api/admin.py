from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.event import Event, EventStatus
from app.schemas.event import EventOut

# no auth yet
router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/queue", response_model=list[EventOut])
def get_moderation_queue(db: Session = Depends(get_db)):
    return (
        db.query(Event)
        .filter(Event.status == EventStatus.pending_review)
        .order_by(Event.created_at.asc())
        .all()
    )

@router.post("/{event_id}/approve", response_model=EventOut)
def approve_event(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.status = EventStatus.published
    db.commit()
    db.refresh(event)
    return event

@router.post("/{event_id}/reject", response_model=EventOut)
def reject_event(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.status = EventStatus.rejected
    db.commit()
    db.refresh(event)
    return event
