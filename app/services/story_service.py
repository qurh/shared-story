from app.services.in_memory_store import STORIES


class StoryService:
    def list_stories(self) -> list[dict]:
        return [story for story in STORIES if story["status"] == "published"]

    def get_story(self, story_id: str) -> dict | None:
        for story in STORIES:
            if story["id"] == story_id and story["status"] == "published":
                return story
        return None
