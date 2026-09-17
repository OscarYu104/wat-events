"""
V1 category classification: keyword matching. 
"""
import re

from app.models.event import EventCategory


_KEYWORDS: dict[EventCategory, list[str]] = {
    EventCategory.career: [
        "career", "resume", "job fair", "recruit", "networking", "internship",
        "co-op", "interview prep", "employer", "job search",
    ],
    EventCategory.academic: [
        "lecture", "seminar", "study", "exam", "tutorial", "research",
        "academic", "course", "midterm", "thesis",
    ],
    EventCategory.workshop: [
        "workshop", "training", "hands-on", "learn how", "bootcamp", "skill-building",
    ],
    EventCategory.sports: [
        "sports", "game", "tournament", "fitness", "gym", "athletics",
        "intramural", "run", "yoga", "hockey", "basketball", "soccer",
    ],
    EventCategory.arts_culture: [
        "art", "music", "concert", "theatre", "theater", "film", "gallery",
        "performance", "culture", "dance", "exhibit",
    ],
    EventCategory.volunteering: [
        "volunteer", "charity", "fundraiser", "donate", "community service",
        "nonprofit",
    ],
    EventCategory.food: [
        "food", "pizza", "bbq", "dinner", "lunch", "snack", "free food",
        "cafe", "coffee",
    ],
    EventCategory.social: [
        "party", "social", "mixer", "meet and greet", "hangout", "bingo",
        "formal", "fest", "night out", "games night",
    ],
}


def infer_categories(title: str, description: str | None) -> list[EventCategory]:
    text = f"{title} {description or ''}".lower()

    matched = [
        category
        for category, keywords in _KEYWORDS.items()
        if any(re.search(rf"\b{re.escape(kw)}\b", text) for kw in keywords)
    ]

    return matched if matched else [EventCategory.other]