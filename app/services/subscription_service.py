from app.services.in_memory_store import STORIES, SUBSCRIPTIONS


class SubscriptionService:
    def subscribe(self, *, user_id: str, story_id: str) -> dict | None:
        story = next((s for s in STORIES if s["id"] == story_id and s["status"] == "published"), None)
        if not story:
            return None
        SUBSCRIPTIONS.add((user_id, story_id))
        story["subscriber_count"] = self.count(story_id)
        return {"story_id": story_id, "subscribed": True, "subscriber_count": story["subscriber_count"]}

    def unsubscribe(self, *, user_id: str, story_id: str) -> dict | None:
        story = next((s for s in STORIES if s["id"] == story_id and s["status"] == "published"), None)
        if not story:
            return None
        SUBSCRIPTIONS.discard((user_id, story_id))
        story["subscriber_count"] = self.count(story_id)
        return {"story_id": story_id, "subscribed": False, "subscriber_count": story["subscriber_count"]}

    def count(self, story_id: str) -> int:
        return sum(1 for _, sid in SUBSCRIPTIONS if sid == story_id)
