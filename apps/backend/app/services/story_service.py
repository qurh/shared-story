from copy import deepcopy

from app.services.in_memory_store import DISCUSSIONS, INSIGHTS, STORIES
from app.services.ranking_service import sort_stories


class StoryService:
    def list_stories(self, sort_mode: str = "composite") -> list[dict]:
        published = [story for story in STORIES if story["status"] == "published"]
        return sort_stories(published, mode=sort_mode)

    def get_story(self, story_id: str) -> dict | None:
        for story in STORIES:
            if story["id"] == story_id and story["status"] == "published":
                story_copy = deepcopy(story)
                story_copy["activity_preview"] = {
                    "insights": [
                        insight
                        for insight in INSIGHTS
                        if insight["story_id"] == story_id and insight["status"] == "published"
                    ][:3],
                    "discussions": [
                        discussion
                        for discussion in DISCUSSIONS
                        if discussion["story_id"] == story_id and discussion["status"] == "published"
                    ][:3],
                }
                return story_copy
        return None
