from fastapi import APIRouter, HTTPException, Query

from app.services.search_service import SearchService
from app.services.story_service import StoryService
from app.services.subscription_service import SubscriptionService

router = APIRouter()

story_service = StoryService()
search_service = SearchService()
subscription_service = SubscriptionService()


@router.get("/stories")
def list_stories() -> dict:
    return {"success": True, "data": {"stories": story_service.list_stories()}}


@router.get("/stories/{story_id}")
def get_story(story_id: str) -> dict:
    story = story_service.get_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"success": True, "data": {"story": story}}


@router.get("/search")
def search(q: str = Query(default="", min_length=1)) -> dict:
    return {"success": True, "data": search_service.search(q)}


@router.post("/stories/{story_id}/subscribe")
def subscribe(story_id: str, user_id: str = Query(default="observer-1")) -> dict:
    result = subscription_service.subscribe(user_id=user_id, story_id=story_id)
    if not result:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"success": True, "data": result}


@router.delete("/stories/{story_id}/subscribe")
def unsubscribe(story_id: str, user_id: str = Query(default="observer-1")) -> dict:
    result = subscription_service.unsubscribe(user_id=user_id, story_id=story_id)
    if not result:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"success": True, "data": result}
