import math

from app.core.runtime_config import load_runtime_config


def normalize_min_max(value: float, min_value: float, max_value: float) -> float:
    if max_value == min_value:
        return 1.0
    return (value - min_value) / (max_value - min_value)


def freshness_score(age_hours: float, decay_hours: float = 72.0) -> float:
    return math.exp(-age_hours / decay_hours)


def composite_score(
    *,
    subscribers: float,
    discussions: float,
    participants: float,
    views: float,
    doubt: float,
    age_hours: float,
) -> float:
    cfg = load_runtime_config()
    w = cfg.COMPOSITE_SORT_WEIGHTS
    fresh = freshness_score(age_hours, cfg.FRESHNESS_DECAY_HOURS)
    return (
        w["subscribers"] * subscribers
        + w["discussions"] * discussions
        + w["participants"] * participants
        + w["views"] * views
        + w["freshness"] * fresh
        + w["doubt_penalty"] * doubt
    )


def sort_stories(stories: list[dict], mode: str = "composite") -> list[dict]:
    if not stories:
        return []

    if mode == "subscribers":
        return sorted(stories, key=lambda s: s.get("subscriber_count", 0), reverse=True)
    if mode == "latest_active":
        return sorted(stories, key=lambda s: s.get("age_hours", 10**9))

    subs = [s.get("subscriber_count", 0) for s in stories]
    dis = [s.get("discussion_count", 0) for s in stories]
    par = [s.get("participant_role_count", 0) for s in stories]
    views = [s.get("view_count", 0) for s in stories]
    doubts = [s.get("doubt_count", 0) for s in stories]

    scored: list[tuple[float, dict]] = []
    for s in stories:
        score = composite_score(
            subscribers=normalize_min_max(s.get("subscriber_count", 0), min(subs), max(subs)),
            discussions=normalize_min_max(s.get("discussion_count", 0), min(dis), max(dis)),
            participants=normalize_min_max(s.get("participant_role_count", 0), min(par), max(par)),
            views=normalize_min_max(s.get("view_count", 0), min(views), max(views)),
            doubt=normalize_min_max(s.get("doubt_count", 0), min(doubts), max(doubts)),
            age_hours=s.get("age_hours", 0),
        )
        scored.append((score, s))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in scored]
