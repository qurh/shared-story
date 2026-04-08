from typing import Literal

from pydantic import BaseModel, Field

SortMode = Literal["composite", "subscribers", "latest_active"]


class ActivityPreviewOut(BaseModel):
    insights: list["InsightOut"] = Field(default_factory=list)
    discussions: list["DiscussionOut"] = Field(default_factory=list)


class StorySummaryOut(BaseModel):
    id: str
    title: str
    summary: str
    status: str
    view_count: int = 0
    discussion_count: int = 0
    participant_role_count: int = 0
    subscriber_count: int = 0
    doubt_count: int = 0
    age_hours: int = 0


class StoryDetailOut(StorySummaryOut):
    activity_preview: ActivityPreviewOut = Field(default_factory=ActivityPreviewOut)


class InsightOut(BaseModel):
    id: str
    story_id: str
    role_id: str
    title: str
    summary: str
    content: str
    status: str


class DiscussionOut(BaseModel):
    id: str
    story_id: str
    role_id: str
    content: str
    status: str


class SearchFallbackOut(BaseModel):
    insights: list[InsightOut] = Field(default_factory=list)
    discussions: list[DiscussionOut] = Field(default_factory=list)


class ListStoriesData(BaseModel):
    stories: list[StorySummaryOut]
    sort: SortMode


class StoryDetailData(BaseModel):
    story: StoryDetailOut


class SearchData(BaseModel):
    stories: list[StorySummaryOut]
    fallback: SearchFallbackOut


class SubscriptionData(BaseModel):
    story_id: str
    subscribed: bool
    subscriber_count: int
