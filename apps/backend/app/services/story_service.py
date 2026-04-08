from datetime import datetime
from copy import deepcopy

from app.services.in_memory_store import DISCUSSIONS, INSIGHTS, STORIES
from app.services.ranking_service import sort_stories


def _latest_by_created_at(items: list[dict], limit: int = 3) -> list[dict]:
    # created_at is the explicit ordering key: pick the newest items first, then
    # restore display order so the preview reads oldest-to-newest within the window.
    latest = sorted(items, key=lambda item: datetime.fromisoformat(item["created_at"]), reverse=True)[:limit]
    latest.reverse()
    return latest


class StoryService:
    def list_stories(self, sort_mode: str = "composite") -> list[dict]:
        published = [story for story in STORIES if story["status"] == "published"]
        return sort_stories(published, mode=sort_mode)

    def get_story(self, story_id: str) -> dict | None:
        for story in STORIES:
            if story["id"] == story_id and story["status"] == "published":
                story_copy = deepcopy(story)
                story_insights = [
                    insight
                    for insight in INSIGHTS
                    if insight["story_id"] == story_id and insight["status"] == "published"
                ]
                story_discussions = [
                    discussion
                    for discussion in DISCUSSIONS
                    if discussion["story_id"] == story_id and discussion["status"] == "published"
                ]
                story_copy["activity_preview"] = {
                    "insights": _latest_by_created_at(story_insights),
                    "discussions": _latest_by_created_at(story_discussions),
                }
                return story_copy
        return None
