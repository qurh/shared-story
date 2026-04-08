from pydantic import BaseModel, Field


class InsightSubmission(BaseModel):
    story_id: str
    role_id: str
    title: str
    summary: str
    content: str


class DiscussionSubmission(BaseModel):
    story_id: str
    role_id: str
    content: str


class ReviewResultOut(BaseModel):
    code: str
    reason_code: str | None = None
    reason_text: str | None = None
    fix_actions: list[str] = Field(default_factory=list)


class SubmissionAcceptedData(BaseModel):
    task_id: str
    status: str
    target_id: str | None = None


class SubmissionRejectedData(BaseModel):
    task_id: str
    status: str
    reason_code: str | None = None
    reason_text: str | None = None
    fix_actions: list[str] = Field(default_factory=list)


class ReviewResultData(BaseModel):
    task_id: str
    status: str
    review_result: ReviewResultOut | None = None
    revision_count: int
    max_revisions: int

