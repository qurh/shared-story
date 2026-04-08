from app.core.runtime_config import load_runtime_config
from app.services.in_memory_store import DISCUSSIONS, INSIGHTS, STORIES


class SearchService:
    def __init__(self) -> None:
        self.runtime_config = load_runtime_config()

    def search(self, query: str) -> dict:
        q = query.strip().lower()
        story_results = [
            s
            for s in STORIES
            if s["status"] == "published" and (q in s["title"].lower() or q in s["summary"].lower())
        ]

        fallback = {"insights": [], "discussions": []}
        if len(story_results) < self.runtime_config.SEARCH_STORY_MIN_RESULTS:
            fallback["insights"] = [
                i
                for i in INSIGHTS
                if i["status"] == "published"
                and (q in i["title"].lower() or q in i["summary"].lower() or q in i["content"].lower())
            ]
            fallback["discussions"] = [
                d
                for d in DISCUSSIONS
                if d["status"] == "published" and q in d["content"].lower()
            ]

        return {"stories": story_results, "fallback": fallback}
