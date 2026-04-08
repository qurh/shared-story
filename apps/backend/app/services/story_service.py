from app.services.in_memory_store import STORIES
from app.services.ranking_service import sort_stories


class StoryService:
    def list_stories(self, sort_mode: str = "composite") -> list[dict]:
        published = [story for story in STORIES if story["status"] == "published"]
        return sort_stories(published, mode=sort_mode)

    def get_story(self, story_id: str) -> dict | None:
        for story in STORIES:
            if story["id"] == story_id and story["status"] == "published":
                return story
        return None
