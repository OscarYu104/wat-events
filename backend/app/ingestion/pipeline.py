import logging

from sqlalchemy.orm import Session

from app.ingestion.base import BaseConnector, RawEvent
from app.models.event import Event, EventStatus, EventCategory
from app.models.source import Source
from app.services.dedup import compute_dedup_hash

logger = logging.getLogger(__name__)


def run_connector(connector: BaseConnector, source: Source, db: Session) -> dict:
    stats = {"fetched": 0, "created": 0, "skipped_duplicate": 0, "skipped_no_date": 0, "errors": 0}

    try:
        raw_events = connector.fetch()
    except Exception:
        logger.exception("Connector fetch failed for source=%s", source.name)
        return stats

    stats["fetched"] = len(raw_events)

    for raw in raw_events:
        try:
            created = _upsert_event(raw, source, db)
            if created:
                stats["created"] += 1
            else:
                stats["skipped_duplicate"] += 1
        except Exception:
            logger.exception("Failed to process event %r from %s", raw.title, source.name)
            stats["errors"] += 1

    db.commit()
    return stats


def _upsert_event(raw: RawEvent, source: Source, db: Session) -> bool:
    if not raw.start_time:
        return False

    dedup_hash = compute_dedup_hash(raw.title, raw.start_time)

    existing = db.query(Event).filter(Event.dedup_hash == dedup_hash).first()
    if existing:
        return False

    event = Event(
        title=raw.title,
        description=raw.description,
        start_time=raw.start_time,
        end_time=raw.end_time,
        location_name=raw.location_name,
        is_online=raw.is_online,
        is_free=raw.is_free if raw.is_free is not None else True,
        cost_amount=raw.cost_amount,
        external_url=raw.external_url,
        source_id=source.id,
        raw_source_id=raw.raw_source_id,
        dedup_hash=dedup_hash,
        categories=[EventCategory.other],  
        status=EventStatus.pending_review,
    )
    db.add(event)
    db.flush()
    return True