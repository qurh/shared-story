from fastapi import APIRouter, HTTPException, Query

from app.api.responses import ok
from app.api.schemas.common import ApiResponse
from app.api.schemas.stories import (
    ListStoriesData,
    SearchData,
    SearchFallbackOut,
    StoryDetailData,
    StoryOut,
    SubscriptionData,
)
from app.services.search_service import SearchService
from app.services.story_service import StoryService
from app.services.subscription_service import SubscriptionService

router = APIRouter()

story_service = StoryService()
search_service = SearchService()
subscription_service = SubscriptionService()


@router.get("/stories", response_model=ApiResponse[ListStoriesData])
def list_stories(sort: str = Query(default="composite")) -> ApiResponse[ListStoriesData]:
    if sort not in {"composite", "subscribers", "latest_active"}:
        raise HTTPException(status_code=400, detail="Unsupported sort mode")
    stories = [StoryOut.model_validate(story) for story in story_service.list_stories(sort_mode=sort)]
    return ok(ListStoriesData(stories=stories, sort=sort))


@router.get("/stories/{story_id}", response_model=ApiResponse[StoryDetailData])
def get_story(story_id: str) -> ApiResponse[StoryDetailData]:
    story = story_service.get_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return ok(StoryDetailData(story=StoryOut.model_validate(story)))


@router.get("/search", response_model=ApiResponse[SearchData])
def search(q: str = Query(default="", min_length=1)) -> ApiResponse[SearchData]:
    result = search_service.search(q)
    data = SearchData(
        stories=[StoryOut.model_validate(story) for story in result["stories"]],
        fallback=SearchFallbackOut(
            insights=result["fallback"]["insights"],
            discussions=result["fallback"]["discussions"],
        ),
    )
    return ok(data)


@router.post("/stories/{story_id}/subscribe", response_model=ApiResponse[SubscriptionData])
def subscribe(story_id: str, user_id: str = Query(default="observer-1")) -> ApiResponse[SubscriptionData]:
    result = subscription_service.subscribe(user_id=user_id, story_id=story_id)
    if not result:
        raise HTTPException(status_code=404, detail="Story not found")
    return ok(SubscriptionData.model_validate(result))


@router.delete("/stories/{story_id}/subscribe", response_model=ApiResponse[SubscriptionData])
def unsubscribe(story_id: str, user_id: str = Query(default="observer-1")) -> ApiResponse[SubscriptionData]:
    result = subscription_service.unsubscribe(user_id=user_id, story_id=story_id)
    if not result:
        raise HTTPException(status_code=404, detail="Story not found")
    return ok(SubscriptionData.model_validate(result))
