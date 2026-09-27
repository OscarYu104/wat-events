import logging
from datetime import datetime, date, timezone

from sqlalchemy.orm import Session

from app.ingestion.base import BaseConnector, RawEvent
from app.models.event import Event, EventStatus, EventCategory
from app.models.source import Source
from app.services.dedup import compute_dedup_hash
from app.services.category_inference import infer_categories

logger = logging.getLogger(__name__)


def run_connector(connector: BaseConnector, source: Source, db: Session) -> dict:
    stats = {"fetched": 0, "created": 0, "skipped_duplicate": 0, "skipped_past": 0, "skipped_no_date": 0, "errors": 0}

    try:
        raw_events = connector.fetch()
    except Exception:
        logger.exception("Connector fetch failed for source=%s", source.name)
        return stats

    stats["fetched"] = len(raw_events)

    for raw in raw_events:
        try:
            result = _upsert_event(raw, source, db)
            stats[result] += 1
        except Exception:
            logger.exception("Failed to process event %r from %s", raw.title, source.name)
            stats["errors"] += 1

    db.commit()
    return stats


def _upsert_event(raw: RawEvent, source: Source, db: Session) -> str:
    if not raw.start_time:
        return "skipped_no_date"

    start = raw.start_time
    if isinstance(start, datetime):
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
    elif isinstance(start, date):
        start = datetime(start.year, start.month, start.day, tzinfo=timezone.utc)
    else:
        return "skipped_no_date"

    if start < datetime.now(timezone.utc):
        return "skipped_past"

    dedup_hash = compute_dedup_hash(str(source.id), raw.title, start)

    existing = db.query(Event).filter(Event.dedup_hash == dedup_hash).first()
    if existing:
        return "skipped_duplicate"

    categories = infer_categories(raw.title, raw.description)

    event = Event(
        title=raw.title,
        description=raw.description,
        start_time=start,
        end_time=raw.end_time,
        location_name=raw.location_name,
        is_online=raw.is_online,
        is_free=raw.is_free if raw.is_free is not None else True,
        cost_amount=raw.cost_amount,
        external_url=raw.external_url,
        source_id=source.id,
        raw_source_id=raw.raw_source_id,
        dedup_hash=dedup_hash,
        categories=categories,
        status=EventStatus.pending_review,
    )
    db.add(event)
    db.flush()
    return "created"