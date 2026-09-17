import httpx
from icalendar import Calendar

from app.ingestion.base import BaseConnector, RawEvent


class ICSConnector(BaseConnector):
    def __init__(self, source_name: str, feed_url: str):
        self.source_name = source_name
        self.feed_url = feed_url

    def fetch(self) -> list[RawEvent]:
        resp = httpx.get(self.feed_url, timeout=30)
        resp.raise_for_status()

        cal = Calendar.from_ical(resp.content)
        events: list[RawEvent] = []

        for component in cal.walk("VEVENT"):
            uid = str(component.get("UID"))
            title = str(component.get("SUMMARY", "Untitled event"))
            description = str(component.get("DESCRIPTION", "")) or None
            location = str(component.get("LOCATION", "")) or None
            dtstart = component.get("DTSTART")
            dtend = component.get("DTEND")

            events.append(
                RawEvent(
                    title=title,
                    raw_source_id=uid,
                    description=description,
                    start_time=dtstart.dt if dtstart else None,
                    end_time=dtend.dt if dtend else None,
                    location_name=location,
                    external_url=str(component.get("URL", "")) or None,
                )
            )
        return events