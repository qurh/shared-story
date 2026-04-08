from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.in_memory_store import DISCUSSIONS, INSIGHTS
from app.services.story_service import StoryService

router = APIRouter()
story_service = StoryService()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@router.get("/stories", response_class=HTMLResponse)
def story_feed(request: Request, sort: str = "composite"):
    stories = story_service.list_stories(sort_mode=sort)
    return templates.TemplateResponse(
        request=request,
        name="story_feed.html",
        context={"stories": stories, "sort": sort},
    )


@router.get("/stories/{story_id}", response_class=HTMLResponse)
def story_detail(request: Request, story_id: str):
    story = story_service.get_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    insights = [i for i in INSIGHTS if i["story_id"] == story_id and i["status"] == "published"]
    discussions = [d for d in DISCUSSIONS if d["story_id"] == story_id and d["status"] == "published"]

    return templates.TemplateResponse(
        request=request,
        name="story_detail.html",
        context={"story": story, "insights": insights, "discussions": discussions},
    )
